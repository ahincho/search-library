"""Grid data structure for 2D pathfinding problems."""

from __future__ import annotations

import math
from collections.abc import Sequence

# Position type: (row, col)
Position = tuple[int, int]

# Cost multiplier for diagonal movements
DIAGONAL_COST: float = math.sqrt(2)

# 4-directional movements: up, down, left, right
FOUR_DIRECTIONS: list[Position] = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# 8-directional movements: 4 cardinal + 4 diagonal
EIGHT_DIRECTIONS: list[Position] = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
    (-1, -1),
    (-1, 1),
    (1, -1),
    (1, 1),
]


class Grid:
    """2D grid for pathfinding problems.

    Supports obstacles, variable movement costs, and configurable
    movement directions (4 or 8 directional).

    The grid uses (row, col) coordinates where:
    - row 0 is the top
    - col 0 is the left

    Attributes:
        rows: Number of rows in the grid.
        cols: Number of columns in the grid.
        allow_diagonal: Whether diagonal movement is allowed.
    """

    def __init__(
        self,
        rows: int,
        cols: int,
        *,
        allow_diagonal: bool = False,
        default_cost: float = 1.0,
    ) -> None:
        """Initialize a grid.

        Args:
            rows: Number of rows.
            cols: Number of columns.
            allow_diagonal: If True, allows 8-directional movement.
            default_cost: Default traversal cost for non-obstacle cells.

        Raises:
            ValueError: If rows or cols are not positive.
        """
        if rows <= 0 or cols <= 0:
            msg = f"Grid dimensions must be positive, got ({rows}, {cols})"
            raise ValueError(msg)

        self.rows = rows
        self.cols = cols
        self.allow_diagonal = allow_diagonal
        self._default_cost = default_cost
        self._obstacles: set[Position] = set()
        self._costs: dict[Position, float] = {}

    @classmethod
    def from_matrix(
        cls,
        matrix: Sequence[Sequence[int]],
        *,
        obstacle_value: int = 1,
        allow_diagonal: bool = False,
    ) -> Grid:
        """Create a grid from a 2D matrix.

        Args:
            matrix: 2D sequence where obstacle_value marks impassable cells.
            obstacle_value: The value that represents an obstacle.
            allow_diagonal: Whether diagonal movement is allowed.

        Returns:
            A configured Grid instance.

        Raises:
            ValueError: If matrix is empty or rows have inconsistent lengths.
        """
        if not matrix or not matrix[0]:
            msg = "Matrix must not be empty"
            raise ValueError(msg)

        rows = len(matrix)
        cols = len(matrix[0])

        grid = cls(rows, cols, allow_diagonal=allow_diagonal)

        for r in range(rows):
            if len(matrix[r]) != cols:
                msg = f"Inconsistent row length at row {r}"
                raise ValueError(msg)
            for c in range(cols):
                if matrix[r][c] == obstacle_value:
                    grid.set_obstacle(r, c)

        return grid

    def set_obstacle(self, row: int, col: int) -> None:
        """Mark a cell as an obstacle.

        Args:
            row: Row index.
            col: Column index.

        Raises:
            IndexError: If position is out of bounds.
        """
        self._validate_position(row, col)
        self._obstacles.add((row, col))

    def remove_obstacle(self, row: int, col: int) -> None:
        """Remove obstacle status from a cell.

        Args:
            row: Row index.
            col: Column index.
        """
        self._obstacles.discard((row, col))

    def is_obstacle(self, row: int, col: int) -> bool:
        """Check if a cell is an obstacle.

        Args:
            row: Row index.
            col: Column index.

        Returns:
            True if the cell is an obstacle.
        """
        return (row, col) in self._obstacles

    def set_cost(self, row: int, col: int, cost: float) -> None:
        """Set a custom traversal cost for a cell.

        Args:
            row: Row index.
            col: Column index.
            cost: The cost to enter this cell.

        Raises:
            IndexError: If position is out of bounds.
            ValueError: If cost is negative.
        """
        self._validate_position(row, col)
        if cost < 0:
            msg = f"Cost must be non-negative, got {cost}"
            raise ValueError(msg)
        self._costs[(row, col)] = cost

    def get_cost(self, position: Position) -> float:
        """Get the traversal cost for a cell.

        Args:
            position: The (row, col) position.

        Returns:
            The cost to enter the cell.
        """
        return self._costs.get(position, self._default_cost)

    def in_bounds(self, row: int, col: int) -> bool:
        """Check if a position is within grid bounds.

        Args:
            row: Row index.
            col: Column index.

        Returns:
            True if position is within bounds.
        """
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_walkable(self, row: int, col: int) -> bool:
        """Check if a cell is within bounds and not an obstacle.

        Args:
            row: Row index.
            col: Column index.

        Returns:
            True if the cell can be traversed.
        """
        return self.in_bounds(row, col) and not self.is_obstacle(row, col)

    def get_neighbors(self, position: Position) -> list[tuple[Position, float]]:
        """Get walkable neighbors of a position with their costs.

        Args:
            position: The (row, col) position to get neighbors for.

        Returns:
            List of (neighbor_position, cost) tuples.
            Diagonal movements cost sqrt(2) times the cell cost.
        """
        row, col = position
        directions = EIGHT_DIRECTIONS if self.allow_diagonal else FOUR_DIRECTIONS
        neighbors: list[tuple[Position, float]] = []

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if self.is_walkable(new_row, new_col):
                base_cost = self.get_cost((new_row, new_col))
                is_diagonal = dr != 0 and dc != 0
                move_cost = base_cost * DIAGONAL_COST if is_diagonal else base_cost
                neighbors.append(((new_row, new_col), move_cost))

        return neighbors

    def _validate_position(self, row: int, col: int) -> None:
        """Validate that a position is within bounds.

        Raises:
            IndexError: If position is out of bounds.
        """
        if not self.in_bounds(row, col):
            msg = f"Position ({row}, {col}) is out of bounds for grid ({self.rows}, {self.cols})"
            raise IndexError(msg)
