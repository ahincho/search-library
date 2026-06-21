# CHANGELOG


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
