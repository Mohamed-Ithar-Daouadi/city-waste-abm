import random
from collections import deque
from mesa import Agent
from city_generator import is_walkable


def bfs(grid, start, goal_fn, width, height):
    
    queue = deque()
    queue.append((start, [start]))
    visited = {start}

    while queue:
        (cx, cy), path = queue.popleft()

        if goal_fn(cx, cy) and (cx, cy) != start:
            if len(path) > 1:
                return path[1]   
            return start

        
        for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            nx, ny = cx + dx, cy + dy
            if (nx, ny) not in visited and is_walkable(grid, nx, ny, width, height):
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(nx, ny)]))

    return None  

class LocalHuman(Agent):
    

    def __init__(self, model, home, work):
        super().__init__(model)
        self.home = home
        self.work = work
        self.waste_prob = 0.05   # 5% chance to drop waste per step
        self.bin_radius = 2      # uses a bin if within 2 cells

    def step(self):
        self._move()
        self._maybe_generate_waste()

    def _move(self):
        target = self.work if self.model.is_day else self.home
        x, y = self.pos
        if (x, y) == target:
            return
        next_step = bfs(
            self.model.city_grid, (x, y),
            lambda cx, cy: (cx, cy) == target,
            self.model.grid.width, self.model.grid.height
        )
        if next_step:
            self.model.grid.move_agent(self, next_step)

    def _maybe_generate_waste(self):
        if random.random() < self.waste_prob:
            x, y = self.pos
            neighbors = self.model.grid.get_neighbors(
                self.pos, moore=True, include_center=False, radius=self.bin_radius
            )
            for agent in neighbors:
                if isinstance(agent, DustBin) and not agent.is_full():
                    agent.receive_waste(1)
                    return
            self.model.street_waste[x][y] += 1
            self.model.total_waste_generated += 1


class Tourist(Agent):

    def __init__(self, model):
        super().__init__(model)
        self.waste_prob = 0.15  
        self.center = (model.grid.width // 2, model.grid.height // 2)

    def step(self):
        if not self.model.is_day:
            return
        self._move()
        self._maybe_generate_waste()

    def _move(self):
        x, y = self.pos
        if random.random() < 0.6:
            cx, cy = self.center
            dx = 1 if cx > x else (-1 if cx < x else 0)
            dy = 1 if cy > y else (-1 if cy < y else 0)
            candidates = [(x+dx, y), (x, y+dy), (x+dx, y+dy)]
        else:
            candidates = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]

        random.shuffle(candidates)
        for nx, ny in candidates:
            if is_walkable(self.model.city_grid, nx, ny,
                           self.model.grid.width, self.model.grid.height):
                self.model.grid.move_agent(self, (nx, ny))
                return

    def _maybe_generate_waste(self):
        cell_agents = self.model.grid.get_cell_list_contents([self.pos])
        crowd_size = len(cell_agents)
        adjusted_prob = min(0.40, self.waste_prob + (crowd_size - 1) * 0.05)

        if random.random() < adjusted_prob:
            x, y = self.pos
            self.model.street_waste[x][y] += 1
            self.model.total_waste_generated += 1

