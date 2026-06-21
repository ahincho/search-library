"""Tests for DFS algorithm."""

import pytest

from search_library.algorithms.dfs import DFS, dfs_search
from search_library.exceptions import NoSolutionFoundError
from search_library.graph.graph import Graph
from search_library.grid.grid import Grid
from search_library.grid.grid_search import GridSearchProblem


class TestDFS:
    """Tests for Depth-First Search."""

    def test_simple_graph(self) -> None:
        g = Graph[str](directed=False)
        g.add_edge("A", "B", 1.0)
        g.add_edge("B", "C", 1.0)

        problem = g.to_search_problem("A", "C")
        result = DFS(problem).search()

        assert result.success is True
        assert result.path[0] == "A"
        assert result.path[-1] == "C"

    def test_finds_path_not_necessarily_shortest(self) -> None:
        """DFS finds A path, not necessarily the shortest."""
        g = Graph[str](directed=False)
        g.add_edge("A", "B", 1.0)
        g.add_edge("A", "C", 1.0)
        g.add_edge("B", "D", 1.0)
        g.add_edge("C", "D", 1.0)

        problem = g.to_search_problem("A", "D")
        result = DFS(problem).search()

        assert result.success is True
        assert result.path[0] == "A"
        assert result.path[-1] == "D"
        # DFS may find longer path, that's OK

    def test_no_path(self) -> None:
        g = Graph[str](directed=True)
        g.add_edge("A", "B", 1.0)
        g.add_node("C")

        problem = g.to_search_problem("A", "C")
        result = DFS(problem).search()

        assert result.success is False
        assert result.path == []

    def test_start_is_goal(self) -> None:
        g = Graph[str]()
        g.add_node("A")
        problem = g.to_search_problem("A", "A")
        result = DFS(problem).search()

        assert result.success is True
        assert result.path == ["A"]

    def test_grid_search(self) -> None:
        grid = Grid(5, 5)
        problem = GridSearchProblem(grid, (0, 0), (4, 4))
        result = DFS(problem).search()

        assert result.success is True
        assert result.path[0] == (0, 0)
        assert result.path[-1] == (4, 4)

    def test_grid_no_path(self) -> None:
        matrix = [[0, 0, 0], [0, 1, 1], [0, 1, 0]]
        grid = Grid.from_matrix(matrix)
        problem = GridSearchProblem(grid, (0, 0), (2, 2))
        result = DFS(problem).search()

        assert result.success is False

    def test_max_iterations(self) -> None:
        grid = Grid(50, 50)
        problem = GridSearchProblem(grid, (0, 0), (49, 49))
        result = DFS(problem).search(max_iterations=10)

        assert result.success is False

    def test_strict_mode(self) -> None:
        g = Graph[str](directed=True)
        g.add_edge("A", "B", 1.0)
        g.add_node("C")
        problem = g.to_search_problem("A", "C")

        with pytest.raises(NoSolutionFoundError):
            DFS(problem).search(strict=True)

    def test_convenience_function(self) -> None:
        g = Graph[str](directed=False)
        g.add_edge("A", "B", 1.0)
        g.add_edge("B", "C", 1.0)
        problem = g.to_search_problem("A", "C")

        result = dfs_search(problem)
        assert result.success is True

    def test_track_explored(self) -> None:
        g = Graph[str](directed=False)
        g.add_edge("A", "B", 1.0)
        g.add_edge("B", "C", 1.0)
        problem = g.to_search_problem("A", "C")

        result = dfs_search(problem, track_explored=True)
        assert result.explored_states is not None
