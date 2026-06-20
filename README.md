# search-library

A professional, extensible search algorithm framework for discrete spaces (graphs and 2D grids).

## Features

- **A\* Search Algorithm** with optimal path finding
- **Graph support** — weighted directed/undirected graphs
- **Grid support** — 2D pathfinding with obstacles, 4/8-directional movement
- **Pluggable heuristics** — Manhattan, Euclidean, or custom
- **Extensible architecture** — designed for adding BFS, DFS, Dijkstra, etc.
- **Strict typing** — full mypy strict compliance
- **Zero dependencies** — pure Python, no external runtime deps

## Installation

```bash
pip install search-library
```

## Quick Start

### Graph Search

```python
from search_library import Graph, AStarSearch

graph = Graph[str](directed=False)
graph.add_edge("A", "B", 1.0)
graph.add_edge("B", "C", 2.0)
graph.add_edge("A", "C", 5.0)

problem = graph.to_search_problem("A", "C")
solver = AStarSearch(problem)
result = solver.search()

print(result.path)        # ['A', 'B', 'C']
print(result.total_cost)  # 3.0
```

### Grid Pathfinding

```python
from search_library import Grid, AStarSearch
from search_library.grid import GridSearchProblem

matrix = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0],
]

grid = Grid.from_matrix(matrix)
problem = GridSearchProblem(grid, start=(0, 0), goal=(4, 4))
solver = AStarSearch(problem)
result = solver.search()

print(result.success)         # True
print(result.path)            # [(0,0), (0,1), ..., (4,4)]
print(result.nodes_explored)  # Number of nodes explored
```

### Custom Heuristic

```python
from search_library.heuristics.base import Heuristic

class ChebyshevHeuristic(Heuristic[tuple[int, int]]):
    def estimate(self, state: tuple[int, int], goal: tuple[int, int]) -> float:
        return float(max(abs(state[0] - goal[0]), abs(state[1] - goal[1])))
```

## Development

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Lint
uv run ruff check src/ tests/

# Type check
uv run mypy src/

# Build
uv build
```

## Architecture

```
src/search_library/
├── core/           # Base abstractions (Node, SearchProblem, SearchResult)
├── algorithms/     # Search implementations (A*)
├── heuristics/     # Pluggable heuristic functions
├── graph/          # Graph data structures
├── grid/           # 2D grid pathfinding
├── utils/          # Helper utilities
└── exceptions/     # Custom exceptions
```

## License

MIT
