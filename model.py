import random
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from city_generator import (
    generate_city, get_street_cells, get_disposal_cells,
    BIN_SPOT
)
from agents import (
    LocalHuman, Tourist, CleaningRobot, DustBin, DustTransporter
)

def compute_street_waste(model):

    return sum(
        model.street_waste[x][y]
        for x in range(model.grid.width)
        for y in range(model.grid.height)
    )

def compute_overflowing_bins(model):
    
    return sum(
        1 for a in model.agents
        if isinstance(a, DustBin) and a.is_full()
    )

def compute_robot_efficiency(model):
    
    if model.total_waste_generated == 0:
        return 0.0
    return round(model.total_waste_collected / model.total_waste_generated, 3)

def compute_district_waste(model):
    
    w  = model.grid.width
    h  = model.grid.height
    hw = w // 2   
    hh = h // 2   

    
    q1 = sum(
        model.street_waste[x][y]
        for x in range(0, hw)
        for y in range(0, hh)
    )
    
    q2 = sum(
        model.street_waste[x][y]
        for x in range(hw, w)
        for y in range(0, hh)
    )
    
    q3 = sum(
        model.street_waste[x][y]
        for x in range(0, hw)
        for y in range(hh, h)
    )
    
    q4 = sum(
        model.street_waste[x][y]
        for x in range(hw, w)
        for y in range(hh, h)
    )

    
    return round((q1 + q2 + q3 + q4) / 4, 2)

def compute_transporter_workload(model):
    return model.transporter_trips

class CityWasteModel(Model):
    def __init__(self, config):
        super().__init__(seed=42)
        random.seed(42)
        self.config = config
        self.grid = MultiGrid(
            config["grid_width"],
            config["grid_height"],
            torus=False
        )

        
        self.city_grid = generate_city(
            config["grid_width"],
            config["grid_height"],
            config["num_bins"],
            config["num_buildings"]
        )

        self.street_waste = [
            [0] * config["grid_height"]
            for _ in range(config["grid_width"])
        ]

        self.total_waste_generated   = 0 
        self.total_waste_collected   = 0  
        self.total_waste_transported = 0  
        self.overflow_events         = 0  
        self.transporter_trips       = 0  
        
        self.is_day = True
        
        self.street_cells = get_street_cells(
            self.city_grid, config["grid_width"], config["grid_height"]
        )
        self.disposal_cells = get_disposal_cells(
            self.city_grid, config["grid_width"], config["grid_height"]
        )

        self._place_agents()
        self.datacollector = DataCollector(
            model_reporters={
                "StreetWaste":         compute_street_waste,
                "OverflowingBins":     compute_overflowing_bins,
                "RobotEfficiency":     compute_robot_efficiency,
                "DistrictWaste":       compute_district_waste,
                "TransporterWorkload": compute_transporter_workload,
            }
        )

    def _place_agents(self):
       
        cfg = self.config
        bin_cells = [
            (x, y)
            for x in range(cfg["grid_width"])
            for y in range(cfg["grid_height"])
            if self.city_grid[x][y] == BIN_SPOT
        ]
        for pos in bin_cells:
            b = DustBin(self, cfg["bin_capacity"])
            self.grid.place_agent(b, pos)

        for _ in range(cfg["num_humans"]):
            if len(self.street_cells) < 2:
                break
            home = random.choice(self.street_cells)
            work = random.choice(self.street_cells)
            a = LocalHuman(self, home, work)
            self.grid.place_agent(a, home)

        for _ in range(cfg["num_tourists"]):
            if not self.street_cells:
                break
            pos = random.choice(self.street_cells)
            a = Tourist(self)
            self.grid.place_agent(a, pos)

        for _ in range(cfg["num_robots"]):
            if not self.street_cells:
                break
            pos = random.choice(self.street_cells)
            a = CleaningRobot(self, cfg["robot_strategy"])
            self.grid.place_agent(a, pos)

        for _ in range(cfg["num_transporters"]):
            if not self.street_cells:
                break
            pos = random.choice(self.street_cells)
            a = DustTransporter(self, cfg["transporter_frequency"])
            self.grid.place_agent(a, pos)

    def step(self):
        step_in_day = self.steps % 24
        self.is_day = step_in_day < 12
        self.datacollector.collect(self)
        self.agents.shuffle_do("step")