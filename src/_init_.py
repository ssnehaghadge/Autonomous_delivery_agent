"""
Source code for the Autonomous Delivery Agent.

This package contains all the core functionality for the delivery agent system.
"""

# Import key classes and functions to make them easily accessible
from .environment import Grid, TerrainType, MovingObstacle, Direction
from .agent import DeliveryAgent
from .planners import BFSPlanner, UCSPlanner, AStarPlanner, SimulatedAnnealingPlanner
from .utils import create_test_map, run_experiment, save_results, load_results
from .api import (
    create_grid, load_grid, save_grid, add_obstacle, set_terrain,
    add_moving_obstacle, create_agent, add_package, add_destination,
    set_algorithm, plan_path, execute_delivery, get_agent_status, get_grid_info
)

# Define what gets imported with "from src import *"
__all__ = [
    # Environment classes
    'Grid', 'TerrainType', 'MovingObstacle', 'Direction',
    
    # Agent class
    'DeliveryAgent',
    
    # Planner classes
    'BFSPlanner', 'UCSPlanner', 'AStarPlanner', 'SimulatedAnnealingPlanner',
    
    # Utility functions
    'create_test_map', 'run_experiment', 'save_results', 'load_results',
    
    # API functions
    'create_grid', 'load_grid', 'save_grid', 'add_obstacle', 'set_terrain',
    'add_moving_obstacle', 'create_agent', 'add_package', 'add_destination',
    'set_algorithm', 'plan_path', 'execute_delivery', 'get_agent_status', 'get_grid_info'
]

# Package metadata
__version__ = "1.0.0"