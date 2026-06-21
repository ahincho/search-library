# search-library

[![CI](https://github.com/ahincho/search-library/actions/workflows/ci.yml/badge.svg)](https://github.com/ahincho/search-library/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/search-library.svg)](https://pypi.org/project/search-library/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![MyPy](https://img.shields.io/badge/type--checked-mypy-blue.svg)](http://mypy-lang.org/)
[![Coverage](https://img.shields.io/badge/coverage-96%25-brightgreen.svg)]()

An extensible search algorithm framework for discrete spaces. Designed as both a production-ready library and an academic reference implementation for graph search algorithms in artificial intelligence.

## Motivation

Search algorithms are fundamental to artificial intelligence and computer science. From pathfinding in video games to route planning in logistics, from puzzle solving to knowledge graph traversal, the ability to efficiently explore state spaces is a core capability.

This library was built to:

- Provide correct, well-tested implementations of classical search algorithms
- Serve as a reference for students and researchers studying AI search
- Offer a unified API that enables fair comparison between algorithms
- Demonstrate software engineering best practices in algorithm library design

## Algorithms

| Algorithm | Strategy | Optimal | Complete | Time | Space |
|-----------|----------|---------|----------|------|-------|
| **A\*** | Best-first (f = g + h) | Yes (admissible h) | Yes | O(b^d) | O(b^d) |
| **BFS** | Level-order (FIFO) | Yes (unweighted) | Yes | O(V + E) | O(V) |
| **DFS** | Depth-first (LIFO) | No | Yes (finite) | O(V + E) | O(bm) |
| **Dijkstra** | Best-first (g only) | Yes | Yes | O((V+E) log V) | O(V) |
| **Bidirectional** | Dual BFS | Yes (unweighted) | Yes | O(b^(d/2)) | O(b^(d/2)) |

Where: b = branching factor, d = solution depth, m = max depth, V = vertices, E = edges.

### A* Search

Informed search using `f(n) = g(n) + h(n)`. Guarantees optimal paths when the heuristic is admissible (never overestimates). The most efficient algorithm when a good heuristic is available.

### Breadth-First Search (BFS)

Explores nodes level by level. Guarantees the shortest path by edge count in unweighted graphs. Ideal when all transitions have equal cost.

### Depth-First Search (DFS)

Explores as deep as possible before backtracking. Uses minimal memory but does not guarantee optimal paths. Useful for existence checks and exhaustive exploration.

### Dijkstra's Algorithm

Equivalent to A* with h(n) = 0. Finds the minimum-cost path in weighted graphs without requiring a heuristic. The baseline optimal algorithm for weighted search.

### Bidirectional Search

Searches simultaneously from start and goal, meeting in the middle. Reduces the effective branching factor exponentially, making it ideal for large unweighted graphs.

## Architecture

```
src/search_library/
├── core/               # Base abstractions
│   ├── types.py        # TypeVar T bound to Hashable
│   ├── nodes.py        # Node dataclass (state, g_cost, h_cost, f_cost)
│   ├── problem.py      # SearchProblem ABC (initial_state, is_goal, successors, heuristic)
│   └── result.py       # SearchResult (path, total_cost, nodes_explored, success)
├── algorithms/         # Search implementations
│   ├── base.py         # SearchAlgorithm ABC (unified interface)
│   ├── astar.py        # A* Search
│   ├── bfs.py          # Breadth-First Search
│   ├── dfs.py          # Depth-First Search
│   ├── dijkstra.py     # Dijkstra's Algorithm
│   └── bidirectional.py # Bidirectional BFS
├── heuristics/         # Pluggable heuristic functions
│   ├── base.py         # Heuristic ABC (Strategy Pattern)
│   ├── manhattan.py    # Manhattan distance (L1)
│   └── euclidean.py    # Euclidean distance (L2)
├── graph/              # Weighted graph data structure
│   ├── graph.py        # Graph + GraphSearchProblem adapter
│   └── edges.py        # Edge dataclass
├── grid/               # 2D grid for pathfinding
│   ├── grid.py         # Grid with obstacles, 4/8-directional movement
│   └── grid_search.py  # GridSearchProblem adapter
├── utils/              # Visualization and formatting
└── exceptions/         # Custom error hierarchy
```

### Design Principles

- **SearchProblem** defines the problem space (initial state, goal test, successors, heuristic)
- **SearchAlgorithm** is the unified interface all algorithms implement
- **Adapter Pattern** converts Graph/Grid into SearchProblem transparently
- **Strategy Pattern** makes heuristics interchangeable at runtime
- **SOLID principles** ensure each component has a single responsibility

## Installation

```bash
pip install search-library
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add search-library
```

## Usage

### A* on a Weighted Graph

```python
from search_library import Graph, AStarSearch

# Build a weighted undirected graph
graph = Graph[str](directed=False)
graph.add_edge("A", "B", 4.0)
graph.add_edge("B", "C", 2.0)
graph.add_edge("A", "C", 7.0)
graph.add_edge("C", "D", 1.0)

# Solve with A*
problem = graph.to_search_problem("A", "D")
result = AStarSearch(problem).search()

print(result.path)           # ['A', 'B', 'C', 'D']
print(result.total_cost)     # 7.0
print(result.nodes_explored) # 4
```

### A* on a 2D Grid (Pathfinding)

```python
from search_library import Grid, AStarSearch, ManhattanHeuristic
from search_library.grid import GridSearchProblem

# 0 = walkable, 1 = obstacle
maze = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0],
]

grid = Grid.from_matrix(maze)
problem = GridSearchProblem(grid, start=(0, 0), goal=(4, 4))
result = AStarSearch(problem).search()

print(result.success)    # True
print(result.total_cost) # 8.0
print(result.steps)      # 8
```

### Comparing Algorithms

```python
from search_library import Graph, AStarSearch, BFS, Dijkstra

graph = Graph[str](directed=False)
graph.add_edge("S", "A", 1.0)
graph.add_edge("S", "B", 4.0)
graph.add_edge("A", "B", 2.0)
graph.add_edge("B", "G", 1.0)

problem = graph.to_search_problem("S", "G")

for Algorithm in [AStarSearch, BFS, Dijkstra]:
    result = Algorithm(problem).search()
    print(f"{Algorithm.__name__:20} | cost={result.total_cost:.1f} | explored={result.nodes_explored}")
```

### Convenience Functions

```python
from search_library import astar_search, bfs_search, dfs_search, dijkstra_search

result = astar_search(problem)
result = bfs_search(problem, max_iterations=10000)
result = dijkstra_search(problem, strict=True)
result = dfs_search(problem, track_explored=True)
```

### Grid Visualization

```python
from search_library.utils import print_grid

grid = Grid.from_matrix(maze)
problem = GridSearchProblem(grid, (0, 0), (4, 4))
result = AStarSearch(problem).search(track_explored=True)

print_grid(grid, result, show_explored=True)
# S * * # .
# . # * # .
# . . * # .
# . # * * *
# . . . . G
```

## Academic Use Cases

- **Pathfinding**: Optimal route computation in maps, games, and robotics
- **Puzzle solving**: N-puzzle, Rubik's cube via state-space search
- **Knowledge graphs**: Shortest path between concepts in semantic networks
- **Algorithm comparison**: Empirical analysis of search strategies (optimality, completeness, efficiency)
- **AI education**: Teaching informed vs. uninformed search with clean, readable code
- **Research prototyping**: Quick experimentation with custom search problems and heuristics

## Complexity Analysis

| Algorithm | Time (worst) | Space (worst) | Optimal | Notes |
|-----------|-------------|---------------|---------|-------|
| A* | O(b^d) | O(b^d) | Yes* | *With admissible heuristic |
| BFS | O(V + E) | O(V) | Yes** | **For uniform-cost edges |
| DFS | O(V + E) | O(bm) | No | m = maximum depth |
| Dijkstra | O((V+E) log V) | O(V) | Yes | Non-negative weights required |
| Bidirectional | O(b^(d/2)) | O(b^(d/2)) | Yes** | **Unweighted / symmetric |

## Development

```bash
# Clone and install
git clone https://github.com/ahincho/search-library.git
cd search-library
uv sync

# Run tests (147 tests, 96%+ coverage)
uv run pytest

# Lint and type-check
uv run ruff check src/ tests/
uv run mypy src/

# Build
uv build
```

## Future Work

- Additional heuristics (Chebyshev, Octile, domain-specific)
- Iterative Deepening A* (IDA*)
- Weighted A* and anytime search
- Performance benchmarking suite
- Interactive visualization (matplotlib / terminal)
- Parallel search for large state spaces

## References

- Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). A Formal Basis for the Heuristic Determination of Minimum Cost Paths. *IEEE Transactions on Systems Science and Cybernetics*.
- Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
- Cormen, T. H., et al. (2022). *Introduction to Algorithms* (4th ed.). MIT Press.

## License

[MIT](LICENSE) — Free for academic and commercial use.

## Author

Developed by [ahincho](https://github.com/ahincho) at Universidad Nacional de San Agustin (UNSA).
