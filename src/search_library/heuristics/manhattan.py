"""Manhattan distance heuristic for grid-based problems."""

from __future__ import annotations

from search_library.heuristics.base import Heuristic


class ManhattanHeuristic(Heuristic[tuple[int, int]]):
    """Manhattan distance heuristic for 2D grid positions.

    Calculates the sum of absolute differences in x and y coordinates.
    This is admissible for grids with 4-directional movement and uniform cost.

    Suitable for:
        - Grid pathfinding with 4-directional movement
        - Problems where diagonal movement is not allowed
    """

    def estimate(self, state: tuple[int, int], goal: tuple[int, int]) -> float:
        """Calculate Manhattan distance between two 2D positions.

        Args:
            state: Current position as (row, col).
            goal: Goal position as (row, col).

        Returns:
            Manhattan distance (L1 norm) between the positions.
        """
        return float(abs(state[0] - goal[0]) + abs(state[1] - goal[1]))
