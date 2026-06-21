"""Bidirectional Search algorithm implementation."""

from __future__ import annotations

from collections import deque

from search_library.algorithms.base import SearchAlgorithm
from search_library.core.problem import SearchProblem
from search_library.core.result import SearchResult
from search_library.core.types import T
from search_library.exceptions.exceptions import NoSolutionFoundError, SearchTimeoutError


class BidirectionalSearch(SearchAlgorithm[T]):
    """Bidirectional BFS search algorithm.

    Searches simultaneously from start and goal, meeting in the middle.
    Significantly reduces the search space compared to unidirectional BFS.

    Requires both a forward problem (start -> goal) and a reverse problem
    (goal -> start) to be provided explicitly. The reverse problem must
    define successors in the reverse direction.

    Best suited for undirected graphs or symmetric directed graphs.

    Complexity:
        Time:  O(b^(d/2)) where b = branching factor, d = solution depth
        Space: O(b^(d/2)) for both frontiers

    Use cases:
        - Large unweighted graphs where BFS alone is too slow
        - Problems with known start and goal states
        - Reducing search space exponentially
    """

    def __init__(
        self,
        problem: SearchProblem[T],
        *,
        reverse_problem: SearchProblem[T],
    ) -> None:
        """Initialize Bidirectional Search.

        Args:
            problem: The forward search problem (start -> goal).
            reverse_problem: The reverse problem (goal -> start).
                Must define successors from the goal state backward.

        Example:
            For an undirected graph, reverse_problem is simply
            graph.to_search_problem(goal, start).
        """
        super().__init__(problem)
        self._reverse_problem = reverse_problem

    def search(
        self,
        *,
        max_iterations: int | None = None,
        strict: bool = False,
        track_explored: bool = False,
    ) -> SearchResult[T]:
        """Execute bidirectional BFS.

        Args:
            max_iterations: Maximum total node expansions before aborting.
            strict: If True, raises exceptions on failure.
            track_explored: If True, populates explored_states in result.

        Returns:
            SearchResult with the path connecting start to goal.
        """
        initial = self._problem.initial_state()
        goal = self._reverse_problem.initial_state()

        if self._problem.is_goal(initial):
            return SearchResult(
                path=[initial],
                total_cost=0.0,
                nodes_explored=1,
                success=True,
                explored_states=frozenset({initial}) if track_explored else None,
            )

        # Forward BFS frontier
        forward_queue: deque[T] = deque([initial])
        forward_visited: set[T] = {initial}
        forward_parent: dict[T, T] = {}

        # Backward BFS frontier
        backward_queue: deque[T] = deque([goal])
        backward_visited: set[T] = {goal}
        backward_parent: dict[T, T] = {}

        iterations = 0

        while forward_queue and backward_queue:
            if max_iterations is not None and iterations >= max_iterations:
                if strict:
                    raise SearchTimeoutError(max_iterations)
                all_visited = forward_visited | backward_visited
                return SearchResult(
                    path=[],
                    total_cost=0.0,
                    nodes_explored=len(all_visited),
                    success=False,
                    explored_states=frozenset(all_visited) if track_explored else None,
                )

            # Expand forward frontier (one node)
            meeting = self._expand_level(
                forward_queue, forward_visited, forward_parent,
                backward_visited, self._problem,
            )
            iterations += 1

            if meeting is not None:
                return self._build_result(
                    meeting, forward_parent, backward_parent,
                    initial, goal, forward_visited, backward_visited,
                    track_explored,
                )

            if not backward_queue:
                break

            # Expand backward frontier (one node)
            meeting = self._expand_level(
                backward_queue, backward_visited, backward_parent,
                forward_visited, self._reverse_problem,
            )
            iterations += 1

            if meeting is not None:
                return self._build_result(
                    meeting, forward_parent, backward_parent,
                    initial, goal, forward_visited, backward_visited,
                    track_explored,
                )

        all_visited = forward_visited | backward_visited
        if strict:
            raise NoSolutionFoundError()
        return SearchResult(
            path=[],
            total_cost=0.0,
            nodes_explored=len(all_visited),
            success=False,
            explored_states=frozenset(all_visited) if track_explored else None,
        )

    @staticmethod
    def _expand_level(
        queue: deque[T],
        visited: set[T],
        parent: dict[T, T],
        other_visited: set[T],
        problem: SearchProblem[T],
    ) -> T | None:
        """Expand one node from the frontier. Returns meeting point if found."""
        if not queue:
            return None

        current = queue.popleft()

        for successor, _ in problem.successors(current):
            if successor in visited:
                continue
            visited.add(successor)
            parent[successor] = current
            queue.append(successor)

            if successor in other_visited:
                return successor

        return None

    def _build_result(
        self,
        meeting: T,
        forward_parent: dict[T, T],
        backward_parent: dict[T, T],
        start: T,
        goal: T,
        forward_visited: set[T],
        backward_visited: set[T],
        track_explored: bool,
    ) -> SearchResult[T]:
        """Build the complete path and recalculate true cost."""
        # Forward path: start -> meeting
        forward_path: list[T] = [meeting]
        current = meeting
        while current != start:
            current = forward_parent[current]
            forward_path.append(current)
        forward_path.reverse()

        # Backward path: meeting -> goal
        backward_path: list[T] = []
        current = meeting
        while current != goal:
            current = backward_parent[current]
            backward_path.append(current)

        full_path = forward_path + backward_path

        # Recalculate true total cost by summing step costs along the path
        total_cost = self._calculate_path_cost(full_path)

        all_visited = forward_visited | backward_visited
        return SearchResult(
            path=full_path,
            total_cost=total_cost,
            nodes_explored=len(all_visited),
            success=True,
            explored_states=frozenset(all_visited) if track_explored else None,
        )

    def _calculate_path_cost(self, path: list[T]) -> float:
        """Calculate the actual cost of a path by querying forward problem successors.

        Args:
            path: The complete path from start to goal.

        Returns:
            Total cost of traversing the path.
        """
        total = 0.0
        for i in range(len(path) - 1):
            current = path[i]
            next_state = path[i + 1]
            # Find the cost of the edge current -> next_state
            for successor, cost in self._problem.successors(current):
                if successor == next_state:
                    total += cost
                    break
        return total


def bidirectional_search(
    problem: SearchProblem[T],
    *,
    reverse_problem: SearchProblem[T],
    max_iterations: int | None = None,
    strict: bool = False,
    track_explored: bool = False,
) -> SearchResult[T]:
    """Convenience function for Bidirectional Search.

    Args:
        problem: Forward search problem (start -> goal).
        reverse_problem: Reverse search problem (goal -> start).
        max_iterations: Maximum node expansions.
        strict: If True, raises on failure.
        track_explored: If True, tracks explored states.
    """
    solver = BidirectionalSearch(problem, reverse_problem=reverse_problem)
    return solver.search(
        max_iterations=max_iterations, strict=strict, track_explored=track_explored
    )
