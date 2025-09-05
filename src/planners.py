"""
Path planning algorithms for the autonomous delivery agent.
Includes uninformed, informed, and local search algorithms.
"""

import heapq
import random
import math
from typing import List, Tuple, Dict, Set, Optional, Callable
from collections import deque
from .environment import Grid, Direction

class Node:
    """Node class for path planning algorithms."""
    
    def __init__(self, x: int, y: int, cost: int = 0, time_step: int = 0, parent: Optional['Node'] = None):
        """
        Initialize a node for path planning.
        
        Args:
            x: x-coordinate
            y: y-coordinate
            cost: Cost to reach this node
            time_step: Time step when this node is reached
            parent: Parent node
        """
        self.x = x
        self.y = y
        self.cost = cost
        self.time_step = time_step
        self.parent = parent
        
    def __lt__(self, other):
        """Comparison method for priority queue."""
        return self.cost < other.cost
        
    def __eq__(self, other):
        """Equality method."""
        return self.x == other.x and self.y == other.y and self.time_step == other.time_step
        
    def __hash__(self):
        """Hash method for use in sets."""
        return hash((self.x, self.y, self.time_step))
        
    def get_path(self) -> List[Tuple[int, int]]:
        """
        Reconstruct the path from the start node to this node.
        
        Returns:
            List of (x, y) coordinates representing the path
        """
        path = []
        current = self
        while current:
            path.append((current.x, current.y))
            current = current.parent
        return list(reversed(path))

class PathPlanner:
    """Base class for path planning algorithms."""
    
    def __init__(self, grid: Grid):
        """
        Initialize the path planner.
        
        Args:
            grid: Grid environment to plan in
        """
        self.grid = grid
        
    def plan(self, start_x: int, start_y: int, goal_x: int, goal_y: int, 
             start_time: int = 0) -> Optional[Node]:
        """
        Plan a path from start to goal.
        
        Args:
            start_x: Start x-coordinate
            start_y: Start y-coordinate
            goal_x: Goal x-coordinate
            goal_y: Goal y-coordinate
            start_time: Starting time step
            
        Returns:
            Node representing the goal, or None if no path found
        """
        raise NotImplementedError("Subclasses must implement the plan method")
        
    @staticmethod
    def manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
        """
        Calculate Manhattan distance between two points.
        
        Args:
            x1, y1: First point coordinates
            x2, y2: Second point coordinates
            
        Returns:
            Manhattan distance
        """
        return abs(x1 - x2) + abs(y1 - y2)
        
    @staticmethod
    def euclidean_distance(x1: int, y1: int, x2: int, y2: int) -> float:
        """
        Calculate Euclidean distance between two points.
        
        Args:
            x1, y1: First point coordinates
            x2, y2: Second point coordinates
            
        Returns:
            Euclidean distance
        """
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

class BFSPlanner(PathPlanner):
    """Breadth-First Search path planner."""
    
    def plan(self, start_x: int, start_y: int, goal_x: int, goal_y: int, 
             start_time: int = 0) -> Optional[Node]:
        """
        Plan a path using Breadth-First Search.
        
        Args:
            start_x: Start x-coordinate
            start_y: Start y-coordinate
            goal_x: Goal x-coordinate
            goal_y: Goal y-coordinate
            start_time: Starting time step
            
        Returns:
            Node representing the goal, or None if no path found
        """
        queue = deque()
        visited = set()
        
        start_node = Node(start_x, start_y, 0, start_time)
        queue.append(start_node)
        visited.add((start_x, start_y, start_time))
        
        while queue:
            current_node = queue.popleft()
            
            if current_node.x == goal_x and current_node.y == goal_y:
                return current_node
                
            for direction in Direction.get_all():
                dx, dy = direction.value
                new_x, new_y = current_node.x + dx, current_node.y + dy
                new_time_step = current_node.time_step + 1
                
                if self.grid.is_valid(new_x, new_y, new_time_step):
                    if (new_x, new_y, new_time_step) not in visited:
                        visited.add((new_x, new_y, new_time_step))
                        new_node = Node(new_x, new_y, current_node.cost + 1, new_time_step, current_node)
                        queue.append(new_node)
                        
        return None

