"""Depth-First Search (DFS) algorithm implementation."""

from __future__ import annotations

from typing import Generic

from search_library.algorithms.base import SearchAlgorithm
from search_library.core.problem import SearchProblem
from search_library.core.result import SearchResult
from search_library.core.types import T
from search_library.exceptions.exceptions import NoSolutionFoundError, SearchTimeoutError


class DFS(SearchAlgorithm[T], Generic[T]):
    """Depth-First Search algorithm.

    Explores as deep as possible along each branch before backtracking,
    using a LIFO stack. Does NOT guarantee optimal paths.

    Complexity:
        Time:  O(V + E) where V = vertices, E = edges
        Space: O(V) worst case for the stack (O(d) for branching factor b, depth d)

    Use cases:
        - Checking if a path exists (not necessarily shortest)
        - Topological sorting
        - Cycle detection
        - Maze generation/solving (finding any path)
        - Memory-constrained environments (lower space than BFS)
    """

    def __init__(self, problem: SearchProblem[T]) -> None:
        """Initialize DFS with a search problem.

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
        """Execute DFS.

        Note: DFS does NOT guarantee optimal paths. The path returned
        is the first one found, which may not be the shortest or cheapest.

        Args:
            max_iterations: Maximum node expansions before aborting.
            strict: If True, raises exceptions on failure.
            track_explored: If True, populates explored_states in result.

        Returns:
            SearchResult with the first path found (not necessarily optimal).
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

        # LIFO stack: stores (state, cost_so_far)
        stack: list[tuple[T, float]] = [(initial, 0.0)]
        visited: set[T] = set()
        came_from: dict[T, T] = {}
        cost_to: dict[T, float] = {initial: 0.0}
        iterations = 0

        while stack:
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

            current, current_cost = stack.pop()

            if current in visited:
                continue

            visited.add(current)
            iterations += 1

            if self._problem.is_goal(current):
                path = self._reconstruct_path(came_from, initial, current)
                return SearchResult(
                    path=path,
                    total_cost=current_cost,
                    nodes_explored=len(visited),
                    success=True,
                    explored_states=frozenset(visited) if track_explored else None,
                )

            for successor, step_cost in self._problem.successors(current):
                if successor not in visited:
                    came_from[successor] = current
                    cost_to[successor] = current_cost + step_cost
                    stack.append((successor, current_cost + step_cost))

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


def dfs_search(
    problem: SearchProblem[T],
    *,
    max_iterations: int | None = None,
    strict: bool = False,
    track_explored: bool = False,
) -> SearchResult[T]:
    """Convenience function for DFS."""
    return DFS(problem).search(
        max_iterations=max_iterations, strict=strict, track_explored=track_explored
    )
