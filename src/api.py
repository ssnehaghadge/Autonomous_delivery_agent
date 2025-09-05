"""
API module for the autonomous delivery agent.
Provides a clean interface for interacting with the delivery system.
"""

from typing import Dict, List, Any, Optional
from .environment import Grid, TerrainType, MovingObstacle
from .agent import DeliveryAgent
from .planners import BFSPlanner, UCSPlanner, AStarPlanner, SimulatedAnnealingPlanner

class DeliveryAPI:
    """API for interacting with the autonomous delivery system."""
    
    def __init__(self):
        """Initialize the API."""
        self.grid = None
        self.agent = None
        self.current_algorithm = "a_star"
        
    def create_grid(self, width: int, height: int) -> Dict[str, Any]:
        """
        Create a new grid environment.
        
        Args:
            width: Width of the grid
            height: Height of the grid
            
        Returns:
            Dictionary with operation status and grid details
        """
        try:
            self.grid = Grid(width, height)
            return {
                "status": "success",
                "message": f"Grid created with size {width}x{height}",
                "width": width,
                "height": height
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create grid: {str(e)}"
            }
    
    def load_grid(self, filename: str) -> Dict[str, Any]:
        """
        Load a grid from a file.
        
        Args:
            filename: Path to the grid file
            
        Returns:
            Dictionary with operation status and grid details
        """
        try:
            self.grid = Grid(1, 1)  # Temporary grid
            self.grid.load_from_file(filename)
            
            return {
                "status": "success",
                "message": f"Grid loaded from {filename}",
                "width": self.grid.width,
                "height": self.grid.height,
                "obstacles": self._count_obstacles(),
                "moving_obstacles": len(self.grid.moving_obstacles)
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to load grid: {str(e)}"
            }
    
    def save_grid(self, filename: str) -> Dict[str, Any]:
        """
        Save the current grid to a file.
        
        Args:
            filename: Path to save the grid file
            
        Returns:
            Dictionary with operation status
        """
        try:
            if self.grid is None:
                return {
                    "status": "error",
                    "message": "No grid to save"
                }
                
            self.grid.save_to_file(filename)
            return {
                "status": "success",
                "message": f"Grid saved to {filename}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to save grid: {str(e)}"
            }
    
    def add_obstacle(self, x: int, y: int) -> Dict[str, Any]:
        """
        Add an obstacle to the grid.
        
        Args:
            x: x-coordinate
            y: y-coordinate
            
        Returns:
            Dictionary with operation status
        """
        try:
            if self.grid is None:
                return {
                    "status": "error",
                    "message": "No grid created"
                }
                
            self.grid.add_obstacle(x, y)
            return {
                "status": "success",
                "message": f"Obstacle added at ({x}, {y})"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to add obstacle: {str(e)}"
            }
    
    def set_terrain(self, x: int, y: int, terrain_type: str) -> Dict[str, Any]:
        """
        Set terrain type for a cell.
        
        Args:
            x: x-coordinate
            y: y-coordinate
            terrain_type: Type of terrain ("road", "grass", "mud", "water")
            
        Returns:
            Dictionary with operation status
        """
        try:
            if self.grid is None:
                return {
                    "status": "error",
                    "message": "No grid created"
                }
                
            # Map string to TerrainType
            terrain_map = {
                "road": TerrainType.ROAD,
                "grass": TerrainType.GRASS,
                "mud": TerrainType.MUD,
                "water": TerrainType.WATER
            }
            
            if terrain_type not in terrain_map:
                return {
                    "status": "error",
                    "message": f"Invalid terrain type: {terrain_type}. Must be one of {list(terrain_map.keys())}"
                }
                
            self.grid.set_terrain(x, y, terrain_map[terrain_type])
            return {
                "status": "success",
                "message": f"Terrain at ({x}, {y}) set to {terrain_type}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to set terrain: {str(e)}"
            }
    
    def add_moving_obstacle(self, x: int, y: int, path: List[List[int]], speed: int = 1) -> Dict[str, Any]:
        """
        Add a moving obstacle to the grid.
        
        Args:
            x: Initial x-coordinate
            y: Initial y-coordinate
            path: List of [x, y] coordinates defining the path
            speed: Number of time steps between moves
            
        Returns:
            Dictionary with operation status
        """
        try:
            if self.grid is None:
                return {
                    "status": "error",
                    "message": "No grid created"
                }
                
            # Convert path to list of tuples
            path_tuples = [(point[0], point[1]) for point in path]
            obstacle = MovingObstacle(x, y, path_tuples, speed)
            self.grid.add_moving_obstacle(obstacle)
            
            return {
                "status": "success",
                "message": f"Moving obstacle added at ({x}, {y}) with path of length {len(path)}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to add moving obstacle: {str(e)}"
            }
    
    def create_agent(self, x: int, y: int, fuel: int = 100) -> Dict[str, Any]:
        """
        Create a delivery agent.
        
        Args:
            x: Starting x-coordinate
            y: Starting y-coordinate
            fuel: Initial fuel amount
            
        Returns:
            Dictionary with operation status
        """
        try:
            if self.grid is None:
                return {
                    "status": "error",
                    "message": "No grid created"
                }
                
            self.agent = DeliveryAgent(self.grid, x, y, fuel)
            return {
                "status": "success",
                "message": f"Agent created at ({x}, {y}) with {fuel} fuel"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create agent: {str(e)}"
            }
    
    def add_package(self, x: int, y: int) -> Dict[str, Any]:
        """
        Add a package for delivery.
        
        Args:
            x: x-coordinate of package
            y: y-coordinate of package
            
        Returns:
            Dictionary with operation status
        """
        try:
            if self.agent is None:
                return {
                    "status": "error",
                    "message": "No agent created"
                }
                
            self.agent.add_package(x, y)
            return {
                "status": "success",
                "message": f"Package added at ({x}, {y})"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to add package: {str(e)}"
            }
    
    def add_destination(self, x: int, y: int) -> Dict[str, Any]:
        """
        Add a delivery destination.
        
        Args:
            x: x-coordinate of destination
            y: y-coordinate of destination
            
        Returns:
            Dictionary with operation status
        """
        try:
            if self.agent is None:
                return {
                    "status": "error",
                    "message": "No agent created"
                }
                
            self.agent.add_destination(x, y)
            return {
                "status": "success",
                "message": f"Destination added at ({x}, {y})"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to add destination: {str(e)}"
            }
    
    def set_algorithm(self, algorithm: str) -> Dict[str, Any]:
        """
        Set the path planning algorithm.
        
        Args:
            algorithm: Algorithm to use ("bfs", "ucs", "a_star", "sa")
            
        Returns:
            Dictionary with operation status
        """
        try:
            valid_algorithms = ["bfs", "ucs", "a_star", "sa"]
            if algorithm not in valid_algorithms:
                return {
                    "status": "error",
                    "message": f"Invalid algorithm: {algorithm}. Must be one of {valid_algorithms}"
                }
                
            self.current_algorithm = algorithm
            return {
                "status": "success",
                "message": f"Algorithm set to {algorithm}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to set algorithm: {str(e)}"
            }
    
    def plan_path(self, start_x: int, start_y: int, goal_x: int, goal_y: int, 
                 algorithm: Optional[str] = None) -> Dict[str, Any]:
        """
        Plan a path from start to goal.
        
        Args:
            start_x: Start x-coordinate
            start_y: Start y-coordinate
            goal_x: Goal x-coordinate
            goal_y: Goal y-coordinate
            algorithm: Algorithm to use (optional, uses current algorithm if not specified)
            
        Returns:
            Dictionary with operation status and path details
        """
        try:
            if self.grid is None:
                return {
                    "status": "error",
                    "message": "No grid created"
                }
                
            algo = algorithm or self.current_algorithm
            
            if algo == "bfs":
                planner = BFSPlanner(self.grid)
            elif algo == "ucs":
                planner = UCSPlanner(self.grid)
            elif algo == "a_star":
                planner = AStarPlanner(self.grid)
            elif algo == "sa":
                planner = SimulatedAnnealingPlanner(self.grid)
            else:
                return {
                    "status": "error",
                    "message": f"Invalid algorithm: {algo}"
                }
                
            result = planner.plan(start_x, start_y, goal_x, goal_y)
            
            if result is None:
                return {
                    "status": "error",
                    "message": "No path found"
                }
                
            path = result.get_path()
            return {
                "status": "success",
                "message": f"Path found with cost {result.cost}",
                "path": path,
                "cost": result.cost,
                "length": len(path),
                "algorithm": algo
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to plan path: {str(e)}"
            }
    
    def execute_delivery(self, algorithm: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute the complete package delivery mission.
        
        Args:
            algorithm: Algorithm to use (optional, uses current algorithm if not specified)
            
        Returns:
            Dictionary with operation status and delivery details
        """
        try:
            if self.agent is None:
                return {
                    "status": "error",
                    "message": "No agent created"
                }
                
            algo = algorithm or self.current_algorithm
            success = self.agent.deliver_packages(algo)
            
            if success:
                return {
                    "status": "success",
                    "message": "Delivery completed successfully",
                    "fuel_remaining": self.agent.fuel,
                    "packages_delivered": self.agent.delivered_packages
                }
            else:
                return {
                    "status": "error",
                    "message": "Delivery failed",
                    "fuel_remaining": self.agent.fuel,
                    "packages_remaining": len(self.agent.packages)
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to execute delivery: {str(e)}"
            }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """
        Get the current status of the agent.
        
        Returns:
            Dictionary with agent status
        """
        try:
            if self.agent is None:
                return {
                    "status": "error",
                    "message": "No agent created"
                }
                
            return {
                "status": "success",
                "position": (self.agent.x, self.agent.y),
                "fuel": self.agent.fuel,
                "packages_remaining": len(self.agent.packages),
                "destinations_remaining": len(self.agent.destinations),
                "path_length": len(self.agent.path) if hasattr(self.agent, 'path') else 0,
                "current_step": self.agent.current_step if hasattr(self.agent, 'current_step') else 0
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to get agent status: {str(e)}"
            }
    
    def get_grid_info(self) -> Dict[str, Any]:
        """
        Get information about the current grid.
        
        Returns:
            Dictionary with grid information
        """
        try:
            if self.grid is None:
                return {
                    "status": "error",
                    "message": "No grid created"
                }
                
            return {
                "status": "success",
                "width": self.grid.width,
                "height": self.grid.height,
                "obstacles": self._count_obstacles(),
                "moving_obstacles": len(self.grid.moving_obstacles),
                "terrain_types": self._get_terrain_distribution()
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to get grid info: {str(e)}"
            }
    
    def _count_obstacles(self) -> int:
        """Count the number of static obstacles in the grid."""
        if self.grid is None:
            return 0
            
        count = 0
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                if self.grid.grid[y, x] == 1:  # OBSTACLE value
                    count += 1
        return count
    
    def _get_terrain_distribution(self) -> Dict[str, int]:
        """Get the distribution of terrain types in the grid."""
        if self.grid is None:
            return {}
            
        distribution = {
            "road": 0,
            "grass": 0,
            "mud": 0,
            "water": 0
        }
        
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                terrain_value = self.grid.terrain[y, x]
                if terrain_value == 1:
                    distribution["road"] += 1
                elif terrain_value == 3:
                    distribution["grass"] += 1
                elif terrain_value == 5:
                    distribution["mud"] += 1
                elif terrain_value == 10:
                    distribution["water"] += 1
                    
        return distribution

# Global API instance
api = DeliveryAPI()

# Convenience functions for easy access to the API
def create_grid(width: int, height: int) -> Dict[str, Any]:
    """Create a new grid environment."""
    return api.create_grid(width, height)

def load_grid(filename: str) -> Dict[str, Any]:
    """Load a grid from a file."""
    return api.load_grid(filename)

def save_grid(filename: str) -> Dict[str, Any]:
    """Save the current grid to a file."""
    return api.save_grid(filename)

def add_obstacle(x: int, y: int) -> Dict[str, Any]:
    """Add an obstacle to the grid."""
    return api.add_obstacle(x, y)

def set_terrain(x: int, y: int, terrain_type: str) -> Dict[str, Any]:
    """Set terrain type for a cell."""
    return api.set_terrain(x, y, terrain_type)

def add_moving_obstacle(x: int, y: int, path: List[List[int]], speed: int = 1) -> Dict[str, Any]:
    """Add a moving obstacle to the grid."""
    return api.add_moving_obstacle(x, y, path, speed)

def create_agent(x: int, y: int, fuel: int = 100) -> Dict[str, Any]:
    """Create a delivery agent."""
    return api.create_agent(x, y, fuel)

def add_package(x: int, y: int) -> Dict[str, Any]:
    """Add a package for delivery."""
    return api.add_package(x, y)

def add_destination(x: int, y: int) -> Dict[str, Any]:
    """Add a delivery destination."""
    return api.add_destination(x, y)

def set_algorithm(algorithm: str) -> Dict[str, Any]:
    """Set the path planning algorithm."""
    return api.set_algorithm(algorithm)

def plan_path(start_x: int, start_y: int, goal_x: int, goal_y: int, 
              algorithm: Optional[str] = None) -> Dict[str, Any]:
    """Plan a path from start to goal."""
    return api.plan_path(start_x, start_y, goal_x, goal_y, algorithm)

def execute_delivery(algorithm: Optional[str] = None) -> Dict[str, Any]:
    """Execute the complete package delivery mission."""
    return api.execute_delivery(algorithm)

def get_agent_status() -> Dict[str, Any]:
    """Get the current status of the agent."""
    return api.get_agent_status()

def get_grid_info() -> Dict[str, Any]:
    """Get information about the current grid."""
    return api.get_grid_info()