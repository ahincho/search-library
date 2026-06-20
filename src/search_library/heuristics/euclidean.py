"""Euclidean distance heuristic for grid-based problems."""

from __future__ import annotations

import math

from search_library.heuristics.base import Heuristic


class EuclideanHeuristic(Heuristic[tuple[int, int]]):
    """Euclidean distance heuristic for 2D grid positions.

    Calculates the straight-line distance between two points.
    This is admissible for any grid movement scheme (4-dir or 8-dir).

    Suitable for:
        - Grid pathfinding with any directional movement
        - Problems where diagonal movement is allowed
        - General-purpose 2D pathfinding
    """

    def estimate(self, state: tuple[int, int], goal: tuple[int, int]) -> float:
        """Calculate Euclidean distance between two 2D positions.

        Args:
            state: Current position as (row, col).
            goal: Goal position as (row, col).

        Returns:
            Euclidean distance (L2 norm) between the positions.
        """
        dx = state[0] - goal[0]
        dy = state[1] - goal[1]
        return math.sqrt(dx * dx + dy * dy)