class UCSPlanner(PathPlanner):
    """Uniform Cost Search path planner."""
    
    def plan(self, start_x: int, start_y: int, goal_x: int, goal_y: int, 
             start_time: int = 0) -> Optional[Node]:
        """
        Plan a path using Uniform Cost Search.
        
        Args:
            start_x: Start x-coordinate
            start_y: Start y-coordinate
            goal_x: Goal x-coordinate
            goal_y: Goal y-coordinate
            start_time: Starting time step
            
        Returns:
            Node representing the goal, or None if no path found
        """
        priority_queue = []
        visited = set()
        
        start_node = Node(start_x, start_y, 0, start_time)
        heapq.heappush(priority_queue, start_node)
        visited.add((start_x, start_y, start_time))
        
        while priority_queue:
            current_node = heapq.heappop(priority_queue)
            
            if current_node.x == goal_x and current_node.y == goal_y:
                return current_node
                
            for direction in Direction.get_all():
                dx, dy = direction.value
                new_x, new_y = current_node.x + dx, current_node.y + dy
                new_time_step = current_node.time_step + 1
                
                if self.grid.is_valid(new_x, new_y, new_time_step):
                    cell_cost = self.grid.get_cost(new_x, new_y)
                    new_cost = current_node.cost + cell_cost
                    
                    if (new_x, new_y, new_time_step) not in visited:
                        visited.add((new_x, new_y, new_time_step))
                        new_node = Node(new_x, new_y, new_cost, new_time_step, current_node)
                        heapq.heappush(priority_queue, new_node)
                        
        return None

class AStarPlanner(PathPlanner):
    """A* path planner with configurable heuristic."""
    
    def __init__(self, grid: Grid, heuristic: Callable[[int, int, int, int], float] = None):
        """
        Initialize the A* path planner.
        
        Args:
            grid: Grid environment to plan in
            heuristic: Heuristic function to use (default: Manhattan distance)
        """
        super().__init__(grid)
        self.heuristic = heuristic or self.manhattan_distance
        
    def plan(self, start_x: int, start_y: int, goal_x: int, goal_y: int, 
             start_time: int = 0) -> Optional[Node]:
        """
        Plan a path using A* search.
        
        Args:
            start_x: Start x-coordinate
            start_y: Start y-coordinate
            goal_x: Goal x-coordinate
            goal_y: Goal y-coordinate
            start_time: Starting time step
            
        Returns:
            Node representing the goal, or None if no path found
        """
        priority_queue = []
        visited = set()
        
        start_node = Node(start_x, start_y, 0, start_time)
        start_priority = start_node.cost + self.heuristic(start_x, start_y, goal_x, goal_y)
        heapq.heappush(priority_queue, (start_priority, start_node))
        visited.add((start_x, start_y, start_time))
        
        while priority_queue:
            _, current_node = heapq.heappop(priority_queue)
            
            if current_node.x == goal_x and current_node.y == goal_y:
                return current_node
                
            for direction in Direction.get_all():
                dx, dy = direction.value
                new_x, new_y = current_node.x + dx, current_node.y + dy
                new_time_step = current_node.time_step + 1
                
                if self.grid.is_valid(new_x, new_y, new_time_step):
                    cell_cost = self.grid.get_cost(new_x, new_y)
                    new_cost = current_node.cost + cell_cost
                    priority = new_cost + self.heuristic(new_x, new_y, goal_x, goal_y)
                    
                    if (new_x, new_y, new_time_step) not in visited:
                        visited.add((new_x, new_y, new_time_step))
                        new_node = Node(new_x, new_y, new_cost, new_time_step, current_node)
                        heapq.heappush(priority_queue, (priority, new_node))
                        
        return None

