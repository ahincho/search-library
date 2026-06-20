# CHANGELOG


## v0.1.0 (2026-06-20)

### Bug Fixes

- Formatting for grid.py and add workflow_call trigger to CI
  ([`8d75c31`](https://github.com/ahincho/search-library/commit/8d75c314464b2b2090786a66ae4c3785c839d0d1))

- Use pip+build instead of uv in semantic-release container
  ([`a740379`](https://github.com/ahincho/search-library/commit/a74037961a15263a40bc9b86740afb2f25a9d6a7))

### Features

- Initial implementation of search-library with A* algorithm - Core abstractions: Node, State,
  SearchProblem, SearchResult - A* search algorithm with heapq priority queue (f=g+h) - Heuristics:
  Manhattan, Euclidean, extensible base ABC - Graph support: weighted directed/undirected graphs -
  Grid support: 2D pathfinding with obstacles, 4/8 directions - Custom exceptions and utility
  helpers - Full test suite (92 tests, 98.87% coverage) - Ruff + MyPy strict configuration - CI/CD:
  GitHub Actions (matrix 3.11-3.14) + semantic-release + PyPI - pyproject.toml with complete PyPI
  metadata (MIT license)
  ([`ae2c4e7`](https://github.com/ahincho/search-library/commit/ae2c4e794f1312e2297237ce0ebd3093908b8fc4))
