# search-library

[![CI](https://github.com/ahincho/search-library/actions/workflows/ci.yml/badge.svg)](https://github.com/ahincho/search-library/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![MyPy](https://img.shields.io/badge/type--checked-mypy-blue.svg)](http://mypy-lang.org/)
[![Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen.svg)]()

A professional, extensible search algorithm framework for discrete spaces (graphs and 2D grids).

## Features

- **A\* Search Algorithm** — optimal pathfinding with `f(n) = g(n) + h(n)`
- **Graph support** — weighted directed/undirected graphs with adjacency lists
- **Grid support** — 2D pathfinding with obstacles, variable costs, 4/8-directional movement
- **Pluggable heuristics** — Manhattan, Euclidean, or bring your own
- **Extensible architecture** — designed for adding BFS, DFS, Dijkstra without modifying base code
- **Strict typing** — full `mypy --strict` compliance with Generics and Protocols
- **Zero runtime dependencies** — pure Python standard library only

## Installation

```bash
pip install search-library
```

Or with uv:

```bash
uv add search-library
```

## Quick Start

### Graph Search

```python
from search_library import Graph, AStarSearch

# Create an undirected weighted graph
graph = Graph[str](directed=False)
graph.add_edge("A", "B", 1.0)
graph.add_edge("B", "C", 2.0)
graph.add_edge("A", "C", 5.0)

# Solve with A*
problem = graph.to_search_problem("A", "C")
solver = AStarSearch(problem)
result = solver.search()

print(result.path)           # ['A', 'B', 'C']
print(result.total_cost)     # 3.0
print(result.nodes_explored) # 3
```

### Grid Pathfinding (Maze)

```python
from search_library import Grid, AStarSearch
from search_library.grid import GridSearchProblem

# 0 = walkable, 1 = obstacle
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
print(result.total_cost)      # 8.0
print(result.nodes_explored)  # Number of states explored
```

### Custom Heuristic

```python
from search_library.heuristics.base import Heuristic

class ChebyshevHeuristic(Heuristic[tuple[int, int]]):
    """Chebyshev distance — useful for 8-directional grids."""
    def estimate(self, state: tuple[int, int], goal: tuple[int, int]) -> float:
        return float(max(abs(state[0] - goal[0]), abs(state[1] - goal[1])))
```

### Custom Search Problem

```python
from search_library.core.problem import SearchProblem
from search_library.algorithms.astar import AStarSearch

class EightPuzzle(SearchProblem[tuple[int, ...]]):
    """Example: define any discrete search problem."""
    def initial_state(self) -> tuple[int, ...]:
        return (1, 2, 3, 4, 0, 5, 6, 7, 8)

    def is_goal(self, state: tuple[int, ...]) -> bool:
        return state == (1, 2, 3, 4, 5, 6, 7, 8, 0)

    def successors(self, state: tuple[int, ...]) -> list[tuple[tuple[int, ...], float]]:
        # Return list of (next_state, cost) tuples
        ...
```

## Architecture

```
src/search_library/
├── core/           # Node, State (Protocol), SearchProblem (ABC), SearchResult
├── algorithms/     # A* implementation (extensible for BFS, DFS, Dijkstra)
├── heuristics/     # Heuristic ABC + Manhattan + Euclidean
├── graph/          # Graph + Edge + GraphSearchProblem adapter
├── grid/           # Grid + GridSearchProblem adapter (4/8 directions)
├── utils/          # Formatting helpers
└── exceptions/     # SearchError hierarchy
```

### Design Principles

- **SOLID** — each class has a single responsibility; open for extension, closed for modification
- **Strategy Pattern** — heuristics are interchangeable at runtime
- **Adapter Pattern** — Graph and Grid adapt to the unified SearchProblem interface
- **Generic Types** — algorithms work with any hashable state type

## Development

```bash
# Install all dependencies (including dev tools)
uv sync

# Run tests with coverage
uv run pytest

# Lint
uv run ruff check src/ tests/

# Format
uv run ruff format src/ tests/

# Type check (strict mode)
uv run mypy src/

# Build wheel + sdist
uv build
```

## CI/CD

| Pipeline | Trigger | What it does |
|----------|---------|--------------|
| **CI** | push, PR | Ruff + MyPy + Pytest (matrix: 3.11, 3.12, 3.13, 3.14) |
| **CD** | push to main | CI + Semantic Release + PyPI publish |

Versioning follows [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` → minor version bump
- `fix:` → patch version bump
- `feat!:` / `BREAKING CHANGE:` → major version bump

## Roadmap

- [x] A* Search Algorithm
- [x] Manhattan & Euclidean heuristics
- [x] Graph support (directed/undirected, weighted)
- [x] Grid support (4/8 directions, obstacles)
- [ ] BFS (Breadth-First Search)
- [ ] DFS (Depth-First Search)
- [ ] Dijkstra's Algorithm
- [ ] Bidirectional Search
- [ ] Visualization utilities

## License

[MIT](LICENSE) — free for academic and commercial use.