class SimulatedAnnealingPlanner(PathPlanner):
    """Simulated Annealing path planner for dynamic environments."""
    
    def __init__(self, grid: Grid, max_iterations: int = 1000, 
                 initial_temp: float = 100.0, cooling_rate: float = 0.95):
        """
        Initialize the Simulated Annealing path planner.
        
        Args:
            grid: Grid environment to plan in
            max_iterations: Maximum number of iterations
            initial_temp: Initial temperature
            cooling_rate: Cooling rate for temperature
        """
        super().__init__(grid)
        self.max_iterations = max_iterations
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        
    def plan(self, start_x: int, start_y: int, goal_x: int, goal_y: int, 
             start_time: int = 0) -> Optional[Node]:
        """
        Plan a path using Simulated Annealing.
        
        Args:
            start_x: Start x-coordinate
            start_y: Start y-coordinate
            goal_x: Goal x-coordinate
            goal_y: Goal y-coordinate
            start_time: Starting time step
            
        Returns:
            Node representing the goal, or None if no path found
        """
        # First try to find a path with A*
        astar = AStarPlanner(self.grid)
        current_node = astar.plan(start_x, start_y, goal_x, goal_y, start_time)
        
        if not current_node:
            return None
            
        current_path = current_node.get_path()
        current_cost = current_node.cost
        
        temperature = self.initial_temp
        
        for i in range(self.max_iterations):
            # Generate a neighbor by modifying the path
            if len(current_path) <= 2:
                break
                
            # Randomly select a point to modify (excluding start and end)
            modify_index = random.randint(1, len(current_path) - 2)
            
            # Create a new path by trying a different direction at this point
            new_path = current_path.copy()
            prev_x, prev_y = new_path[modify_index - 1]
            next_x, next_y = new_path[modify_index + 1]
            
            # Try to find an alternative route between prev and next
            directions = list(Direction.get_all())
            random.shuffle(directions)
            
            found_alternative = False
            for direction in directions:
                dx, dy = direction.value
                alt_x, alt_y = prev_x + dx, prev_y + dy
                
                if (alt_x, alt_y) != (prev_x, prev_y) and (alt_x, alt_y) != (next_x, next_y):
                    time_step = modify_index + start_time
                    if self.grid.is_valid(alt_x, alt_y, time_step):
                        # Check if we can get from alt to next in one step
                        if (abs(alt_x - next_x) + abs(alt_y - next_y)) == 1:
                            new_path[modify_index] = (alt_x, alt_y)
                            found_alternative = True
                            break
            
            if found_alternative:
                # Calculate the cost of the new path
                new_cost = 0
                valid_path = True
                
                for j in range(1, len(new_path)):
                    prev_x, prev_y = new_path[j-1]
                    curr_x, curr_y = new_path[j]
                    time_step = j + start_time
                    
                    if not self.grid.is_valid(curr_x, curr_y, time_step):
                        valid_path = False
                        break
                        
                    new_cost += self.grid.get_cost(curr_x, curr_y)
                
                if valid_path:
                    # Decide whether to accept the new path
                    if new_cost < current_cost:
                        current_path = new_path
                        current_cost = new_cost
                    else:
                        # Accept worse solution with probability based on temperature
                        acceptance_prob = math.exp((current_cost - new_cost) / temperature)
                        if random.random() < acceptance_prob:
                            current_path = new_path
                            current_cost = new_cost
                
                # Cool down
                temperature *= self.cooling_rate
        
        # Convert path back to node
        if current_path:
            # Create the node chain
            parent = None
            total_cost = 0
            for i, (x, y) in enumerate(current_path):
                time_step = i + start_time
                if i > 0:
                    prev_x, prev_y = current_path[i-1]
                    total_cost += self.grid.get_cost(x, y)
                node = Node(x, y, total_cost, time_step, parent)
                parent = node
            
            return parent
            
        return None
    