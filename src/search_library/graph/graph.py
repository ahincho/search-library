"""Graph data structure for search problems."""

from __future__ import annotations

from typing import Generic, TypeVar

from search_library.core.problem import SearchProblem
from search_library.graph.edges import Edge
from search_library.heuristics.base import Heuristic

T = TypeVar("T")


class Graph(Generic[T]):
    """Weighted directed graph supporting search operations.

    Stores nodes and weighted edges. Can be used as directed or undirected.

    Attributes:
        directed: Whether the graph is directed.
    """

    def __init__(self, directed: bool = True) -> None:
        """Initialize an empty graph.

        Args:
            directed: If True, edges are one-way. If False, edges are added
                      in both directions automatically.
        """
        self.directed = directed
        self._adjacency: dict[T, list[tuple[T, float]]] = {}

    @property
    def nodes(self) -> set[T]:
        """Return the set of all nodes in the graph."""
        return set(self._adjacency.keys())

    @property
    def node_count(self) -> int:
        """Return the number of nodes in the graph."""
        return len(self._adjacency)

    def add_node(self, node: T) -> None:
        """Add a node to the graph.

        Args:
            node: The node identifier to add.
        """
        if node not in self._adjacency:
            self._adjacency[node] = []

    def add_edge(self, source: T, target: T, weight: float = 1.0) -> None:
        """Add a weighted edge to the graph.

        Args:
            source: The source node.
            target: The target node.
            weight: The edge weight (must be non-negative).

        Raises:
            ValueError: If weight is negative.
        """
        if weight < 0:
            msg = f"Edge weight must be non-negative, got {weight}"
            raise ValueError(msg)

        self.add_node(source)
        self.add_node(target)
        self._adjacency[source].append((target, weight))

        if not self.directed:
            self._adjacency[target].append((source, weight))

    def add_edge_from(self, edge: Edge[T]) -> None:
        """Add an edge from an Edge object.

        Args:
            edge: The Edge instance to add.
        """
        self.add_edge(edge.source, edge.target, edge.weight)

    def neighbors(self, node: T) -> list[tuple[T, float]]:
        """Get the neighbors of a node with their edge weights.

        Args:
            node: The node to query.

        Returns:
            List of (neighbor, weight) tuples.

        Raises:
            KeyError: If the node is not in the graph.
        """
        if node not in self._adjacency:
            msg = f"Node {node!r} not found in graph"
            raise KeyError(msg)
        return list(self._adjacency[node])

    def has_node(self, node: T) -> bool:
        """Check if a node exists in the graph.

        Args:
            node: The node to check.

        Returns:
            True if the node exists, False otherwise.
        """
        return node in self._adjacency

    def has_edge(self, source: T, target: T) -> bool:
        """Check if an edge exists between two nodes.

        Args:
            source: The source node.
            target: The target node.

        Returns:
            True if the edge exists, False otherwise.
        """
        if source not in self._adjacency:
            return False
        return any(neighbor == target for neighbor, _ in self._adjacency[source])

    def to_search_problem(
        self, start: T, goal: T, heuristic: Heuristic[T] | None = None
    ) -> GraphSearchProblem[T]:
        """Create a SearchProblem from this graph.

        Args:
            start: The starting node.
            goal: The goal node.
            heuristic: Optional heuristic function for informed search.

        Returns:
            A GraphSearchProblem instance.

        Raises:
            KeyError: If start or goal are not in the graph.
        """
        if not self.has_node(start):
            msg = f"Start node {start!r} not found in graph"
            raise KeyError(msg)
        if not self.has_node(goal):
            msg = f"Goal node {goal!r} not found in graph"
            raise KeyError(msg)
        return GraphSearchProblem(self, start, goal, heuristic)


class GraphSearchProblem(SearchProblem[T]):
    """A search problem defined over a graph.

    Adapts a Graph instance to the SearchProblem interface,
    allowing it to be used with any search algorithm.
    """

    def __init__(
        self,
        graph: Graph[T],
        start: T,
        goal: T,
        heuristic: Heuristic[T] | None = None,
    ) -> None:
        """Initialize the graph search problem.

        Args:
            graph: The graph to search.
            start: The starting node.
            goal: The goal node.
            heuristic: Optional heuristic for informed search.
        """
        self._graph = graph
        self._start = start
        self._goal = goal
        self._heuristic = heuristic

    def initial_state(self) -> T:
        """Return the start node."""
        return self._start

    def is_goal(self, state: T) -> bool:
        """Check if state is the goal node."""
        return state == self._goal

    def successors(self, state: T) -> list[tuple[T, float]]:
        """Return neighbors and their edge weights."""
        return self._graph.neighbors(state)

    def heuristic(self, state: T) -> float:
        """Return heuristic estimate to goal."""
        if self._heuristic is None:
            return 0.0
        return self._heuristic.estimate(state, self._goal)
