"""Tests for BFS algorithm."""

import pytest

from search_library.algorithms.bfs import BFS, bfs_search
from search_library.exceptions import NoSolutionFoundError, SearchTimeoutError
from search_library.graph.graph import Graph
from search_library.grid.grid import Grid
from search_library.grid.grid_search import GridSearchProblem


class TestBFS:
    """Tests for Breadth-First Search."""

    def test_simple_graph(self) -> None:
        g = Graph[str](directed=False)
        g.add_edge("A", "B", 1.0)
        g.add_edge("B", "C", 1.0)
        g.add_edge("A", "C", 1.0)

        problem = g.to_search_problem("A", "C")
        result = BFS(problem).search()

        assert result.success is True
        assert result.path[0] == "A"
        assert result.path[-1] == "C"
        # BFS finds shortest by edges: A->C directly
        assert len(result.path) == 2

    def test_graph_weighted_ignores_weights(self) -> None:
        """BFS finds shortest by edge count, not weight."""
        g = Graph[str](directed=False)
        g.add_edge("A", "B", 1.0)
        g.add_edge("B", "C", 1.0)
        g.add_edge("A", "C", 100.0)

        problem = g.to_search_problem("A", "C")
        result = BFS(problem).search()

        assert result.success is True
        # BFS finds A->C (1 edge) even though cost=100
        assert len(result.path) == 2

    def test_no_path(self) -> None:
        g = Graph[str](directed=True)
        g.add_edge("A", "B", 1.0)
        g.add_node("C")

        problem = g.to_search_problem("A", "C")
        result = BFS(problem).search()

        assert result.success is False
        assert result.path == []

    def test_start_is_goal(self) -> None:
        g = Graph[str]()
        g.add_node("A")
        problem = g.to_search_problem("A", "A")
        result = BFS(problem).search()

        assert result.success is True
        assert result.path == ["A"]
        assert result.total_cost == 0.0

    def test_grid_search(self) -> None:
        grid = Grid(5, 5)
        problem = GridSearchProblem(grid, (0, 0), (4, 4))
        result = BFS(problem).search()

        assert result.success is True
        assert result.path[0] == (0, 0)
        assert result.path[-1] == (4, 4)

    def test_grid_with_obstacles(self) -> None:
        matrix = [[0, 0, 0], [1, 1, 0], [0, 0, 0]]
        grid = Grid.from_matrix(matrix)
        problem = GridSearchProblem(grid, (0, 0), (2, 0))
        result = BFS(problem).search()

        assert result.success is True
        for pos in result.path:
            assert not grid.is_obstacle(pos[0], pos[1])

    def test_max_iterations(self) -> None:
        grid = Grid(100, 100)
        problem = GridSearchProblem(grid, (0, 0), (99, 99))
        result = BFS(problem).search(max_iterations=10)

        assert result.success is False

    def test_strict_no_solution(self) -> None:
        g = Graph[str](directed=True)
        g.add_edge("A", "B", 1.0)
        g.add_node("C")
        problem = g.to_search_problem("A", "C")

        with pytest.raises(NoSolutionFoundError):
            BFS(problem).search(strict=True)

    def test_strict_timeout(self) -> None:
        grid = Grid(100, 100)
        problem = GridSearchProblem(grid, (0, 0), (99, 99))

        with pytest.raises(SearchTimeoutError):
            BFS(problem).search(max_iterations=5, strict=True)

    def test_convenience_function(self) -> None:
        g = Graph[str](directed=False)
        g.add_edge("A", "B", 1.0)
        g.add_edge("B", "C", 1.0)
        problem = g.to_search_problem("A", "C")

        result = bfs_search(problem)
        assert result.success is True

    def test_track_explored(self) -> None:
        g = Graph[str](directed=False)
        g.add_edge("A", "B", 1.0)
        g.add_edge("B", "C", 1.0)
        problem = g.to_search_problem("A", "C")

        result = bfs_search(problem, track_explored=True)
        assert result.explored_states is not None
        assert "A" in result.explored_states
