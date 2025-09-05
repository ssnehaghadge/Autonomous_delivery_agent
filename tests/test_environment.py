"""
Tests for the environment module.
"""

import unittest
import numpy as np
from src.environment import Grid, TerrainType, MovingObstacle

class TestGrid(unittest.TestCase):
    """Test cases for the Grid class."""
    
    def setUp(self):
        """Set up a test grid."""
        self.grid = Grid(10, 10)
        
    def test_initialization(self):
        """Test grid initialization."""
        self.assertEqual(self.grid.width, 10)
        self.assertEqual(self.grid.height, 10)
        self.assertEqual(self.grid.grid.shape, (10, 10))
        self.assertEqual(self.grid.terrain.shape, (10, 10))
        
    def test_add_obstacle(self):
        """Test adding obstacles."""
        self.grid.add_obstacle(5, 5)
        self.assertEqual(self.grid.grid[5, 5], 1)
        
    def test_set_terrain(self):
        """Test setting terrain."""
        self.grid.set_terrain(3, 3, TerrainType.GRASS)
        self.assertEqual(self.grid.terrain[3, 3], 3)
        
    def test_is_valid(self):
        """Test cell validation."""
        # Test within bounds
        self.assertTrue(self.grid.is_valid(0, 0))
        self.assertTrue(self.grid.is_valid(9, 9))
        
        # Test out of bounds
        self.assertFalse(self.grid.is_valid(-1, 0))
        self.assertFalse(self.grid.is_valid(10, 10))
        
        # Test with obstacle
        self.grid.add_obstacle(5, 5)
        self.assertFalse(self.grid.is_valid(5, 5))
        
    def test_get_cost(self):
        """Test getting movement cost."""
        self.grid.set_terrain(3, 3, TerrainType.MUD)
        self.assertEqual(self.grid.get_cost(3, 3), 5)

class TestMovingObstacle(unittest.TestCase):
    """Test cases for the MovingObstacle class."""
    
    def test_movement(self):
        """Test obstacle movement."""
        path = [(0, 0), (0, 1), (1, 1), (1, 0)]
        obstacle = MovingObstacle(0, 0, path, speed=1)
        
        # Test initial position
        self.assertEqual(obstacle.x, 0)
        self.assertEqual(obstacle.y, 0)
        
        # Test movement
        obstacle.move()
        self.assertEqual(obstacle.x, 0)
        self.assertEqual(obstacle.y, 1)
        
        obstacle.move()
        self.assertEqual(obstacle.x, 1)
        self.assertEqual(obstacle.y, 1)
        
    def test_get_position_at_time(self):
        """Test position prediction."""
        path = [(0, 0), (0, 1), (1, 1), (1, 0)]
        obstacle = MovingObstacle(0, 0, path, speed=1)
        
        self.assertEqual(obstacle.get_position_at_time(0), (0, 0))
        self.assertEqual(obstacle.get_position_at_time(1), (0, 1))
        self.assertEqual(obstacle.get_position_at_time(2), (1, 1))

if __name__ == "__main__":
    unittest.main()