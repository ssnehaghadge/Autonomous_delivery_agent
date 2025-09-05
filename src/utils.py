"""
Utility functions for the autonomous delivery agent project.
"""

import time
import json
import random
from typing import Dict, Any, List
from .environment import Grid, TerrainType, MovingObstacle
from .agent import DeliveryAgent

def create_test_map(size: str) -> Grid:
    """
    Create a test map of the specified size.
    
    Args:
        size: Size of the map ("small", "medium", "large", or "dynamic")
        
    Returns:
        Grid object with the test map
    """
    if size == "small":
        grid = Grid(10, 10)
        # Add some obstacles
        for i in range(3, 7):
            grid.add_obstacle(i, 5)
        # Add different terrain
        for i in range(10):
            for j in range(3):
                grid.set_terrain(i, j, TerrainType.GRASS)
        for i in range(10):
            for j in range(7, 10):
                grid.set_terrain(i, j, TerrainType.MUD)
                
    elif size == "medium":
        grid = Grid(20, 20)
        # Add obstacles in a cross pattern
        for i in range(5, 15):
            grid.add_obstacle(i, 10)
        for j in range(5, 15):
            grid.add_obstacle(10, j)
        # Add different terrain
        for i in range(20):
            for j in range(5):
                grid.set_terrain(i, j, TerrainType.GRASS)
        for i in range(20):
            for j in range(15, 20):
                grid.set_terrain(i, j, TerrainType.MUD)
        for i in range(5):
            for j in range(20):
                grid.set_terrain(i, j, TerrainType.WATER)
                
    elif size == "large":
        grid = Grid(50, 50)
        # Add random obstacles
        for _ in range(100):
            x = random.randint(0, 49)
            y = random.randint(0, 49)
            grid.add_obstacle(x, y)
        # Add different terrain in regions
        for i in range(50):
            for j in range(10):
                grid.set_terrain(i, j, TerrainType.GRASS)
        for i in range(50):
            for j in range(40, 50):
                grid.set_terrain(i, j, TerrainType.MUD)
        for i in range(10):
            for j in range(50):
                grid.set_terrain(i, j, TerrainType.WATER)
                
    elif size == "dynamic":
        grid = Grid(15, 15)
        # Add static obstacles
        for i in range(5, 10):
            grid.add_obstacle(i, 7)
        # Add a moving obstacle
        moving_path = [(3, 3), (3, 4), (3, 5), (4, 5), (5, 5), (5, 4), (5, 3), (4, 3)]
        moving_obstacle = MovingObstacle(3, 3, moving_path, speed=2)
        grid.add_moving_obstacle(moving_obstacle)
        # Add different terrain
        for i in range(15):
            for j in range(5):
                grid.set_terrain(i, j, TerrainType.GRASS)
        
    else:
        raise ValueError(f"Unknown map size: {size}")
        
    return grid

def run_experiment(map_size: str, algorithm: str) -> Dict[str, Any]:
    """
    Run a delivery experiment with the specified map and algorithm.
    
    Args:
        map_size: Size of the map ("small", "medium", "large", or "dynamic")
        algorithm: Planning algorithm to use ("bfs", "ucs", "a_star", "sa")
        
    Returns:
        Dictionary with experiment results
    """
    grid = create_test_map(map_size)
    agent = DeliveryAgent(grid, 0, 0, fuel=1000)
    
    # Add package and destination based on map size
    if map_size == "small":
        agent.add_package(9, 9)
        agent.add_destination(5, 2)
    elif map_size == "medium":
        agent.add_package(19, 19)
        agent.add_destination(10, 5)
    elif map_size == "large":
        agent.add_package(45, 45)
        agent.add_destination(10, 10)
    elif map_size == "dynamic":
        agent.add_package(12, 12)
        agent.add_destination(7, 3)
    
    start_time = time.time()
    success = agent.deliver_packages(algorithm)
    end_time = time.time()
    
    return {
        "success": success,
        "path_cost": agent.path[-1].cost if success and hasattr(agent, 'path') and agent.path else float('inf'),
        "fuel_remaining": agent.fuel,
        "time_taken": end_time - start_time,
        "path_length": len(agent.path) if success and hasattr(agent, 'path') and agent.path else 0,
        "algorithm": algorithm,
        "map_size": map_size
    }

def save_results(results: List[Dict[str, Any]], filename: str):
    """
    Save experiment results to a JSON file.
    
    Args:
        results: List of experiment results
        filename: Output filename
    """
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)

def load_results(filename: str) -> List[Dict[str, Any]]:
    """
    Load experiment results from a JSON file.
    
    Args:
        filename: Input filename
        
    Returns:
        List of experiment results
    """
    with open(filename, 'r') as f:
        return json.load(f)