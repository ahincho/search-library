"""A* (A-Star) search algorithm implementation."""

from __future__ import annotations

import heapq
from typing import Generic, TypeVar

from search_library.core.nodes import Node
from search_library.core.problem import SearchProblem
from search_library.core.result import SearchResult

T = TypeVar("T")


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

    def search(self) -> SearchResult[T]:
        """Execute the A* search algorithm.

        Returns:
            SearchResult containing the path, cost, and exploration stats.
        """
        initial = self._problem.initial_state()

        # Check if start is already the goal
        if self._problem.is_goal(initial):
            return SearchResult(
                path=[initial],
                total_cost=0.0,
                nodes_explored=1,
                success=True,
                explored_states=frozenset({initial}),
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

        # Track explored states
        closed_set: set[T] = set()

        while open_list:
            _, _, current = heapq.heappop(open_list)

            # Skip if already explored with better cost
            if current.state in closed_set:
                continue

            closed_set.add(current.state)

            # Goal check
            if self._problem.is_goal(current.state):
                path = current.reconstruct_path()
                return SearchResult(
                    path=path,
                    total_cost=current.g_cost,
                    nodes_explored=len(closed_set),
                    success=True,
                    explored_states=frozenset(closed_set),
                )

            # Expand successors
            for successor_state, step_cost in self._problem.successors(current.state):
                if successor_state in closed_set:
                    continue

                tentative_g = current.g_cost + step_cost

                # Only proceed if this path is better
                if tentative_g < g_scores.get(successor_state, float("inf")):
                    g_scores[successor_state] = tentative_g
                    h_cost = self._problem.heuristic(successor_state)

                    successor_node = Node(
                        state=successor_state,
                        parent=current,
                        g_cost=tentative_g,
                        h_cost=h_cost,
                    )

                    counter += 1
                    heapq.heappush(
                        open_list,
                        (successor_node.f_cost, counter, successor_node),
                    )

        # No solution found
        return SearchResult(
            path=[],
            total_cost=0.0,
            nodes_explored=len(closed_set),
            success=False,
            explored_states=frozenset(closed_set),
        )
