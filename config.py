SCENARIO_1A = {
    "name": "Few Bins (5)",
    "grid_width": 30,
    "grid_height": 30,
    "num_humans": 40,
    "num_tourists": 10,       
    "num_robots": 3,
    "num_transporters": 2,
    "num_bins": 5,           
    "bin_capacity": 10,
    "robot_strategy": "nearest",
    "transporter_frequency": 10,  
    "num_buildings": 12,      
    "num_steps": 200,
}

SCENARIO_1B = {
    "name": "Many Bins (15)",
    "grid_width": 30,
    "grid_height": 30,
    "num_humans": 40,
    "num_tourists": 10,       
    "num_robots": 3,
    "num_transporters": 2,
    "num_bins": 15,           
    "bin_capacity": 10,
    "robot_strategy": "nearest",
    "transporter_frequency": 10,  
    "num_buildings": 12,      
    "num_steps": 200,
}

SCENARIO_2A = {
    "name": "Random Robot Patrol",
    "grid_width": 30,
    "grid_height": 30,
    "num_humans": 40,
    "num_tourists": 10,       
    "num_robots": 3,
    "num_transporters": 2,
    "num_bins": 10,           
    "bin_capacity": 10,
    "robot_strategy": "random",
    "transporter_frequency": 10,  
    "num_buildings": 12,      
    "num_steps": 200,
}

SCENARIO_2B = {
    "name": "Nearest-Waste BFS Strategy",
    "grid_width": 30,
    "grid_height": 30,
    "num_humans": 40,
    "num_tourists": 10,       
    "num_robots": 3,
    "num_transporters": 2,
    "num_bins": 10,           
    "bin_capacity": 10,
    "robot_strategy": "nearest",
    "transporter_frequency": 10,  
    "num_buildings": 12,      
    "num_steps": 200,
}

SCENARIO_3A = {
    "name": "Low Tourist Density (10)",
    "grid_width": 30,
    "grid_height": 30,
    "num_humans": 40,
    "num_tourists": 10,       
    "num_robots": 3,
    "num_transporters": 2,
    "num_bins": 10,           
    "bin_capacity": 10,
    "robot_strategy": "nearest",
    "transporter_frequency": 10,  
    "num_buildings": 12,      
    "num_steps": 200,
}

SCENARIO_3B = {
    "name": "High Tourist Density (30)",
    "grid_width": 30,
    "grid_height": 30,
    "num_humans": 40,
    "num_tourists": 30,       
    "num_robots": 3,
    "num_transporters": 2,
    "num_bins": 10,           
    "bin_capacity": 10,
    "robot_strategy": "nearest",
    "transporter_frequency": 10,  
    "num_buildings": 12,      
    "num_steps": 200,
}



SCENARIO_4A = {
    "name": "Rare Transporters (every 20 steps)",
    "grid_width": 30,
    "grid_height": 30,
    "num_humans": 40,
    "num_tourists": 10,       
    "num_robots": 3,
    "num_transporters": 2,
    "num_bins": 12,           
    "bin_capacity": 5,
    "robot_strategy": "nearest",
    "transporter_frequency": 20,  
    "num_buildings": 12,      
    "num_steps": 200,
}

SCENARIO_4B = {
    "name": "Frequent Transporters (every 3 steps)",
    "grid_width": 30,
    "grid_height": 30,
    "num_humans": 40,
    "num_tourists": 10,       
    "num_robots": 3,
    "num_transporters": 2,
    "num_bins": 12,           
    "bin_capacity": 5,
    "robot_strategy": "nearest",
    "transporter_frequency": 3,  
    "num_buildings": 12,      
    "num_steps": 200,
}

SCENARIO_5A = {
    "name": "Many Streets (5 buildings)",
    "grid_width": 30,
    "grid_height": 30,
    "num_humans": 40,
    "num_tourists": 10,       
    "num_robots": 3,
    "num_transporters": 2,
    "num_bins": 10,           
    "bin_capacity": 10,
    "robot_strategy": "nearest",
    "transporter_frequency": 10,  
    "num_buildings": 5,      
    "num_steps": 200,
}

SCENARIO_5B = {
    "name": "Many Buildings (40 buildings)",
    "grid_width": 30,
    "grid_height": 30,
    "num_humans": 40,
    "num_tourists": 10,       
    "num_robots": 3,
    "num_transporters": 2,
    "num_bins": 10,           
    "bin_capacity": 10,
    "robot_strategy": "nearest",
    "transporter_frequency": 10,  
    "num_buildings": 40,      
    "num_steps": 200,
}

ALL_SCENARIOS = [
    SCENARIO_1A, SCENARIO_1B,
    SCENARIO_2A, SCENARIO_2B,
    SCENARIO_3A, SCENARIO_3B,
    SCENARIO_4A, SCENARIO_4B,
    SCENARIO_5A, SCENARIO_5B,
]