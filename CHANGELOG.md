# CHANGELOG


## v1.0.0 (2026-06-21)

### Bug Fixes

- Critical correctness and consistency fixes for v1.0 - DFS: store parent on stack to prevent
  came_from overwrite in multi-path graphs - Bidirectional: require reverse_problem explicitly
  (remove fragile _find_goal) - Bidirectional: recalculate total_cost from actual path edges for
  correctness - AStarSearch: now inherits from SearchAlgorithm for polymorphic consistency - Extract
  _reconstruct_path to SearchAlgorithm base (DRY across all algorithms) - Remove dead code (cost_to
  dict in BFS, redundant Generic[T]) - Export SearchAlgorithm in algorithms __init__ BREAKING:
  BidirectionalSearch now requires reverse_problem keyword argument
  ([`4e1ea51`](https://github.com/ahincho/search-library/commit/4e1ea518d48313e98dc4bad45fae715d02f8c860))

### Chores

- **release**: Prepare v1.0 stable release - Update pyproject.toml metadata (description, keywords,
  status Beta) - Add __version__ = '1.0.0' to package __init__ - Rewrite README.md as academic
  reference documentation - Include algorithm comparison table, architecture diagram, usage examples
  - Add references to foundational papers (Hart et al., Russell & Norvig) - All 147 tests passing,
  96%+ coverage, mypy strict, ruff clean
  ([`c028210`](https://github.com/ahincho/search-library/commit/c0282106fee666195a82b7666acb767513d56a30))

### Features

- Implement BFS, DFS, Dijkstra, Bidirectional Search and visualization utilities - BFS: shortest
  path by edge count using FIFO queue (deque) - DFS: depth-first exploration using LIFO stack -
  Dijkstra: optimal weighted path using priority queue (heapq) - Bidirectional Search: simultaneous
  BFS from start and goal - SearchAlgorithm ABC: unified interface for all algorithms -
  Visualization: render_grid(), render_search_result(), print_grid() - All algorithms support
  max_iterations, strict mode, track_explored - Convenience functions: bfs_search(), dfs_search(),
  dijkstra_search(), bidirectional_search() - 146 tests passing, 96%+ coverage
  ([`6e4487b`](https://github.com/ahincho/search-library/commit/6e4487b13a06c3bce970bd453a3a523ccaf2a44d))

- Release v1.0 stable with complete algorithm suite BREAKING CHANGE: BidirectionalSearch now
  requires reverse_problem parameter. - Format all files for CI consistency - Complete framework:
  A*, BFS, DFS, Dijkstra, Bidirectional Search - Academic README with references and architecture
  documentation - 147 tests, 96%+ coverage, mypy strict, ruff clean - Production-ready for academic
  and professional use
  ([`0809e78`](https://github.com/ahincho/search-library/commit/0809e782d508b191cf3f413b52565025071f207d))


## v0.2.0 (2026-06-21)

### Features

- Apply code review improvements for production readiness - Grid: diagonal movements now cost
  sqrt(2) for geometric correctness - Type safety: TypeVar bound=Hashable prevents runtime errors
  with unhashable states - Memory: replaced Node parent chain with external came_from dict - Search
  limits: added max_iterations parameter to prevent runaway searches - SearchResult: explored_states
  is now optional (None by default) to save memory - Graph: internal structure migrated to dict[T,
  dict[T, float]] for O(1) has_edge - Exceptions: added strict mode that raises
  NoSolutionFoundError/SearchTimeoutError - API: added astar_search() convenience function - Removed
  unused State protocol (replaced by TypeVar bound)
  ([`39f8f11`](https://github.com/ahincho/search-library/commit/39f8f111e276991c33fbf59a8577f528daf9a2bc))


## v0.1.0 (2026-06-20)

### Bug Fixes

- Formatting for grid.py and add workflow_call trigger to CI
  ([`8d75c31`](https://github.com/ahincho/search-library/commit/8d75c314464b2b2090786a66ae4c3785c839d0d1))

- Use pip+build instead of uv in semantic-release container
  ([`a740379`](https://github.com/ahincho/search-library/commit/a74037961a15263a40bc9b86740afb2f25a9d6a7))

### Chores

- Add workflow_dispatch trigger to CD for manual releases
  ([`15c5bb0`](https://github.com/ahincho/search-library/commit/15c5bb020e562d4ea9906c190cffacde2a321349))

### Documentation

- Improve README with badges, examples, architecture and roadmap
  ([`e6e21ab`](https://github.com/ahincho/search-library/commit/e6e21abd928097180bd5ad6b1f81c2820a7f9fb6))

### Features

- Initial implementation of search-library with A* algorithm - Core abstractions: Node, State,
  SearchProblem, SearchResult - A* search algorithm with heapq priority queue (f=g+h) - Heuristics:
  Manhattan, Euclidean, extensible base ABC - Graph support: weighted directed/undirected graphs -
  Grid support: 2D pathfinding with obstacles, 4/8 directions - Custom exceptions and utility
  helpers - Full test suite (92 tests, 98.87% coverage) - Ruff + MyPy strict configuration - CI/CD:
  GitHub Actions (matrix 3.11-3.14) + semantic-release + PyPI - pyproject.toml with complete PyPI
  metadata (MIT license)
  ([`ae2c4e7`](https://github.com/ahincho/search-library/commit/ae2c4e794f1312e2297237ce0ebd3093908b8fc4))
