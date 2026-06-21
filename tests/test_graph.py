"""Tests for graph module."""

import pytest

from search_library.algorithms.astar import AStarSearch, astar_search
from search_library.graph.edges import Edge
from search_library.graph.graph import Graph


class TestEdge:
    """Tests for Edge class."""

    def test_edge_creation(self) -> None:
        edge = Edge(source="A", target="B", weight=2.5)
        assert edge.source == "A"
        assert edge.target == "B"
        assert edge.weight == 2.5

    def test_edge_default_weight(self) -> None:
        edge = Edge(source="A", target="B")
        assert edge.weight == 1.0

    def test_edge_negative_weight_raises(self) -> None:
        with pytest.raises(ValueError, match="non-negative"):
            Edge(source="A", target="B", weight=-1.0)

    def test_edge_reversed(self) -> None:
        edge = Edge(source="A", target="B", weight=3.0)
        rev = edge.reversed()
        assert rev.source == "B"
        assert rev.target == "A"
        assert rev.weight == 3.0

    def test_edge_is_frozen(self) -> None:
        edge = Edge(source="A", target="B")
        with pytest.raises(Exception):  # noqa: B017
            edge.weight = 5.0  # type: ignore[misc]


class TestGraph:
    """Tests for Graph class."""

    def test_empty_graph(self) -> None:
        g = Graph[str]()
        assert g.node_count == 0
        assert g.nodes == set()

    def test_add_node(self) -> None:
        g = Graph[str]()
        g.add_node("A")
        assert g.has_node("A")
        assert g.node_count == 1

    def test_add_edge_directed(self) -> None:
        g = Graph[str](directed=True)
        g.add_edge("A", "B", 2.0)
        assert g.has_edge("A", "B")
        assert not g.has_edge("B", "A")

    def test_add_edge_undirected(self) -> None:
        g = Graph[str](directed=False)
        g.add_edge("A", "B", 2.0)
        assert g.has_edge("A", "B")
        assert g.has_edge("B", "A")

    def test_add_edge_creates_nodes(self) -> None:
        g = Graph[str]()
        g.add_edge("A", "B")
        assert g.has_node("A")
        assert g.has_node("B")

    def test_add_edge_negative_weight_raises(self) -> None:
        g = Graph[str]()
        with pytest.raises(ValueError, match="non-negative"):
            g.add_edge("A", "B", -1.0)

    def test_neighbors(self) -> None:
        g = Graph[str]()
        g.add_edge("A", "B", 1.0)
        g.add_edge("A", "C", 2.0)
        neighbors = g.neighbors("A")
        assert ("B", 1.0) in neighbors
        assert ("C", 2.0) in neighbors

    def test_neighbors_unknown_node_raises(self) -> None:
        g = Graph[str]()
        with pytest.raises(KeyError):
            g.neighbors("X")

    def test_has_edge_nonexistent_source(self) -> None:
        g = Graph[str]()
        assert not g.has_edge("X", "Y")

    def test_add_edge_from_object(self) -> None:
        g = Graph[str]()
        edge = Edge(source="A", target="B", weight=3.0)
        g.add_edge_from(edge)
        assert g.has_edge("A", "B")
        neighbors = g.neighbors("A")
        assert ("B", 3.0) in neighbors

    def test_add_duplicate_node(self) -> None:
        g = Graph[str]()
        g.add_node("A")
        g.add_node("A")
        assert g.node_count == 1

    def test_get_edge_weight(self) -> None:
        g = Graph[str]()
        g.add_edge("A", "B", 5.0)
        assert g.get_edge_weight("A", "B") == 5.0
        assert g.get_edge_weight("A", "C") is None
        assert g.get_edge_weight("X", "Y") is None

    def test_has_edge_o1_performance(self) -> None:
        """Verify has_edge uses O(1) dict lookup."""
        g = Graph[int]()
        for i in range(1000):
            g.add_edge(0, i, 1.0)
        # This should be fast (O(1) not O(n))
        assert g.has_edge(0, 999)
        assert not g.has_edge(0, 1000)


