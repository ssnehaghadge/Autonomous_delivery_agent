"""
Example usage of the Autonomous Delivery Agent API.
These examples demonstrate various ways to use the system.
"""

import os
import sys
import time

# Add the current directory to the path so we can import from src
sys.path.insert(0, os.path.dirname(__file__))

# Now import using absolute imports
from src.environment import Grid, TerrainType, MovingObstacle, Direction
from src.agent import DeliveryAgent
from src.planners import BFSPlanner, UCSPlanner, AStarPlanner, SimulatedAnnealingPlanner

def print_separator():
    """Print a separator line for better output readability."""
    print("\n" + "="*60 + "\n")

def basic_example():
    """Basic example of using the API."""
    print("=== Basic Example ===")
    print("Creating a simple grid and delivering a package")
    
    # Create a grid
    grid = Grid(10, 10)
    print(f"Grid created with size 10x10")
    
    # Add some obstacles
    grid.add_obstacle(3, 3)
    grid.add_obstacle(4, 4)
    grid.add_obstacle(5, 5)
    
    # Set terrain
    grid.set_terrain(2, 2, TerrainType.GRASS)
    grid.set_terrain(6, 6, TerrainType.MUD)
    
    # Create an agent
    agent = DeliveryAgent(grid, 0, 0, fuel=100)
    print("Agent created at (0, 0) with 100 fuel")
    
    # Add packages and destinations
    agent.add_package(7, 7)
    agent.add_destination(9, 9)
    print("Package at (7, 7), Destination at (9, 9)")
    
    # Execute delivery with A* algorithm
    print("Starting delivery with A* algorithm...")
    result = agent.deliver_packages("a_star")
    
    if result:
        print("✅ Delivery completed successfully!")
    else:
        print("❌ Delivery failed!")
    
    # Get agent status
    status = agent.get_status()
    print(f"Final position: {status['position']}")
    print(f"Fuel remaining: {status['fuel']}")
    print(f"Packages remaining: {status['packages_remaining']}")
    return result

