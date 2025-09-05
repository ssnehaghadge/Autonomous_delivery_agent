"""
Tests for the planners module.
"""

import unittest
from src.environment import Grid, TerrainType
from src.planners import BFSPlanner, UCSPlanner, AStarPlanner, SimulatedAnnealingPlanner

class TestPathPlanners(unittest.TestCase):
    """Test cases for path planning algorithms."""
    
    def setUp(self):
        """Set up a test grid."""
        self.grid = Grid(5, 5)
        # Add a simple obstacle
        self.grid.add_obstacle(2, 2)
        
    def test_bfs_planner(self):
        """Test BFS path planning."""
        planner = BFSPlanner(self.grid)
        result = planner.plan(0, 0, 4, 4)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.x, 4)
        self.assertEqual(result.y, 4)
        
        # Check path length (should be 8 moves for a 5x5 grid with one obstacle)
        path = result.get_path()
        self.assertEqual(len(path), 9)  # Includes start position
        
    def test_ucs_planner(self):
        """Test UCS path planning."""
        planner = UCSPlanner(self.grid)
        result = planner.plan(0, 0, 4, 4)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.x, 4)
        self.assertEqual(result.y, 4)
        
    def test_astar_planner(self):
        """Test A* path planning."""
        planner = AStarPlanner(self.grid)
        result = planner.plan(0, 0, 4, 4)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.x, 4)
        self.assertEqual(result.y, 4)
        
    def test_simulated_annealing_planner(self):
        """Test Simulated Annealing path planning."""
        planner = SimulatedAnnealingPlanner(self.grid, max_iterations=100)
        result = planner.plan(0, 0, 4, 4)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.x, 4)
        self.assertEqual(result.y, 4)

if __name__ == "__main__":
    unittest.main()