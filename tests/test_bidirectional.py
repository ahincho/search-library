"""Tests for Bidirectional Search algorithm."""

import pytest

from search_library.algorithms.bidirectional import BidirectionalSearch, bidirectional_search
from search_library.exceptions import NoSolutionFoundError
from search_library.graph.graph import Graph
from search_library.grid.grid import Grid
from search_library.grid.grid_search import GridSearchProblem


class TestBidirectionalSearch:
    """Tests for Bidirectional BFS Search."""

    def test_simple_undirected_graph(self) -> None:
        g = Graph[str](directed=False)
        g.add_edge("A", "B", 1.0)
        g.add_edge("B", "C", 1.0)
        g.add_edge("C", "D", 1.0)

        forward = g.to_search_problem("A", "D")
        reverse = g.to_search_problem("D", "A")
        result = BidirectionalSearch(forward, reverse_problem=reverse).search()

        assert result.success is True
        assert result.path[0] == "A"
        assert result.path[-1] == "D"

    def test_finds_path_in_undirected_grid(self) -> None:
        grid = Grid(5, 5)
        forward = GridSearchProblem(grid, (0, 0), (4, 4))
        reverse = GridSearchProblem(grid, (4, 4), (0, 0))
        result = BidirectionalSearch(forward, reverse_problem=reverse).search()

        assert result.success is True
        assert result.path[0] == (0, 0)
        assert result.path[-1] == (4, 4)

    def test_start_is_goal(self) -> None:
        g = Graph[str](directed=False)
        g.add_node("A")
        forward = g.to_search_problem("A", "A")
        result = BidirectionalSearch(forward).search()

        assert result.success is True
        assert result.path == ["A"]

    def test_no_path_directed_graph(self) -> None:
        g = Graph[str](directed=True)
        g.add_edge("A", "B", 1.0)
        g.add_node("C")

        forward = g.to_search_problem("A", "C")
        reverse = g.to_search_problem("C", "A")
        result = BidirectionalSearch(forward, reverse_problem=reverse).search()

        assert result.success is False

    def test_max_iterations(self) -> None:
        grid = Grid(50, 50)
        forward = GridSearchProblem(grid, (0, 0), (49, 49))
        reverse = GridSearchProblem(grid, (49, 49), (0, 0))
        result = BidirectionalSearch(forward, reverse_problem=reverse).search(
            max_iterations=5
        )

        assert result.success is False

    def test_strict_no_solution(self) -> None:
        g = Graph[str](directed=True)
        g.add_edge("A", "B", 1.0)
        g.add_node("C")
        forward = g.to_search_problem("A", "C")
        reverse = g.to_search_problem("C", "A")

        with pytest.raises(NoSolutionFoundError):
            BidirectionalSearch(forward, reverse_problem=reverse).search(strict=True)

    def test_fewer_nodes_explored_than_bfs(self) -> None:
        """Bidirectional should explore fewer nodes than unidirectional BFS."""
        from search_library.algorithms.bfs import BFS

        grid = Grid(10, 10)
        forward = GridSearchProblem(grid, (0, 0), (9, 9))
        reverse = GridSearchProblem(grid, (9, 9), (0, 0))

        bfs_result = BFS(forward).search(track_explored=True)
        bidir_result = BidirectionalSearch(forward, reverse_problem=reverse).search(
            track_explored=True
        )

        assert bidir_result.success is True
        assert bfs_result.success is True
        # Bidirectional typically explores fewer nodes
        assert bidir_result.nodes_explored <= bfs_result.nodes_explored

    def test_convenience_function(self) -> None:
        g = Graph[str](directed=False)
        g.add_edge("A", "B", 1.0)
        g.add_edge("B", "C", 1.0)
        forward = g.to_search_problem("A", "C")
        reverse = g.to_search_problem("C", "A")

        result = bidirectional_search(forward, reverse_problem=reverse)
        assert result.success is True

    def test_without_reverse_problem(self) -> None:
        """When no reverse_problem, uses _find_goal fallback."""
        g = Graph[str](directed=False)
        g.add_edge("A", "B", 1.0)
        g.add_edge("B", "C", 1.0)
        forward = g.to_search_problem("A", "C")

        result = BidirectionalSearch(forward).search()
        assert result.success is True
        assert result.path[0] == "A"
        assert result.path[-1] == "C"
