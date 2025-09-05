"""
Autonomous delivery agent implementation.
Handles package delivery, path planning, and execution.
"""

from typing import List, Tuple, Optional, Dict
from .environment import Grid
from .planners import PathPlanner, BFSPlanner, UCSPlanner, AStarPlanner, SimulatedAnnealingPlanner

class DeliveryAgent:
    """Autonomous delivery agent class."""
    
    def __init__(self, grid: Grid, start_x: int, start_y: int, fuel: int = 100):
        """
        Initialize the delivery agent.
        
        Args:
            grid: Grid environment
            start_x: Starting x-coordinate
            start_y: Starting y-coordinate
            fuel: Initial fuel amount
        """
        self.grid = grid
        self.x = start_x
        self.y = start_y
        self.fuel = fuel
        self.path = []  # Initialize empty path
        self.current_step = 0
        self.packages = []  # List of (x, y) package locations
        self.destinations = []  # List of (x, y) destination locations
        self.delivered_packages = 0
        
    def add_package(self, x: int, y: int):
        """
        Add a package to be picked up.
        
        Args:
            x: x-coordinate of package
            y: y-coordinate of package
        """
        self.packages.append((x, y))
        
    def add_destination(self, x: int, y: int):
        """
        Add a delivery destination.
        
        Args:
            x: x-coordinate of destination
            y: y-coordinate of destination
        """
        self.destinations.append((x, y))
        
    def plan_path_to(self, goal_x: int, goal_y: int, algorithm: str = "a_star") -> bool:
        """
        Plan a path to the goal using the specified algorithm.
        
        Args:
            goal_x: Goal x-coordinate
            goal_y: Goal y-coordinate
            algorithm: Planning algorithm to use ("bfs", "ucs", "a_star", "sa")
            
        Returns:
            True if a path was found, False otherwise
        """
        if algorithm == "bfs":
            planner = BFSPlanner(self.grid)
        elif algorithm == "ucs":
            planner = UCSPlanner(self.grid)
        elif algorithm == "a_star":
            planner = AStarPlanner(self.grid)
        elif algorithm == "sa":
            planner = SimulatedAnnealingPlanner(self.grid)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
            
        result_node = planner.plan(self.x, self.y, goal_x, goal_y, self.current_step)
            
        if result_node:
            self.path = result_node.get_path()
            # Remove the first element (current position)
            if self.path:
                self.path = self.path[1:]
            self.current_step = 0
            return True
        return False
        
    def execute_step(self) -> bool:
        """
        Execute one step along the planned path.
        
        Returns:
            True if movement was successful, False if no more steps
        """
        if self.current_step < len(self.path):
            next_x, next_y = self.path[self.current_step]
            self.x, self.y = next_x, next_y
            self.current_step += 1
            
            # Consume fuel based on terrain cost
            cell_cost = self.grid.get_cost(self.x, self.y)
            self.fuel -= cell_cost
            
            # Update moving obstacles in the grid
            self.grid.update_moving_obstacles()
            
            # Check if we picked up a package
            if (self.x, self.y) in self.packages:
                self.packages.remove((self.x, self.y))
                print(f"Picked up package at ({self.x}, {self.y})")
                
            # Check if we delivered a package
            if (self.x, self.y) in self.destinations and len(self.packages) < self.delivered_packages:
                self.delivered_packages = len(self.packages)
                print(f"Delivered package at ({self.x}, {self.y})")
            
            return True
        return False
        
    def has_reached_goal(self, goal_x: int, goal_y: int) -> bool:
        """
        Check if the agent has reached the goal.
        
        Args:
            goal_x: Goal x-coordinate
            goal_y: Goal y-coordinate
            
        Returns:
            True if agent is at the goal position
        """
        return self.x == goal_x and self.y == goal_y
        
    def deliver_packages(self, algorithm: str = "a_star") -> bool:
        """
        Execute the complete package delivery mission.
        
        Args:
            algorithm: Planning algorithm to use
            
        Returns:
            True if all packages were delivered, False otherwise
        """
        # Simple strategy: go to each package, then to each destination
        all_points = self.packages + self.destinations
        
        for point_x, point_y in all_points:
            if not self.plan_path_to(point_x, point_y, algorithm):
                print(f"Failed to plan path to ({point_x}, {point_y})")
                return False
                
            while not self.has_reached_goal(point_x, point_y):
                if not self.execute_step():
                    print(f"Failed to execute path to ({point_x}, {point_y})")
                    return False
                    
                # Check if we're out of fuel
                if self.fuel <= 0:
                    print("Out of fuel!")
                    return False
                    
        return len(self.packages) == 0
        
    def get_status(self) -> Dict:
        """
        Get the current status of the agent.
        
        Returns:
            Dictionary with agent status information
        """
        return {
            "position": (self.x, self.y),
            "fuel": self.fuel,
            "packages_remaining": len(self.packages),
            "path_length": len(self.path),
            "current_step": self.current_step
        }