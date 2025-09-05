Autonomous Delivery Agent
An implementation of an autonomous delivery agent that navigates a 2D grid city to deliver packages using various path planning algorithms.

Features
Environment Modeling: Static obstacles, varying terrain costs, dynamic moving obstacles

Path Planning Algorithms:

Uninformed: BFS, Uniform Cost Search

Informed: A* with admissible heuristics (Manhattan/Euclidean distance)

Local Search: Simulated Annealing for dynamic replanning

Rational Agent: Maximizes delivery efficiency under constraints (time, fuel)

Experimental Comparison: Comprehensive testing across multiple map sizes

Dynamic Replanning: Handles moving obstacles and changing environments

Project Structure

autonomous_delivery_agent/
├── src/                 # Source code
│   ├── __init__.py     # Package initialization
│   ├── environment.py  # Grid, obstacles, terrain types
│   ├── agent.py        # Delivery agent implementation
│   ├── planners.py     # Path planning algorithms
│   ├── utils.py        # Utility functions
│   ├── cli.py          # Command-line interface
│   └── api.py          # Programmatic API interface
├── maps/               # Map files
│   ├── small.map       # Small test map
│   ├── medium.map      # Medium test map
│   ├── large.map       # Large test map
│   └── dynamic.map     # Map with dynamic obstacles
├── tests/              # Unit tests
│   ├── __init__.py
│   ├── test_environment.py
│   ├── test_planners.py
│   └── test_agent.py
├── examples.py         # Usage examples
├── requirements.txt    # Python dependencies
├── requirements.md     # Detailed requirements
└── README.md          # This file


Installation
Clone the repository:

bash
git clone <repository-url>
cd autonomous_delivery_agent
Install dependencies:

bash
pip install -r requirements.txt
Quick Start
Basic Usage
python
from src.environment import Grid, TerrainType
from src.agent import DeliveryAgent

# Create a grid
grid = Grid(10, 10)

# Add obstacles and terrain
grid.add_obstacle(3, 3)
grid.set_terrain(2, 2, TerrainType.GRASS)

# Create an agent
agent = DeliveryAgent(grid, 0, 0, fuel=100)

# Add packages and destinations
agent.add_package(7, 7)
agent.add_destination(9, 9)

# Deliver packages using A* algorithm
result = agent.deliver_packages("a_star")
print(f"Delivery {'successful' if result else 'failed'}")
Command Line Interface
bash
# Run a specific experiment
python -m src.cli run --map small --algorithm a_star

# Run all experiments
python -m src.cli run-all --output results.json

# Run demo with dynamic obstacles
python -m src.cli demo --map dynamic --algorithm sa
Running Examples
bash
# Run all examples
python examples.py

# Run specific examples
python -c "from examples import basic_example; basic_example()"

Map Format
Map files use the following format:
width height
num_static_obstacles
x1 y1
x2 y2
...
terrain_grid (space-separated values for each row)
num_moving_obstacles
x y path_length x1 y1 x2 y2 ... speed

Example:
10 10
3
3 3
4 4
5 5
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
1 1 1 1 1 1 1 1 1 1
5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1
3 3 8 3 3 3 4 3 5 3 5 4 5 5 4 5 4 3 2

Algorithms
1. BFS (Breadth-First Search)
Type: Uninformed search

Use Case: Shortest path in terms of number of moves

Advantages: Guaranteed to find shortest path (in moves)

Disadvantages: Ignores terrain costs

2. UCS (Uniform Cost Search)
Type: Uninformed search

Use Case: Optimal path considering terrain costs

Advantages: Guaranteed optimal path cost

Disadvantages: Can be slow for large grids

3. A* (A-Star)
Type: Informed search

Use Case: Efficient optimal path finding

Advantages: Fast with good heuristic

Heuristics: Manhattan distance, Euclidean distance

4. Simulated Annealing
Type: Local search

Use Case: Dynamic environments with moving obstacles

Advantages: Handles changing environments well

Disadvantages: Not guaranteed optimal

API Reference

Core Classes
Grid

grid = Grid(width, height)
grid.add_obstacle(x, y)
grid.set_terrain(x, y, terrain_type)
grid.load_from_file(filename)
grid.save_to_file(filename)

DeliveryAgent

agent = DeliveryAgent(grid, start_x, start_y, fuel=100)
agent.add_package(x, y)
agent.add_destination(x, y)
agent.deliver_packages(algorithm)
agent.plan_path_to(goal_x, goal_y, algorithm)
agent.execute_step()

Path Planners

# Available planners:
# - BFSPlanner(grid)
# - UCSPlanner(grid)
# - AStarPlanner(grid)
# - SimulatedAnnealingPlanner(grid)

planner = AStarPlanner(grid)
path = planner.plan(start_x, start_y, goal_x, goal_y)

Terrain Types
TerrainType.ROAD (cost: 1)

TerrainType.GRASS (cost: 3)

TerrainType.MUD (cost: 5)

TerrainType.WATER (cost: 10)

Testing
Run the test suite:
python -m unittest discover tests
Test coverage includes:

Grid environment functionality

Path planning algorithms

Agent behavior and delivery logic

Obstacle and terrain handling

Examples
The project includes comprehensive examples in examples.py:
# Run all examples
python examples.py

# Example output:
# ✅ Basic Example: Delivery completed successfully!
# ✅ Dynamic Obstacles: Handled moving obstacles!
# ✅ Multiple Packages: All packages delivered!
# 📊 Algorithm Comparison: A* was fastest!

Results Format
Experimental results are saved in JSON format with:
Success status
Path cost
Fuel consumption
Execution time
Algorithm performance metrics

Dynamic Replanning
The system supports dynamic replanning for:
Moving obstacles with predictable paths
Changing terrain costs
Real-time obstacle appearance
Fuel constraints and optimization

Contributing
Fork the repository
Create a feature branch
Add tests for new functionality
Submit a pull request

License
This project is licensed under the MIT License - see the LICENSE file for details.

Citation
If you use this project in your research, please cite:

bibtex
@software{autonomous_delivery_agent,
  title = {Autonomous Delivery Agent},
  author = {Your Name},
  year = {2023},
  url = {https://github.com/yourusername/autonomous_delivery_agent}
}
Support
For questions and support:
Create an issue on GitHub
Check the examples for usage patterns
Review the API documentation

Future Enhancements
GUI visualization
More path planning algorithms
Multi-agent coordination
Real-time simulation
Advanced terrain types
Machine learning integration

Note: This project was developed as part of an academic course on artificial intelligence and autonomous systems.
