"""Base heuristic interface using Strategy Pattern."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic

from search_library.core.types import T


class Heuristic(ABC, Generic[T]):
    """Abstract base class for heuristic functions.

    Heuristics estimate the cost from a given state to a goal state.
    They must be admissible (never overestimate) for A* to find optimal paths.

    Implement this class to create custom heuristics for specific problems.
    """

    @abstractmethod
    def estimate(self, state: T, goal: T) -> float:
        """Estimate the cost from state to goal.

        Args:
            state: The current state.
            goal: The goal state.

        Returns:
            A non-negative float representing the estimated cost.
            Must be admissible (never overestimate actual cost).
        """

    def __call__(self, state: T, goal: T) -> float:
        """Allow the heuristic to be called as a function.

        Args:
            state: The current state.
            goal: The goal state.

        Returns:
            The heuristic estimate.
        """
        return self.estimate(state, goal)
