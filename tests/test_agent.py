"""
Tests for the agent module.
"""

import unittest
from src.environment import Grid, TerrainType
from src.agent import DeliveryAgent

class TestDeliveryAgent(unittest.TestCase):
    """Test cases for the DeliveryAgent class."""
    
    def setUp(self):
        """Set up a test grid and agent."""
        self.grid = Grid(5, 5)
        self.agent = DeliveryAgent(self.grid, 0, 0, fuel=100)
        
    def test_initialization(self):
        """Test agent initialization."""
        self.assertEqual(self.agent.x, 0)
        self.assertEqual(self.agent.y, 0)
        self.assertEqual(self.agent.fuel, 100)
        self.assertEqual(len(self.agent.packages), 0)
        self.assertEqual(len(self.agent.destinations), 0)
        
    def test_add_package(self):
        """Test adding packages."""
        self.agent.add_package(3, 3)
        self.assertEqual(len(self.agent.packages), 1)
        self.assertEqual(self.agent.packages[0], (3, 3))
        
    def test_add_destination(self):
        """Test adding destinations."""
        self.agent.add_destination(4, 4)
        self.assertEqual(len(self.agent.destinations), 1)
        self.assertEqual(self.agent.destinations[0], (4, 4))
        
    def test_plan_path(self):
        """Test path planning."""
        self.agent.add_package(4, 4)
        success = self.agent.plan_path_to(4, 4, "bfs")
        self.assertTrue(success)
        self.assertGreater(len(self.agent.path), 0)
        
    def test_execute_step(self):
        """Test step execution."""
        self.agent.add_package(1, 0)
        self.agent.plan_path_to(1, 0, "bfs")
        success = self.agent.execute_step()
        self.assertTrue(success)
        self.assertEqual(self.agent.x, 1)
        self.assertEqual(self.agent.y, 0)

if __name__ == "__main__":
    unittest.main()