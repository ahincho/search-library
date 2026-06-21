"""Tests for Dijkstra's algorithm."""

import pytest

from search_library.algorithms.dijkstra import Dijkstra, dijkstra_search
from search_library.exceptions import NoSolutionFoundError
from search_library.graph.graph import Graph
from search_library.grid.grid import Grid
from search_library.grid.grid_search import GridSearchProblem


class TestDijkstra:
    """Tests for Dijkstra's Algorithm."""

    def test_simple_weighted_graph(self) -> None:
        g = Graph[str](directed=False)
        g.add_edge("A", "B", 1.0)
        g.add_edge("B", "C", 2.0)
        g.add_edge("A", "C", 5.0)

        problem = g.to_search_problem("A", "C")
        result = Dijkstra(problem).search()

        assert result.success is True
        assert result.path == ["A", "B", "C"]
        assert result.total_cost == 3.0

    def test_optimal_path_in_complex_graph(self) -> None:
        g = Graph[str](directed=True)
        g.add_edge("S", "A", 1.0)
        g.add_edge("S", "B", 4.0)
        g.add_edge("A", "B", 2.0)
        g.add_edge("A", "C", 5.0)
        g.add_edge("B", "C", 1.0)
        g.add_edge("C", "G", 3.0)

        problem = g.to_search_problem("S", "G")
        result = Dijkstra(problem).search()

        assert result.success is True
        assert result.total_cost == 7.0
        assert result.path == ["S", "A", "B", "C", "G"]

    def test_same_result_as_astar_no_heuristic(self) -> None:
        """Dijkstra should produce same optimal cost as A* with h=0."""
        from search_library.algorithms.astar import AStarSearch

        g = Graph[str](directed=False)
        g.add_edge("A", "B", 3.0)
        g.add_edge("A", "C", 1.0)
        g.add_edge("C", "D", 1.0)
        g.add_edge("B", "D", 1.0)
        g.add_edge("D", "E", 2.0)

        problem = g.to_search_problem("A", "E")
        dijkstra_result = Dijkstra(problem).search()
        astar_result = AStarSearch(problem).search()

        assert dijkstra_result.total_cost == astar_result.total_cost

    def test_no_path(self) -> None:
        g = Graph[str](directed=True)
        g.add_edge("A", "B", 1.0)
        g.add_node("C")

        problem = g.to_search_problem("A", "C")
        result = Dijkstra(problem).search()

        assert result.success is False

    def test_start_is_goal(self) -> None:
        g = Graph[str]()
        g.add_node("A")
        problem = g.to_search_problem("A", "A")
        result = Dijkstra(problem).search()

        assert result.success is True
        assert result.path == ["A"]
        assert result.total_cost == 0.0

    def test_grid_search(self) -> None:
        grid = Grid(5, 5)
        problem = GridSearchProblem(grid, (0, 0), (4, 4))
        result = Dijkstra(problem).search()

        assert result.success is True
        assert result.total_cost == 8.0  # Same as A* for uniform grid

    def test_max_iterations(self) -> None:
        grid = Grid(100, 100)
        problem = GridSearchProblem(grid, (0, 0), (99, 99))
        result = Dijkstra(problem).search(max_iterations=10)

        assert result.success is False

    def test_strict_mode(self) -> None:
        g = Graph[str](directed=True)
        g.add_edge("A", "B", 1.0)
        g.add_node("C")
        problem = g.to_search_problem("A", "C")

        with pytest.raises(NoSolutionFoundError):
            Dijkstra(problem).search(strict=True)

    def test_convenience_function(self) -> None:
        g = Graph[str](directed=False)
        g.add_edge("A", "B", 1.0)
        g.add_edge("B", "C", 2.0)
        problem = g.to_search_problem("A", "C")

        result = dijkstra_search(problem)
        assert result.success is True
        assert result.total_cost == 3.0
