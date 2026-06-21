"""Visualization utilities for search results on grids."""

from __future__ import annotations

from search_library.core.result import SearchResult
from search_library.grid.grid import Grid, Position


def render_grid(
    grid: Grid,
    *,
    path: list[Position] | None = None,
    explored: frozenset[Position] | None = None,
    start_char: str = "S",
    goal_char: str = "G",
    path_char: str = "*",
    explored_char: str = ".",
    obstacle_char: str = "#",
    empty_char: str = " ",
) -> str:
    """Render a grid as a text string with path and explored nodes.

    Args:
        grid: The Grid to render.
        path: Optional list of positions representing the solution path.
        explored: Optional set of explored positions to display.
        start_char: Character for the start position.
        goal_char: Character for the goal position.
        path_char: Character for path positions.
        explored_char: Character for explored positions.
        obstacle_char: Character for obstacles.
        empty_char: Character for empty cells.

    Returns:
        Multi-line string representation of the grid.
    """
    path_set: set[Position] = set(path) if path else set()
    explored_set: set[Position] = set(explored) if explored else set()

    start: Position | None = path[0] if path else None
    goal: Position | None = path[-1] if path and len(path) > 1 else None

    lines: list[str] = []
    for row in range(grid.rows):
        cells: list[str] = []
        for col in range(grid.cols):
            pos: Position = (row, col)
            if pos == start:
                cells.append(start_char)
            elif pos == goal:
                cells.append(goal_char)
            elif grid.is_obstacle(row, col):
                cells.append(obstacle_char)
            elif pos in path_set:
                cells.append(path_char)
            elif pos in explored_set:
                cells.append(explored_char)
            else:
                cells.append(empty_char)
        lines.append(" ".join(cells))

    return "\n".join(lines)


def render_search_result(
    grid: Grid,
    result: SearchResult[Position],
    *,
    show_explored: bool = False,
) -> str:
    """Render a search result on a grid.

    Args:
        grid: The Grid that was searched.
        result: The SearchResult from a search algorithm.
        show_explored: If True, shows explored nodes (requires track_explored=True).

    Returns:
        Multi-line string with the grid, path, and optionally explored nodes.
    """
    explored = result.explored_states if show_explored else None
    return render_grid(grid, path=result.path if result.success else None, explored=explored)


def print_grid(
    grid: Grid,
    result: SearchResult[Position] | None = None,
    *,
    show_explored: bool = False,
) -> None:
    """Print a grid with optional search result visualization.

    Args:
        grid: The Grid to print.
        result: Optional SearchResult to overlay on the grid.
        show_explored: If True, shows explored nodes.
    """
    if result is not None:
        output = render_search_result(grid, result, show_explored=show_explored)
    else:
        output = render_grid(grid)
    print(output)