def load_map_example():
    """Example of loading a map from file."""
    print_separator()
    print("=== Load Map Example ===")
    print("Loading a map from file and delivering a package")
    
    # Check if map file exists
    map_file = "maps/small.map"
    if not os.path.exists(map_file):
        print(f"Map file {map_file} not found. Creating a simple grid instead.")
        grid = Grid(8, 8)
        # Add some obstacles
        for i in range(3, 6):
            grid.add_obstacle(i, 4)
    else:
        # Load a grid from file
        grid = Grid(1, 1)  # Temporary grid
        grid.load_from_file(map_file)
        print(f"Loaded grid: {grid.width}x{grid.height}")
    
    # Create an agent
    agent = DeliveryAgent(grid, 0, 0, fuel=200)
    print(f"Agent created at (0, 0) with 200 fuel")
    
    # Add packages and destinations based on map size
    package_pos = (grid.width-1, grid.height-1)
    destination_pos = (grid.width//2, grid.height//2)
    
    agent.add_package(*package_pos)
    agent.add_destination(*destination_pos)
    print(f"Package at {package_pos}, Destination at {destination_pos}")
    
    # Execute delivery with UCS algorithm
    print("Starting delivery with UCS algorithm...")
    result = agent.deliver_packages("ucs")
    
    if result:
        print("✅ Delivery completed successfully!")
        status = agent.get_status()
        print(f"Fuel remaining: {status['fuel']}")
    else:
        print("❌ Delivery failed!")
        status = agent.get_status()
        print(f"Fuel remaining: {status['fuel']}")
        print(f"Packages remaining: {status['packages_remaining']}")
    
    return result

def dynamic_obstacles_example():
    """Example with moving obstacles."""
    print_separator()
    print("=== Dynamic Obstacles Example ===")
    print("Demonstrating path planning with moving obstacles")
    
    # Create a grid
    grid = Grid(15, 15)
    print("Created 15x15 grid")
    
    # Add a moving obstacle with a circular path
    path = [(3, 3), (3, 4), (3, 5), (4, 5), (5, 5), (5, 4), (5, 3), (4, 3)]
    moving_obstacle = MovingObstacle(3, 3, path, speed=2)
    grid.add_moving_obstacle(moving_obstacle)
    print("Added moving obstacle with circular path")
    
    # Add some static obstacles
    for i in range(5, 10):
        grid.add_obstacle(i, 7)
    print("Added static obstacles")
    
    # Create an agent
    agent = DeliveryAgent(grid, 0, 0, fuel=150)
    print("Agent created at (0, 0) with 150 fuel")
    
    # Add packages and destinations
    agent.add_package(10, 10)
    agent.add_destination(14, 14)
    print("Package at (10, 10), Destination at (14, 14)")
    
    # Use simulated annealing for dynamic replanning
    print("Starting delivery with Simulated Annealing algorithm...")
    result = agent.deliver_packages("sa")
    
    if result:
        print("✅ Delivery completed successfully with dynamic obstacles!")
    else:
        print("❌ Delivery failed with dynamic obstacles!")
    
    # Show grid info
    status = agent.get_status()
    print(f"Final position: {status['position']}")
    print(f"Fuel remaining: {status['fuel']}")
    print(f"Grid has {len(grid.moving_obstacles)} moving obstacles")
    
    return result

def multiple_packages_example():
    """Example with multiple packages."""
    print_separator()
    print("=== Multiple Packages Example ===")
    print("Delivering multiple packages to multiple destinations")
    
    # Create a grid
    grid = Grid(12, 12)
    print("Created 12x12 grid")
    
    # Add some obstacles
    for i in range(4, 8):
        grid.add_obstacle(i, 6)
    print("Added obstacles")
    
    # Add different terrain types
    for i in range(12):
        for j in range(3):
            grid.set_terrain(i, j, TerrainType.GRASS)
        for j in range(9, 12):
            grid.set_terrain(i, j, TerrainType.MUD)
    print("Added varying terrain types")
    
    # Create an agent with more fuel
    agent = DeliveryAgent(grid, 0, 0, fuel=300)
    print("Agent created at (0, 0) with 300 fuel")
    
    # Add multiple packages and destinations
    packages = [(3, 3), (8, 8), (5, 10)]
    destinations = [(10, 2), (2, 10), (10, 10)]
    
    for pkg in packages:
        agent.add_package(*pkg)
    for dest in destinations:
        agent.add_destination(*dest)
    
    print(f"Added {len(packages)} packages at: {packages}")
    print(f"Added {len(destinations)} destinations at: {destinations}")
    
    # Execute delivery with A* algorithm
    print("Starting delivery with A* algorithm...")
    result = agent.deliver_packages("a_star")
    
    if result:
        print("✅ All packages delivered successfully!")
        status = agent.get_status()
        print(f"Fuel remaining: {status['fuel']}")
    else:
        print("❌ Delivery failed!")
        status = agent.get_status()
        print(f"Fuel remaining: {status['fuel']}")
        print(f"Packages remaining: {status['packages_remaining']}")
    
    return result

def algorithm_comparison_example():
    """Example comparing different algorithms."""
    print_separator()
    print("=== Algorithm Comparison Example ===")
    print("Comparing different path planning algorithms on the same problem")
    
    algorithms = ["bfs", "ucs", "a_star", "sa"]
    results = {}
    
    for algo in algorithms:
        print(f"\nTesting {algo} algorithm...")
        
        # Create a fresh grid for each test
        grid = Grid(8, 8)
        
        # Add obstacles in a plus pattern
        for i in range(2, 6):
            grid.add_obstacle(i, 4)
            grid.add_obstacle(4, i)
        
        # Add varying terrain
        for i in range(8):
            for j in range(2):
                grid.set_terrain(i, j, TerrainType.GRASS)
            for j in range(6, 8):
                grid.set_terrain(i, j, TerrainType.MUD)
        
        # Create an agent
        agent = DeliveryAgent(grid, 0, 0, fuel=200)
        
        # Add package and destination
        agent.add_package(7, 7)
        agent.add_destination(3, 3)
        
        # Execute delivery and measure time
        start_time = time.time()
        result = agent.deliver_packages(algo)
        end_time = time.time()
        
        # Store results
        status = agent.get_status()
        results[algo] = {
            "success": result,
            "time": end_time - start_time,
            "fuel_remaining": status["fuel"],
            "message": "Success" if result else "Failed"
        }
    
    # Print comparison results
    print("\nAlgorithm Comparison Results:")
    print("-" * 50)
    for algo, result in results.items():
        print(f"{algo.upper():<6}: Success={result['success']}, "
              f"Time={result['time']:.4f}s, "
              f"Fuel={result['fuel_remaining']}, "
              f"Message={result['message']}")
    
    return results

def step_by_step_example():
    """Example showing step-by-step execution."""
    print_separator()
    print("=== Step-by-Step Example ===")
    print("Demonstrating manual control of the agent")
    
    # Create a simple grid
    grid = Grid(5, 5)
    print("Created 5x5 grid")
    
    # Add an obstacle
    grid.add_obstacle(2, 2)
    print("Added obstacle at (2, 2)")
    
    # Create an agent
    agent = DeliveryAgent(grid, 0, 0, fuel=50)
    print("Agent created at (0, 0) with 50 fuel")
    
    # Add a package
    agent.add_package(4, 4)
    print("Package added at (4, 4)")
    
    # Plan a path
    planner = AStarPlanner(grid)
    result = planner.plan(0, 0, 4, 4)
    
    if result is not None:
        print(f"✅ Path found with cost {result.cost}")
        path = result.get_path()
        print(f"Path length: {len(path)} steps")
        print(f"Path: {path}")
        
        # Manual execution (just a few steps for demonstration)
        agent = DeliveryAgent(grid, 0, 0, fuel=50)  # Reset agent
        agent.add_package(4, 4)  # Re-add package
        
        # Plan the path
        agent.plan_path_to(4, 4, "a_star")
        
        # Execute a few steps manually
        for i in range(min(3, len(agent.path))):
            status = agent.get_status()
            print(f"\nStep {i}: Position={status['position']}, Fuel={status['fuel']}")
            
            # Execute one step
            if agent.execute_step():
                print(f"  Moved to ({agent.x}, {agent.y})")
                # Check if we picked up a package
                if (agent.x, agent.y) == (4, 4):
                    print("  📦 Package picked up!")
            else:
                print("  ❌ Cannot move further")
                break
            
        # Show final status
        status = agent.get_status()
        print(f"\nFinal: Position={status['position']}, Fuel={status['fuel']}")
        return True
    else:
        print("❌ No path found")
        return False

def error_handling_example():
    """Example demonstrating error handling."""
    print_separator()
    print("=== Error Handling Example ===")
    print("Showing how the system handles various error conditions")
    
    results = []
    
    # Test 1: Impossible path
    print("\n1. Testing impossible path:")
    grid = Grid(3, 3)
    # Create a wall of obstacles
    for i in range(3):
        grid.add_obstacle(i, 1)
    
    agent = DeliveryAgent(grid, 0, 0, fuel=50)
    agent.add_package(2, 2)
    
    result = agent.deliver_packages("a_star")
    results.append(result)
    print(f"   Result: {'✅ Success' if result else '❌ Failed'}")
    
    # Test 2: Out of fuel
    print("\n2. Testing out of fuel scenario:")
    grid = Grid(5, 5)
    # Set all terrain to high cost
    for i in range(5):
        for j in range(5):
            grid.set_terrain(i, j, TerrainType.WATER)  # High cost
    
    agent = DeliveryAgent(grid, 0, 0, fuel=10)  # Very low fuel
    agent.add_package(4, 4)
    
    result = agent.deliver_packages("a_star")
    results.append(result)
    print(f"   Result: {'✅ Success' if result else '❌ Failed'}")
    status = agent.get_status()
    print(f"   Fuel remaining: {status['fuel']}")
    
    return results

def main():
    """Run all examples."""
    print("Autonomous Delivery Agent Examples")
    print("==================================")
    
    results = []
    
    # Run examples
    results.append(basic_example())
    results.append(load_map_example())
    results.append(dynamic_obstacles_example())
    results.append(multiple_packages_example())
    
    # These might take longer, so run them last
    algorithm_results = algorithm_comparison_example()
    results.append(step_by_step_example())
    error_results = error_handling_example()
    results.extend(error_results)
    
    print_separator()
    print("📊 Examples Summary:")
    print("====================")
    
    success_count = sum(1 for r in results if r is True)
    total_count = len(results)
    
    print(f"Completed {total_count} examples")
    print(f"Successful: {success_count}")
    print(f"Failed: {total_count - success_count}")
    print(f"Success rate: {success_count/total_count*100:.1f}%")
    
    if success_count == total_count:
        print("🎉 All examples completed successfully!")
    else:
        print("⚠️  Some examples failed. Check the output above for details.")

if __name__ == "__main__":
    main()
    