class CleaningRobot(Agent):
    
    def __init__(self, model, strategy="nearest"):
        super().__init__(model)
        self.strategy = strategy
        self.carrying = 0
        self.capacity = 5        # max waste units it can carry
        self.waste_collected = 0

    def step(self):
        times = 2 if not self.model.is_day else 1
        for _ in range(times):
            self._act()

    def _act(self):
        x, y = self.pos
        if self.carrying >= self.capacity:
            self._deposit()
            return

        if self.model.street_waste[x][y] > 0:
            picked = min(self.model.street_waste[x][y],
                        self.capacity - self.carrying)
            self.model.street_waste[x][y] -= picked
            self.carrying += picked
            self.waste_collected += picked
            self.model.total_waste_collected += picked
            return

        self._move()

    def _move(self):
        if self.strategy == "nearest":
            self._move_bfs()
        else:
            self._move_random()

    def _move_bfs(self):
        x, y = self.pos
        sw = self.model.street_waste
        next_step = bfs(
            self.model.city_grid, (x, y),
            lambda cx, cy: sw[cx][cy] > 0,
            self.model.grid.width, self.model.grid.height
        )
        if next_step:
            self.model.grid.move_agent(self, next_step)
        else:
            self._move_random()

    def _move_random(self):
        x, y = self.pos
        candidates = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        random.shuffle(candidates)
        for nx, ny in candidates:
            if is_walkable(self.model.city_grid, nx, ny,
                           self.model.grid.width, self.model.grid.height):
                self.model.grid.move_agent(self, (nx, ny))
                return

    def _deposit(self):
        x, y = self.pos
        next_step = bfs(
            self.model.city_grid, (x, y),
            lambda cx, cy: any(
                isinstance(a, DustBin) and not a.is_full()
                for a in self.model.grid.get_cell_list_contents([(cx, cy)])
            ),
            self.model.grid.width, self.model.grid.height
        )

        if next_step:
            self.model.grid.move_agent(self, next_step)
            nx, ny = next_step
            for agent in self.model.grid.get_cell_list_contents([(nx, ny)]):
                if isinstance(agent, DustBin) and not agent.is_full():
                    space = agent.capacity - agent.waste_level
                    deposited = min(self.carrying, space)
                    agent.receive_waste(deposited)
                    self.carrying -= deposited
                    break
        else:
            disposal = self.model.disposal_cells
            if disposal:
                target = random.choice(disposal)
                next_step = bfs(
                    self.model.city_grid, (x, y),
                    lambda cx, cy: (cx, cy) == target,
                    self.model.grid.width, self.model.grid.height
                )
                if next_step:
                    self.model.grid.move_agent(self, next_step)
                    if self.pos == target:
                        self.carrying = 0

class DustBin(Agent):

    def __init__(self, model, capacity=10):
        super().__init__(model)
        self.capacity = capacity
        self.waste_level = 0

    def is_full(self):
        return self.waste_level >= self.capacity

    def receive_waste(self, amount):
        self.waste_level += amount

    def step(self):
        if self.waste_level > self.capacity:
            overflow = self.waste_level - self.capacity
            self.waste_level = self.capacity
            x, y = self.pos
            self.model.street_waste[x][y] += overflow
            self.model.total_waste_generated += overflow
            self.model.overflow_events += 1

class DustTransporter(Agent):

    def __init__(self, model, frequency=10):
        super().__init__(model)
        self.frequency = frequency
        self.carrying = 0
        self.trips = 0
        self.state = "idle"       
        self.target_pos = None 

    def step(self):
        if self.state == "idle":
            if self.model.steps % self.frequency == 0:
                self._start_collection()

        elif self.state == "going_to_bin":
            self._move_to_bin()

        elif self.state == "going_to_disposal":
            self._move_to_disposal()

    def _start_collection(self):
        bins = [
            a for a in self.model.agents
            if isinstance(a, DustBin) and a.waste_level > 0
        ]
        if not bins:
            return
        target_bin = max(bins, key=lambda b: b.waste_level)
        self.target_pos = target_bin.pos
        self.state = "going_to_bin"

    def _move_to_bin(self):
        x, y = self.pos

        if (x, y) == self.target_pos:
            cell_contents = self.model.grid.get_cell_list_contents([self.target_pos])
            for agent in cell_contents:
                if isinstance(agent, DustBin):
                    collected = agent.waste_level
                    if collected > 0:
                        self.carrying += collected
                        agent.waste_level = 0
                        self.trips += 1
                        self.model.transporter_trips += 1
                        self.model.total_waste_transported += collected
                    break

            if self.model.disposal_cells:
                tx, ty = self.pos
                self.target_pos = min(
                    self.model.disposal_cells,
                    key=lambda d: abs(d[0]-tx) + abs(d[1]-ty)
                )
                self.state = "going_to_disposal"
            else:
                self.state = "idle"
            return

        next_step = bfs(
            self.model.city_grid, (x, y),
            lambda cx, cy: (cx, cy) == self.target_pos,
            self.model.grid.width, self.model.grid.height
        )
        if next_step:
            self.model.grid.move_agent(self, next_step)
        else:
            self.state = "idle"
            self.target_pos = None

    def _move_to_disposal(self):
        x, y = self.pos
        if (x, y) == self.target_pos:
            self.carrying = 0
            self.state = "idle"
            self.target_pos = None
            return

        next_step = bfs(
            self.model.city_grid, (x, y),
            lambda cx, cy: (cx, cy) == self.target_pos,
            self.model.grid.width, self.model.grid.height
        )
        if next_step:
            self.model.grid.move_agent(self, next_step)
        else:
            self.state = "idle"
            self.target_pos = None