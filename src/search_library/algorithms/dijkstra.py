"""Dijkstra's algorithm implementation."""

from __future__ import annotations

import heapq

from search_library.algorithms.base import SearchAlgorithm
from search_library.core.nodes import Node
from search_library.core.problem import SearchProblem
from search_library.core.result import SearchResult
from search_library.core.types import T
from search_library.exceptions.exceptions import NoSolutionFoundError, SearchTimeoutError


class Dijkstra(SearchAlgorithm[T]):
    """Dijkstra's shortest path algorithm.

    Equivalent to A* with h(n)=0. Uses a priority queue ordered by g(n)
    to find the optimal path in weighted graphs with non-negative edges.

    Complexity:
        Time:  O((V + E) log V) with binary heap
        Space: O(V) for distances and priority queue

    Use cases:
        - Shortest path in weighted graphs
        - When no admissible heuristic is available
        - Network routing
    """

    def __init__(self, problem: SearchProblem[T]) -> None:
        """Initialize Dijkstra with a search problem.

        Args:
            problem: The search problem to solve.
        """
        super().__init__(problem)

    def search(
        self,
        *,
        max_iterations: int | None = None,
        strict: bool = False,
        track_explored: bool = False,
    ) -> SearchResult[T]:
        """Execute Dijkstra's algorithm.

        Args:
            max_iterations: Maximum node expansions before aborting.
            strict: If True, raises exceptions on failure.
            track_explored: If True, populates explored_states in result.

        Returns:
            SearchResult with the optimal path (minimum cost).
        """
        initial = self._problem.initial_state()

        if self._problem.is_goal(initial):
            return SearchResult(
                path=[initial],
                total_cost=0.0,
                nodes_explored=1,
                success=True,
                explored_states=frozenset({initial}) if track_explored else None,
            )

        counter = 0
        start_node = Node(state=initial, g_cost=0.0, h_cost=0.0)
        open_list: list[tuple[float, int, Node[T]]] = []
        heapq.heappush(open_list, (0.0, counter, start_node))

        g_scores: dict[T, float] = {initial: 0.0}
        came_from: dict[T, T] = {}
        closed_set: set[T] = set()
        iterations = 0

        while open_list:
            if max_iterations is not None and iterations >= max_iterations:
                if strict:
                    raise SearchTimeoutError(max_iterations)
                return SearchResult(
                    path=[],
                    total_cost=0.0,
                    nodes_explored=len(closed_set),
                    success=False,
                    explored_states=frozenset(closed_set) if track_explored else None,
                )

            _, _, current = heapq.heappop(open_list)

            if current.state in closed_set:
                continue

            closed_set.add(current.state)
            iterations += 1

            if self._problem.is_goal(current.state):
                path = self._reconstruct_path(came_from, initial, current.state)
                return SearchResult(
                    path=path,
                    total_cost=current.g_cost,
                    nodes_explored=len(closed_set),
                    success=True,
                    explored_states=frozenset(closed_set) if track_explored else None,
                )

            for successor_state, step_cost in self._problem.successors(current.state):
                if successor_state in closed_set:
                    continue

                tentative_g = current.g_cost + step_cost

                if tentative_g < g_scores.get(successor_state, float("inf")):
                    g_scores[successor_state] = tentative_g
                    came_from[successor_state] = current.state

                    successor_node = Node(
                        state=successor_state, g_cost=tentative_g, h_cost=0.0
                    )
                    counter += 1
                    heapq.heappush(open_list, (tentative_g, counter, successor_node))

        if strict:
            raise NoSolutionFoundError()
        return SearchResult(
            path=[],
            total_cost=0.0,
            nodes_explored=len(closed_set),
            success=False,
            explored_states=frozenset(closed_set) if track_explored else None,
        )


def dijkstra_search(
    problem: SearchProblem[T],
    *,
    max_iterations: int | None = None,
    strict: bool = False,
    track_explored: bool = False,
) -> SearchResult[T]:
    """Convenience function for Dijkstra's algorithm."""
    return Dijkstra(problem).search(
        max_iterations=max_iterations, strict=strict, track_explored=track_explored
    )