class TestGraphSearchProblem:
    """Tests for graph-based search with A*."""

    def test_simple_graph_search(self) -> None:
        g = Graph[str](directed=False)
        g.add_edge("A", "B", 1.0)
        g.add_edge("B", "C", 1.0)
        g.add_edge("A", "C", 3.0)

        problem = g.to_search_problem("A", "C")
        solver = AStarSearch(problem)
        result = solver.search()

        assert result.success is True
        assert result.path == ["A", "B", "C"]
        assert result.total_cost == 2.0

    def test_complex_graph_search(self) -> None:
        """Test with a graph that has multiple paths."""
        g = Graph[str](directed=True)
        g.add_edge("S", "A", 1.0)
        g.add_edge("S", "B", 4.0)
        g.add_edge("A", "B", 2.0)
        g.add_edge("A", "C", 5.0)
        g.add_edge("B", "C", 1.0)
        g.add_edge("C", "G", 3.0)

        problem = g.to_search_problem("S", "G")
        solver = AStarSearch(problem)
        result = solver.search()

        assert result.success is True
        assert result.total_cost == 7.0  # S->A->B->C->G = 1+2+1+3
        assert result.path == ["S", "A", "B", "C", "G"]

    def test_graph_no_path(self) -> None:
        g = Graph[str](directed=True)
        g.add_edge("A", "B", 1.0)
        g.add_node("C")

        problem = g.to_search_problem("A", "C")
        solver = AStarSearch(problem)
        result = solver.search()

        assert result.success is False
        assert result.path == []

    def test_start_equals_goal(self) -> None:
        g = Graph[str]()
        g.add_node("A")

        problem = g.to_search_problem("A", "A")
        solver = AStarSearch(problem)
        result = solver.search()

        assert result.success is True
        assert result.path == ["A"]
        assert result.total_cost == 0.0

    def test_to_search_problem_invalid_start(self) -> None:
        g = Graph[str]()
        g.add_node("B")
        with pytest.raises(KeyError, match="Start node"):
            g.to_search_problem("X", "B")

    def test_to_search_problem_invalid_goal(self) -> None:
        g = Graph[str]()
        g.add_node("A")
        with pytest.raises(KeyError, match="Goal node"):
            g.to_search_problem("A", "X")

    def test_weighted_graph_optimal_path(self) -> None:
        """Ensure A* finds optimal path, not shortest hop count."""
        g = Graph[str](directed=False)
        g.add_edge("A", "C", 10.0)
        g.add_edge("A", "B", 3.0)
        g.add_edge("B", "C", 4.0)

        problem = g.to_search_problem("A", "C")
        solver = AStarSearch(problem)
        result = solver.search()

        assert result.success is True
        assert result.total_cost == 7.0
        assert result.path == ["A", "B", "C"]

    def test_astar_search_convenience_function(self) -> None:
        """Test the astar_search() convenience function."""
        g = Graph[str](directed=False)
        g.add_edge("A", "B", 1.0)
        g.add_edge("B", "C", 1.0)

        problem = g.to_search_problem("A", "C")
        result = astar_search(problem)

        assert result.success is True
        assert result.path == ["A", "B", "C"]
        assert result.total_cost == 2.0

    def test_track_explored_states(self) -> None:
        """Test that track_explored populates explored_states."""
        g = Graph[str](directed=False)
        g.add_edge("A", "B", 1.0)
        g.add_edge("B", "C", 1.0)

        problem = g.to_search_problem("A", "C")

        # Default: no explored states
        result = astar_search(problem)
        assert result.explored_states is None

        # With tracking
        result = astar_search(problem, track_explored=True)
        assert result.explored_states is not None
        assert "A" in result.explored_states
