"""A* (A-Star) search algorithm implementation."""

from __future__ import annotations

import heapq
from typing import Generic

from search_library.core.nodes import Node
from search_library.core.problem import SearchProblem
from search_library.core.result import SearchResult
from search_library.core.types import T
from search_library.exceptions.exceptions import NoSolutionFoundError, SearchTimeoutError


class AStarSearch(Generic[T]):
    """A* Search Algorithm implementation.

    A* is an informed search algorithm that finds the optimal path
    from a start state to a goal state using:

        f(n) = g(n) + h(n)

    Where:
        - g(n): actual cost from start to node n
        - h(n): heuristic estimate from n to goal
        - f(n): estimated total cost through n

    The algorithm is optimal when the heuristic is admissible
    (never overestimates the true cost).
    """

    def __init__(self, problem: SearchProblem[T]) -> None:
        """Initialize A* with a search problem.

        Args:
            problem: The search problem to solve.
        """
        self._problem = problem

    def search(
        self,
        *,
        max_iterations: int | None = None,
        strict: bool = False,
        track_explored: bool = False,
    ) -> SearchResult[T]:
        """Execute the A* search algorithm.

        Args:
            max_iterations: Maximum number of node expansions before aborting.
                None means no limit.
            strict: If True, raises exceptions on failure instead of returning
                a result with success=False.
            track_explored: If True, populates explored_states in the result.
                Disabled by default to save memory on large search spaces.

        Returns:
            SearchResult containing the path, cost, and exploration stats.

        Raises:
            NoSolutionFoundError: If strict=True and no solution exists.
            SearchTimeoutError: If strict=True and max_iterations is exceeded.
        """
        initial = self._problem.initial_state()

        # Check if start is already the goal
        if self._problem.is_goal(initial):
            return SearchResult(
                path=[initial],
                total_cost=0.0,
                nodes_explored=1,
                success=True,
                explored_states=frozenset({initial}) if track_explored else None,
            )

        # Create start node
        h_cost = self._problem.heuristic(initial)
        start_node = Node(state=initial, g_cost=0.0, h_cost=h_cost)

        # Priority queue: (f_cost, counter, node)
        # Counter breaks ties in f_cost to ensure FIFO ordering
        counter = 0
        open_list: list[tuple[float, int, Node[T]]] = []
        heapq.heappush(open_list, (start_node.f_cost, counter, start_node))

        # Track best known g_cost for each state
        g_scores: dict[T, float] = {initial: 0.0}

        # Path reconstruction map: state -> parent state
        came_from: dict[T, T] = {}

        # Track explored states
        closed_set: set[T] = set()

        iterations = 0

        while open_list:
            # Check iteration limit
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

            # Skip if already explored with better cost
            if current.state in closed_set:
                continue

            closed_set.add(current.state)
            iterations += 1

            # Goal check
            if self._problem.is_goal(current.state):
                path = self._reconstruct_path(came_from, initial, current.state)
                return SearchResult(
                    path=path,
                    total_cost=current.g_cost,
                    nodes_explored=len(closed_set),
                    success=True,
                    explored_states=frozenset(closed_set) if track_explored else None,
                )

            # Expand successors
            for successor_state, step_cost in self._problem.successors(current.state):
                if successor_state in closed_set:
                    continue

                tentative_g = current.g_cost + step_cost

                # Only proceed if this path is better
                if tentative_g < g_scores.get(successor_state, float("inf")):
                    g_scores[successor_state] = tentative_g
                    came_from[successor_state] = current.state
                    h_cost = self._problem.heuristic(successor_state)

                    successor_node = Node(
                        state=successor_state,
                        g_cost=tentative_g,
                        h_cost=h_cost,
                    )

                    counter += 1
                    heapq.heappush(
                        open_list,
                        (successor_node.f_cost, counter, successor_node),
                    )

        # No solution found
        if strict:
            raise NoSolutionFoundError()
        return SearchResult(
            path=[],
            total_cost=0.0,
            nodes_explored=len(closed_set),
            success=False,
            explored_states=frozenset(closed_set) if track_explored else None,
        )

    @staticmethod
    def _reconstruct_path(came_from: dict[T, T], start: T, goal: T) -> list[T]:
        """Reconstruct path from came_from map.

        Args:
            came_from: Mapping of state -> parent state.
            start: The initial state.
            goal: The goal state.

        Returns:
            Ordered list of states from start to goal.
        """
        path: list[T] = [goal]
        current = goal
        while current != start:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path


def astar_search(
    problem: SearchProblem[T],
    *,
    max_iterations: int | None = None,
    strict: bool = False,
    track_explored: bool = False,
) -> SearchResult[T]:
    """Convenience function for A* search.

    Equivalent to AStarSearch(problem).search(...) but more concise.

    Args:
        problem: The search problem to solve.
        max_iterations: Maximum node expansions before aborting.
        strict: If True, raises exceptions on failure.
        track_explored: If True, populates explored_states in the result.

    Returns:
        SearchResult containing the path, cost, and exploration stats.
    """
    solver = AStarSearch(problem)
    return solver.search(
        max_iterations=max_iterations,
        strict=strict,
        track_explored=track_explored,
    )
