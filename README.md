# Pac-Man-Python and A*

### Demo


https://github.com/Azabu-bound/Pac-Man-Python/assets/150316117/80af1911-0690-4c27-b7bc-d1a87ab33bb4


### Getting Started
To run the Pac-Man with A* program locally, follow these steps:

#### Prerequisites
- Python 3.x: Make sure you have Python 3.x installed on your system. You can download it from the official Python website: python.org
- Pygame (https://pypi.org/project/pygame/): The program requires the Pygame library. You can install it using pip by running the following command:
```
pip install pygame
```

#### Cloning the Repository
1. Open your terminal or cli.
2. Change the current working directory to the location where you want to clone the repository.
3. Run the following command to clone the repository:
```
git clone https://github.com/Azabu-bound/Pac-Man-Python.git
```
4. Once the cloning process is complete, navigate to the directory:
```
cd Pac-Man-Python
```
5. Move into the src file:
```
cd src
```

#### Loading the game
1. Confirm you are in the correct directory.
2. run the following in your terminal:
```
python3 main.py
```

### Playing the game
- To begin playing press the SPACE BAR.
- You can move Pac-Man using the arrow keys or W, A, S, D keys.
- You can pause the game by pressing the SPACE BAR. A subsequent press will resume the game.
- The objective is to eat all of the pellets while avoiding the ghosts. 
- If Pac-Man collides with a ghost, you will lose a life. The game ends when you lose all your lives (3).
- If you consume a power-up pellet and collide with a ghost you will send it back to spawn.
- If you eat all the pellets, you win the game! Upon winning the game will reset.

### Data Structures, algorithms, pathfinding, oh my!
Pac-Man can essentially be viewed as a graph problem given that the map/maze is just one big graph. Each intersection or junction in the maze can be considered a node (or vertex) in the graph, and the paths connecting these intersections can be considered edges.

Within Pac-Man specifically the graph allows us to:
1. Find the shortest path between two points in the maze, such as the path from Pac-Man's current position to a target pellet or the path from a ghost's position to Pac-Man.
2. Determine the connectivity of the maze, ensuring that all areas are reachable.
3. Implement pathfinding algorithms, such as A*, to efficiently navigate the maze and make intelligent decisions for Pac-Man and the ghosts.

To implement the map we use a class called NodeGroup. The NodeGroup class reads the maze layout from a text file and creates a lookup table (nodes_LUT) that maps tile coordinates to Node objects. Each Node object represents a tile in the maze and contains information about its neighbors and access permissions for entities (Pac-Man and ghosts).
Just look at this beautiful graph!!



![Screenshot 2024-05-03 at 22 09 31](https://github.com/Azabu-bound/Pac-Man-Python/assets/150316117/7ba851d8-90fd-44bc-8a3b-d0fcb8ac8328)

#### A* and pathfinding
For this project I really had three goals: gain experience in game development, work with graphs, and explore pathfinding. Graphs are simply awesome and Dijkstra's algorithm was one of my favorite lectures from 3104. Finding out that the A* algorithm combines the advantages of both Dijkstra's algorithm, which guarantees the shortest path, and the greedy best-first search algorithm, which focuses on reaching the goal quickly, inspired me to attempt to implement it.

Foremost, I think it is best to explain a bit about how A* works. The A* algorithm uses a heuristic function to estimate the cost of reaching the goal from a given node. The heuristic function is an estimate of the minimum cost from the current node to the goal node. The algorithm maintains an open set of nodes to be explored and a closed set of nodes that have already been explored. The algorithm expands the nodes with the lowest f-cost first, balancing the actual cost (g-cost) and the estimated cost to the goal (h-cost). This allows it to efficiently explore the most promising paths while still considering the actual shortest path.

So, why does A* potentially improve Pac-Man?
In short, the algorithm can be used by the ghosts to find the optimal path to reach Pac-Man's position. This makes the game more challenging because:
1. Intelligent Ghost Movement: Instead of random or predetermined movements, the ghosts can use the A* algorithm to calculate the most efficient path to reach Pac-Man. This makes their movement more intelligent and purposeful, increasing the difficulty for the player.
2. Dynamic Pathfinding: As Pac-Man moves around the maze, the ghosts can continuously update their target position and recalculate the optimal path using A*. This allows them to adapt to Pac-Man's movements and actively pursue him, making it harder for the player to escape.
3. Coordinated Pursuit: Multiple ghosts can use the A* algorithm simultaneously, each targeting Pac-Man from different positions. This coordinated pursuit can create challenging situations where Pac-Man is surrounded or cornered by the ghosts.
4. Efficient Resource Utilization: The A* algorithm efficiently utilizes the available resources (nodes and edges) in the game graph. It explores the most promising paths first, reducing unnecessary exploration and allowing the ghosts to reach Pac-Man more quickly.

Here is my code for the A* algorithm:
```
def astar_direction(self, directions):
    queue = []
    cost = {self.node: 0}
    previous = {self.node: None}

    heapq.heappush(queue, PriorityEntry(0, 0, self.node))  # Push the starting node

    while queue:
        current_entry = heapq.heappop(queue)  # Pop the entry with the lowest priority
        current_cost = current_entry.cost
        current_node = current_entry.node

        if current_node.position == self.goal:
            path = []
            while current_node != self.node:
                path.append(current_node)
                current_node = previous[current_node]
            path.append(self.node)
            path.reverse()
            if len(path) > 1:
                next_node = path[1]
                for d in directions:
                    if self.node.neighbors[d] == next_node:
                        return d
            break

        for d in directions:
            neighbor = self.node.neighbors[d]
            if neighbor is not None:
                new_cost = current_cost + 1
                if neighbor not in cost or new_cost < cost[neighbor]:
                    cost[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor.position, self.goal)
                    heapq.heappush(queue, PriorityEntry(priority, new_cost, neighbor))
                    previous[neighbor] = current_node

        if not queue:
                # If no path is found, return the direction that brings the ghost closer to the goal
                min_distance = float('inf')
                closest_direction = None
                for d in directions:
                    neighbor = self.node.neighbors[d]
                    if neighbor is not None:
                        distance = self.heuristic(neighbor.position, self.goal)
                        if distance < min_distance:
                            min_distance = distance
                            closest_direction = d
                if closest_direction is not None:
                    return closest_direction

    return self.random_direction(directions)

def heuristic(self, a, b):
    # Manhattan distance heuristic
    return abs(a.x - b.x) + abs(a.y - b.y)
```

#### Priority Queue
When implementing A* it became apparent that we were going to need to trade some memory for better time efficiency. Our weapon of choice was the priority queue. A priority queue allows us to efficiently select the most promising node to explore next. In A*, we assign each node a priority based on the estimated total cost to reach the goal through that node. The priority is typically calculated as the sum of the actual cost to reach the node (g-cost) and the estimated cost from the node to the goal (h-cost, or heuristic).

By using a priority queue, we can ensure that the node with the lowest estimated total cost is always at the front of the queue. This enables the A* algorithm to explore the most promising paths first, potentially reaching the goal faster and more efficiently compared to other pathfinding algorithms.
The priority queue maintains the nodes in a sorted order based on their estimated total cost. When we need to select the next node to explore, we simply dequeue the node with the highest priority (lowest estimated total cost) from the front of the queue. This operation is typically performed in logarithmic time complexity (O(log n)).

I utilized a priority queue using the heapq module in Python. The priority queue stores PriorityEntry objects, which contain the priority (estimated total cost), cost (actual cost from the start node), and the corresponding Node object.

When implementing the priority queue I was constanly getting the following error: The error message `TypeError: '<' not supported between instances of 'Node' and 'Node'`. This error kept occuring because python heap queue (heapq) was not able to compare two instances of my Node class directly. The PriorityEntry class was designed to handle this error. The __lt__ and __eq__ methods in the PriorityEntry class are special methods in Python that define the behavior of the less than (<) and equality (==) operators, respectively, when comparing instances of the PriorityEntry class. These methods are important for the correct functioning of the priority queue used in the A* algorithm. The __lt__ method determines the ordering of the entries in the priority queue, ensuring that the entry with the lowest priority (and cost as a tiebreaker) is always at the front of the queue. The __eq__ method is used to check for equality between entries, which is useful when updating or removing entries from the priority queue.

Here is the code for PriorityEntry:
```
class PriorityEntry:
    def __init__(self, priority, cost, node):
        self.priority = priority
        self.cost = cost
        self.node = node

    def __lt__(self, other):
        return (self.priority < other.priority) or (self.priority == other.priority and self.cost < other.cost)

    def __eq__(self, other):
        return self.node == other.node and self.cost == other.cost and self.priority == other.priority
```

### A moment for reflection :)
When I initially started this project, I wanted to learn a new language and game engine. I originally planned to do this project in LUA using the LOVE game engine. However, I quickly realized how difficult of a problem Pac-Man is to solve, especially considering I would need to implement two data structures. As a result, I defaulted to working with a language and engine I am more comfortable with: Python and Pygame. With this said, I crucially learned that fighting a war on two fronts is silly (especially when there is no need to). Also, just because a project is well-defined does not mean it will be easy to implement. Pac-Man is easy to conceptualize, has an abundance of references available, and is well-studied; however, the various gotchas (I'm looking at you, ghosts!) and nuances make for a challenging programming experience. In hindsight, I would not have completed this project had I not already been tinkering around with writing Pac-Man in Python before this semester and had experience hacking other famous arcade games such as Pong and Asteroids.

While this project functions as intended and largely resembles Pac-Man, it could be improved. The following are a list of features that could be added:
- Fruit mechanic
- Sprites
- A graphically rendered Maze
- Sound Fx
- Animations
- Text
- A title screen
- A leaderboard
- Multiple levels

#### References
- https://theory.stanford.edu/~amitp/GameProgramming/AStarComparison.html (A*)
- https://www.youtube.com/watch?v=eSOJ3ARN5FM (A*)
- https://www.youtube.com/watch?v=9H27CimgPsQ (Pac-Man)
- https://pacman.holenet.info/#Chapter_2 (Pac-Man)
