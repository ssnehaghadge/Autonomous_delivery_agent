"""
Script to run all experiments and generate results.
"""

from src.utils import run_experiment, save_results
import traceback

def main():
    """Run all experiments and save results."""
    results = []
    map_sizes = ["small", "medium", "large", "dynamic"]
    algorithms = ["bfs", "ucs", "a_star", "sa"]
    
    for map_size in map_sizes:
        for algorithm in algorithms:
            try:
                print(f"Running {algorithm} on {map_size} map...")
                result = run_experiment(map_size, algorithm)
                results.append(result)
                print(f"Result: Success={result['success']}, Cost={result['path_cost']}, Time={result['time_taken']:.4f}s")
            except Exception as e:
                print(f"Error running {algorithm} on {map_size}: {str(e)}")
                traceback.print_exc()
                # Add error result
                results.append({
                    "success": False,
                    "path_cost": float('inf'),
                    "fuel_remaining": 0,
                    "time_taken": 0,
                    "path_length": 0,
                    "algorithm": algorithm,
                    "map_size": map_size,
                    "error": str(e)
                })
            
    save_results(results, "experiment_results.json")
    print("All experiments completed. Results saved to experiment_results.json")
    
    # Print summary
    success_count = sum(1 for r in results if r['success'])
    total_count = len(results)
    print(f"Success rate: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")

if __name__ == "__main__":
    main()