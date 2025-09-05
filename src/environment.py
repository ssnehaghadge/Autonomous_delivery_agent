"""
Environment module for the autonomous delivery agent.
Defines the grid world, terrain types, obstacles, and moving entities.
"""

from enum import Enum
from typing import List, Tuple, Dict, Set, Optional
import numpy as np

class TerrainType(Enum):
    """Enumeration of different terrain types with their movement costs."""
    ROAD = 1
    GRASS = 3
    MUD = 5
    WATER = 10  # Essentially an obstacle unless specified otherwise

class CellType(Enum):
    """Enumeration of cell types in the grid."""
    EMPTY = 0
    OBSTACLE = 1
    AGENT = 2
    PACKAGE = 3
    DESTINATION = 4
    MOVING_OBSTACLE = 5

class Direction(Enum):
    """Enumeration of possible movement directions."""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    
    @staticmethod
    def get_all():
        """Return all possible directions."""
        return [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]

class MovingObstacle:
    """Class representing a moving obstacle with a predefined path."""
    
    def __init__(self, x: int, y: int, path: List[Tuple[int, int]], speed: int = 1):
        """
        Initialize a moving obstacle.
        
        Args:
            x: Initial x-coordinate
            y: Initial y-coordinate
            path: List of (x, y) coordinates defining the path
            speed: Number of time steps between moves
        """
        self.x = x
        self.y = y
        self.path = path
        self.current_step = 0
        self.speed = speed
        self.step_counter = 0
        
    def move(self):
        """Move the obstacle to the next position in its path."""
        self.step_counter += 1
        if self.step_counter >= self.speed:
            self.step_counter = 0
            self.current_step = (self.current_step + 1) % len(self.path)
            self.x, self.y = self.path[self.current_step]
    
    def get_position_at_time(self, time_step: int) -> Tuple[int, int]:
        """
        Predict the obstacle's position at a future time step.
        
        Args:
            time_step: Future time step to predict position for
            
        Returns:
            (x, y) coordinates at the specified time step
        """
        predicted_step = (self.current_step + time_step) % len(self.path)
        return self.path[predicted_step]

class Grid:
    """Class representing the 2D grid environment."""
    
    def __init__(self, width: int, height: int):
        """
        Initialize a grid with specified dimensions.
        
        Args:
            width: Width of the grid
            height: Height of the grid
        """
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)
        self.terrain = np.full((height, width), TerrainType.ROAD.value)
        self.moving_obstacles = []
        
    def is_valid(self, x: int, y: int, time_step: int = 0) -> bool:
        """
        Check if a cell is valid (within bounds and not blocked).
        
        Args:
            x: x-coordinate
            y: y-coordinate
            time_step: Time step to check for moving obstacles
            
        Returns:
            True if the cell is valid, False otherwise
        """
        # Check bounds
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
            
        # Check for static obstacles
        if self.grid[y, x] == CellType.OBSTACLE.value:
            return False
            
        # Check for moving obstacles at this time step
        for obstacle in self.moving_obstacles:
            pred_x, pred_y = obstacle.get_position_at_time(time_step)
            if x == pred_x and y == pred_y:
                return False
                
        return True
        
    def get_cost(self, x: int, y: int) -> int:
        """
        Get the movement cost for a cell.
        
        Args:
            x: x-coordinate
            y: y-coordinate
            
        Returns:
            Movement cost for the cell
        """
        return self.terrain[y, x]
        
    def add_obstacle(self, x: int, y: int):
        """
        Add a static obstacle at the specified coordinates.
        
        Args:
            x: x-coordinate
            y: y-coordinate
        """
        self.grid[y, x] = CellType.OBSTACLE.value
        
    def set_terrain(self, x: int, y: int, terrain_type: TerrainType):
        """
        Set the terrain type for a cell.
        
        Args:
            x: x-coordinate
            y: y-coordinate
            terrain_type: Type of terrain to set
        """
        self.terrain[y, x] = terrain_type.value
        
    def add_moving_obstacle(self, obstacle: MovingObstacle):
        """
        Add a moving obstacle to the grid.
        
        Args:
            obstacle: MovingObstacle instance to add
        """
        self.moving_obstacles.append(obstacle)
        
    def update_moving_obstacles(self):
        """Update positions of all moving obstacles."""
        for obstacle in self.moving_obstacles:
            obstacle.move()
            
    def load_from_file(self, filename: str):
        """
        Load grid configuration from a file.
        
        Args:
            filename: Path to the grid file
        """
        with open(filename, 'r') as f:
            lines = f.readlines()
            
        # Parse grid dimensions
        width, height = map(int, lines[0].split())
        
        # Initialize grid
        self.__init__(width, height)
        
        line_idx = 1
        
        # Parse static obstacles
        num_obstacles = int(lines[line_idx]); line_idx += 1
        for _ in range(num_obstacles):
            x, y = map(int, lines[line_idx].split()); line_idx += 1
            self.add_obstacle(x, y)
            
        # Parse terrain
        for y in range(self.height):
            terrain_row = list(map(int, lines[line_idx].split()))
            line_idx += 1
            for x, terrain_val in enumerate(terrain_row):
                self.set_terrain(x, y, TerrainType(terrain_val))
                
        # Parse moving obstacles
        num_moving_obstacles = int(lines[line_idx]); line_idx += 1
        for _ in range(num_moving_obstacles):
            parts = lines[line_idx].split(); line_idx += 1
            x, y = int(parts[0]), int(parts[1])
            path_length = int(parts[2])
            path = []
            for i in range(path_length):
                path.append((int(parts[3 + i*2]), int(parts[4 + i*2])))
            speed = int(parts[3 + path_length*2])
            obstacle = MovingObstacle(x, y, path, speed)
            self.add_moving_obstacle(obstacle)
            
    def save_to_file(self, filename: str):
        """
        Save grid configuration to a file.
        
        Args:
            filename: Path to save the grid file
        """
        with open(filename, 'w') as f:
            # Write dimensions
            f.write(f"{self.width} {self.height}\n")
            
            # Write static obstacles count and positions
            obstacle_positions = []
            for y in range(self.height):
                for x in range(self.width):
                    if self.grid[y, x] == CellType.OBSTACLE.value:
                        obstacle_positions.append((x, y))
            
            f.write(f"{len(obstacle_positions)}\n")
            for x, y in obstacle_positions:
                f.write(f"{x} {y}\n")
                
            # Write terrain
            for y in range(self.height):
                terrain_row = [str(self.terrain[y, x]) for x in range(self.width)]
                f.write(" ".join(terrain_row) + "\n")
                
            # Write moving obstacles
            f.write(f"{len(self.moving_obstacles)}\n")
            for obstacle in self.moving_obstacles:
                f.write(f"{obstacle.x} {obstacle.y} {len(obstacle.path)} ")
                for x, y in obstacle.path:
                    f.write(f"{x} {y} ")
                f.write(f"{obstacle.speed}\n")