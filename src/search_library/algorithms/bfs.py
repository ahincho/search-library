"""Breadth-First Search (BFS) algorithm implementation."""

from __future__ import annotations

from collections import deque
from typing import Generic

from search_library.algorithms.base import SearchAlgorithm
from search_library.core.problem import SearchProblem
from search_library.core.result import SearchResult
from search_library.core.types import T
from search_library.exceptions.exceptions import NoSolutionFoundError, SearchTimeoutError


class BFS(SearchAlgorithm[T], Generic[T]):
    """Breadth-First Search algorithm.

    Explores nodes level by level using a FIFO queue. Guarantees the
    shortest path (fewest edges) in unweighted graphs.

    Complexity:
        Time:  O(V + E) where V = vertices, E = edges
        Space: O(V) for the visited set and queue

    Use cases:
        - Shortest path in unweighted graphs
        - Finding if a path exists between two nodes
        - Level-order traversal
        - Problems where all edges have equal cost
    """

    def __init__(self, problem: SearchProblem[T]) -> None:
        """Initialize BFS with a search problem.

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
        """Execute BFS.

        Args:
            max_iterations: Maximum node expansions before aborting.
            strict: If True, raises exceptions on failure.
            track_explored: If True, populates explored_states in result.

        Returns:
            SearchResult with the shortest path (by edge count).
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

        # FIFO queue: stores (state, cost_so_far)
        queue: deque[tuple[T, float]] = deque([(initial, 0.0)])
        visited: set[T] = {initial}
        came_from: dict[T, T] = {}
        cost_to: dict[T, float] = {initial: 0.0}
        iterations = 0

        while queue:
            if max_iterations is not None and iterations >= max_iterations:
                if strict:
                    raise SearchTimeoutError(max_iterations)
                return SearchResult(
                    path=[],
                    total_cost=0.0,
                    nodes_explored=len(visited),
                    success=False,
                    explored_states=frozenset(visited) if track_explored else None,
                )

            current, current_cost = queue.popleft()
            iterations += 1

            for successor, step_cost in self._problem.successors(current):
                if successor in visited:
                    continue

                visited.add(successor)
                came_from[successor] = current
                new_cost = current_cost + step_cost
                cost_to[successor] = new_cost

                if self._problem.is_goal(successor):
                    path = self._reconstruct_path(came_from, initial, successor)
                    return SearchResult(
                        path=path,
                        total_cost=new_cost,
                        nodes_explored=len(visited),
                        success=True,
                        explored_states=frozenset(visited) if track_explored else None,
                    )

                queue.append((successor, new_cost))

        if strict:
            raise NoSolutionFoundError()
        return SearchResult(
            path=[],
            total_cost=0.0,
            nodes_explored=len(visited),
            success=False,
            explored_states=frozenset(visited) if track_explored else None,
        )

    @staticmethod
    def _reconstruct_path(came_from: dict[T, T], start: T, goal: T) -> list[T]:
        """Reconstruct path from came_from map."""
        path: list[T] = [goal]
        current = goal
        while current != start:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path


def bfs_search(
    problem: SearchProblem[T],
    *,
    max_iterations: int | None = None,
    strict: bool = False,
    track_explored: bool = False,
) -> SearchResult[T]:
    """Convenience function for BFS."""
    return BFS(problem).search(
        max_iterations=max_iterations, strict=strict, track_explored=track_explored
    )
