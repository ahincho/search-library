"""Tests for core module: Node, SearchResult."""

from search_library.core.nodes import Node
from search_library.core.result import SearchResult


class TestNode:
    """Tests for the Node class."""

    def test_node_creation(self) -> None:
        node = Node(state="A", g_cost=0.0, h_cost=5.0)
        assert node.state == "A"
        assert node.g_cost == 0.0
        assert node.h_cost == 5.0
        assert node.f_cost == 5.0

    def test_node_f_cost_calculation(self) -> None:
        node = Node(state="B", g_cost=3.0, h_cost=4.0)
        assert node.f_cost == 7.0

    def test_node_comparison(self) -> None:
        node_a = Node(state="A", g_cost=1.0, h_cost=3.0)  # f=4
        node_b = Node(state="B", g_cost=2.0, h_cost=5.0)  # f=7
        assert node_a < node_b
        assert node_a <= node_b
        assert not node_b < node_a

    def test_node_comparison_equal_f(self) -> None:
        node_a = Node(state="A", g_cost=2.0, h_cost=3.0)  # f=5
        node_b = Node(state="B", g_cost=1.0, h_cost=4.0)  # f=5
        assert not node_a < node_b
        assert node_a <= node_b

    def test_node_comparison_not_implemented(self) -> None:
        node = Node(state="A", g_cost=1.0, h_cost=1.0)
        assert node.__lt__(42) is NotImplemented
        assert node.__le__("x") is NotImplemented


class TestSearchResult:
    """Tests for SearchResult."""

    def test_successful_result(self) -> None:
        result = SearchResult(
            path=["A", "B", "C"],
            total_cost=5.0,
            nodes_explored=10,
            success=True,
            explored_states=frozenset({"A", "B", "C", "D"}),
        )
        assert result.success is True
        assert result.path_length == 3
        assert result.steps == 2
        assert result.total_cost == 5.0
        assert result.nodes_explored == 10
        assert result.explored_states is not None

    def test_failed_result(self) -> None:
        result = SearchResult(
            path=[],
            total_cost=0.0,
            nodes_explored=5,
            success=False,
        )
        assert result.success is False
        assert result.path_length == 0
        assert result.steps == 0
        assert result.explored_states is None

    def test_single_node_result(self) -> None:
        result = SearchResult(
            path=["A"],
            total_cost=0.0,
            nodes_explored=1,
            success=True,
        )
        assert result.path_length == 1
        assert result.steps == 0

    def test_explored_states_default_none(self) -> None:
        result = SearchResult(path=[], success=False)
        assert result.explored_states is None
