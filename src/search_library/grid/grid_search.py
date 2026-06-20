"""Search problem adapter for 2D grids."""

from __future__ import annotations

from search_library.core.problem import SearchProblem
from search_library.grid.grid import Grid, Position
from search_library.heuristics.base import Heuristic
from search_library.heuristics.manhattan import ManhattanHeuristic


class GridSearchProblem(SearchProblem[Position]):
    """Adapts a Grid to the SearchProblem interface.

    Allows any search algorithm to operate on a 2D grid by
    providing start/goal positions and a heuristic.
    """

    def __init__(
        self,
        grid: Grid,
        start: Position,
        goal: Position,
        heuristic: Heuristic[Position] | None = None,
    ) -> None:
        """Initialize a grid search problem.

        Args:
            grid: The Grid to search on.
            start: Starting position (row, col).
            goal: Goal position (row, col).
            heuristic: Heuristic function. Defaults to Manhattan distance.

        Raises:
            ValueError: If start or goal are invalid positions.
        """
        self._grid = grid
        self._start = start
        self._goal = goal
        self._heuristic = heuristic or ManhattanHeuristic()

        self._validate_positions()

    def _validate_positions(self) -> None:
        """Validate start and goal positions.

        Raises:
            ValueError: If positions are out of bounds or are obstacles.
        """
        sr, sc = self._start
        gr, gc = self._goal

        if not self._grid.in_bounds(sr, sc):
            msg = f"Start position {self._start} is out of bounds"
            raise ValueError(msg)
        if not self._grid.in_bounds(gr, gc):
            msg = f"Goal position {self._goal} is out of bounds"
            raise ValueError(msg)
        if self._grid.is_obstacle(sr, sc):
            msg = f"Start position {self._start} is an obstacle"
            raise ValueError(msg)
        if self._grid.is_obstacle(gr, gc):
            msg = f"Goal position {self._goal} is an obstacle"
            raise ValueError(msg)

    def initial_state(self) -> Position:
        """Return the start position."""
        return self._start

    def is_goal(self, state: Position) -> bool:
        """Check if the position is the goal."""
        return state == self._goal

    def successors(self, state: Position) -> list[tuple[Position, float]]:
        """Return walkable neighbors and their traversal costs."""
        return self._grid.get_neighbors(state)

    def heuristic(self, state: Position) -> float:
        """Return heuristic estimate from state to goal."""
        return self._heuristic.estimate(state, self._goal)
