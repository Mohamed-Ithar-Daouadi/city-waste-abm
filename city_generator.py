import random

STREET      = 0
BUILDING    = 1
PUBLIC      = 2
BIN_SPOT    = 3
DISPOSAL    = 4

def generate_city(width, height, num_bins, num_buildings=12):
    grid = [[STREET for _ in range(height)] for _ in range(width)]

    for _ in range(num_buildings):
        bx = random.randint(3, width - 8)
        by = random.randint(3, height - 8)
        bw = random.randint(3, 6)
        bh = random.randint(3, 6)
        for x in range(bx, min(bx + bw, width - 2)):
            for y in range(by, min(by + bh, height - 2)):
                grid[x][y] = BUILDING

    for _ in range(4):
        px = random.randint(2, width - 6)
        py = random.randint(2, height - 6)
        for x in range(px, min(px + 3, width - 1)):
            for y in range(py, min(py + 3, height - 1)):
                if grid[x][y] == STREET:
                    grid[x][y] = PUBLIC

    for x in range(width):
        grid[x][0] = DISPOSAL
        grid[x][height - 1] = DISPOSAL

    bins_placed = 0
    attempts = 0
    while bins_placed < num_bins and attempts < 1000:
        bx = random.randint(1, width - 2)
        by = random.randint(1, height - 2)
        if grid[bx][by] == STREET:
            grid[bx][by] = BIN_SPOT
            bins_placed += 1
        attempts += 1

    return grid


def get_street_cells(grid, width, height):
    return [
        (x, y)
        for x in range(width)
        for y in range(height)
        if grid[x][y] in (STREET, PUBLIC, BIN_SPOT)
    ]


def get_disposal_cells(grid, width, height):
    return [
        (x, y)
        for x in range(width)
        for y in range(height)
        if grid[x][y] == DISPOSAL
    ]


def is_walkable(grid, x, y, width, height):

    if x < 0 or y < 0 or x >= width or y >= height:
        return False
    return grid[x][y] != BUILDING