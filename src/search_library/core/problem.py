"""Abstract search problem definition."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class SearchProblem(ABC, Generic[T]):
    """Abstract base class for defining a search problem.

    A search problem defines:
    - An initial state
    - A goal state (or goal test)
    - A way to generate successors
    - A cost function for transitions

    Type parameter T represents the state type.
    """

    @abstractmethod
    def initial_state(self) -> T:
        """Return the initial state of the problem.

        Returns:
            The starting state.
        """

    @abstractmethod
    def is_goal(self, state: T) -> bool:
        """Check if the given state is a goal state.

        Args:
            state: The state to check.

        Returns:
            True if the state is a goal state, False otherwise.
        """

    @abstractmethod
    def successors(self, state: T) -> list[tuple[T, float]]:
        """Generate successor states and their transition costs.

        Args:
            state: The current state.

        Returns:
            A list of tuples (successor_state, step_cost).
        """

    def heuristic(self, state: T) -> float:
        """Estimate the cost from state to the nearest goal.

        Default implementation returns 0 (equivalent to Dijkstra's algorithm).
        Override this method to provide informed heuristics.

        Args:
            state: The state to evaluate.

        Returns:
            Non-negative estimated cost to reach a goal state.
        """
        return 0.0
