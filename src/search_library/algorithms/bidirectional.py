"""Bidirectional Search algorithm implementation."""

from __future__ import annotations

from collections import deque
from typing import Generic

from search_library.algorithms.base import SearchAlgorithm
from search_library.core.problem import SearchProblem
from search_library.core.result import SearchResult
from search_library.core.types import T
from search_library.exceptions.exceptions import NoSolutionFoundError, SearchTimeoutError


class BidirectionalSearch(SearchAlgorithm[T], Generic[T]):
    """Bidirectional BFS search algorithm.

    Searches simultaneously from start and goal, meeting in the middle.
    Significantly reduces the search space compared to unidirectional BFS.

    Requires a reversible problem (goal state must be known explicitly and
    successors must be traversable in reverse). Uses BFS from both ends.

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
        reverse_problem: SearchProblem[T] | None = None,
    ) -> None:
        """Initialize Bidirectional Search.

        Args:
            problem: The forward search problem (start -> goal).
            reverse_problem: Optional reverse problem (goal -> start).
                If not provided, the algorithm uses the same problem's
                successors for the backward search (assumes undirected graph).
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
            max_iterations: Maximum total expansions before aborting.
            strict: If True, raises exceptions on failure.
            track_explored: If True, populates explored_states in result.

        Returns:
            SearchResult with the path connecting start to goal.
        """
        initial = self._problem.initial_state()

        # For bidirectional search, we need to know the goal state.
        # We check if initial is goal first.
        if self._problem.is_goal(initial):
            return SearchResult(
                path=[initial],
                total_cost=0.0,
                nodes_explored=1,
                success=True,
                explored_states=frozenset({initial}) if track_explored else None,
            )

        # Determine the goal state by checking which state the reverse starts from
        reverse = self._reverse_problem or self._problem
        goal = reverse.initial_state() if self._reverse_problem else self._find_goal(initial)

        if goal is None:
            if strict:
                raise NoSolutionFoundError("Cannot determine goal state for bidirectional search")
            return SearchResult(path=[], success=False, nodes_explored=0)

        # Forward BFS frontier
        forward_queue: deque[T] = deque([initial])
        forward_visited: set[T] = {initial}
        forward_parent: dict[T, T] = {}
        forward_cost: dict[T, float] = {initial: 0.0}

        # Backward BFS frontier
        backward_queue: deque[T] = deque([goal])
        backward_visited: set[T] = {goal}
        backward_parent: dict[T, T] = {}
        backward_cost: dict[T, float] = {goal: 0.0}

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

            # Expand forward
            meeting = self._expand_forward(
                forward_queue, forward_visited, forward_parent,
                forward_cost, backward_visited,
            )
            iterations += 1

            if meeting is not None:
                path, cost = self._build_path(
                    meeting, forward_parent, backward_parent,
                    forward_cost, backward_cost, initial, goal,
                )
                all_visited = forward_visited | backward_visited
                return SearchResult(
                    path=path,
                    total_cost=cost,
                    nodes_explored=len(all_visited),
                    success=True,
                    explored_states=frozenset(all_visited) if track_explored else None,
                )

            if not backward_queue:
                break

            # Expand backward
            meeting = self._expand_backward(
                backward_queue, backward_visited, backward_parent,
                backward_cost, forward_visited, reverse,
            )
            iterations += 1

            if meeting is not None:
                path, cost = self._build_path(
                    meeting, forward_parent, backward_parent,
                    forward_cost, backward_cost, initial, goal,
                )
                all_visited = forward_visited | backward_visited
                return SearchResult(
                    path=path,
                    total_cost=cost,
                    nodes_explored=len(all_visited),
                    success=True,
                    explored_states=frozenset(all_visited) if track_explored else None,
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

    def _find_goal(self, initial: T) -> T | None:
        """Try to find the goal by scanning successors (limited BFS)."""
        # For bidirectional to work without a reverse_problem,
        # we need to find what state is_goal returns True for.
        # We do a limited BFS to find it.
        queue: deque[T] = deque([initial])
        visited: set[T] = {initial}
        for _ in range(10000):
            if not queue:
                return None
            state = queue.popleft()
            if state != initial and self._problem.is_goal(state):
                return state
            for succ, _ in self._problem.successors(state):
                if succ not in visited:
                    visited.add(succ)
                    queue.append(succ)
                    if self._problem.is_goal(succ):
                        return succ
        return None

    def _expand_forward(
        self,
        queue: deque[T],
        visited: set[T],
        parent: dict[T, T],
        cost: dict[T, float],
        other_visited: set[T],
    ) -> T | None:
        """Expand one level of forward BFS. Returns meeting point if found."""
        if not queue:
            return None

        current = queue.popleft()
        current_cost = cost[current]

        for successor, step_cost in self._problem.successors(current):
            if successor in visited:
                continue
            visited.add(successor)
            parent[successor] = current
            cost[successor] = current_cost + step_cost
            queue.append(successor)

            if successor in other_visited:
                return successor

        return None

    def _expand_backward(
        self,
        queue: deque[T],
        visited: set[T],
        parent: dict[T, T],
        cost: dict[T, float],
        other_visited: set[T],
        reverse_problem: SearchProblem[T],
    ) -> T | None:
        """Expand one level of backward BFS. Returns meeting point if found."""
        if not queue:
            return None

        current = queue.popleft()
        current_cost = cost[current]

        for successor, step_cost in reverse_problem.successors(current):
            if successor in visited:
                continue
            visited.add(successor)
            parent[successor] = current
            cost[successor] = current_cost + step_cost
            queue.append(successor)

            if successor in other_visited:
                return successor

        return None

    @staticmethod
    def _build_path(
        meeting: T,
        forward_parent: dict[T, T],
        backward_parent: dict[T, T],
        forward_cost: dict[T, float],
        backward_cost: dict[T, float],
        start: T,
        goal: T,
    ) -> tuple[list[T], float]:
        """Build the complete path through the meeting point."""
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
        total_cost = forward_cost.get(meeting, 0.0) + backward_cost.get(meeting, 0.0)

        return full_path, total_cost


def bidirectional_search(
    problem: SearchProblem[T],
    *,
    reverse_problem: SearchProblem[T] | None = None,
    max_iterations: int | None = None,
    strict: bool = False,
    track_explored: bool = False,
) -> SearchResult[T]:
    """Convenience function for Bidirectional Search."""
    solver = BidirectionalSearch(problem, reverse_problem=reverse_problem)
    return solver.search(
        max_iterations=max_iterations, strict=strict, track_explored=track_explored
    )
