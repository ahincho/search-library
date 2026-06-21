"""Tests for visualization utilities."""

from search_library.core.result import SearchResult
from search_library.grid.grid import Grid
from search_library.utils.visualization import render_grid, render_search_result


class TestRenderGrid:
    """Tests for render_grid utility."""

    def test_empty_grid(self) -> None:
        grid = Grid(3, 3)
        output = render_grid(grid)
        lines = output.split("\n")
        assert len(lines) == 3

    def test_grid_with_obstacles(self) -> None:
        grid = Grid(3, 3)
        grid.set_obstacle(1, 1)
        output = render_grid(grid)
        assert "#" in output

    def test_grid_with_path(self) -> None:
        grid = Grid(3, 3)
        path = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]
        output = render_grid(grid, path=path)
        assert "S" in output
        assert "G" in output
        assert "*" in output

    def test_grid_with_explored(self) -> None:
        grid = Grid(3, 3)
        explored = frozenset({(1, 0), (1, 1), (2, 0)})
        output = render_grid(grid, explored=explored)
        assert "." in output

    def test_custom_characters(self) -> None:
        grid = Grid(3, 3)
        path = [(0, 0), (1, 0), (2, 0)]
        output = render_grid(
            grid, path=path, start_char="@", goal_char="X", path_char="+"
        )
        assert "@" in output
        assert "X" in output
        assert "+" in output


class TestRenderSearchResult:
    """Tests for render_search_result utility."""

    def test_successful_result(self) -> None:
        grid = Grid(3, 3)
        result: SearchResult[tuple[int, int]] = SearchResult(
            path=[(0, 0), (0, 1), (0, 2)],
            total_cost=2.0,
            nodes_explored=3,
            success=True,
        )
        output = render_search_result(grid, result)
        assert "S" in output
        assert "G" in output

    def test_failed_result(self) -> None:
        grid = Grid(3, 3)
        result: SearchResult[tuple[int, int]] = SearchResult(
            path=[], success=False, nodes_explored=5
        )
        output = render_search_result(grid, result)
        # No path markers
        assert "S" not in output
        assert "G" not in output

    def test_with_explored_states(self) -> None:
        grid = Grid(3, 3)
        result: SearchResult[tuple[int, int]] = SearchResult(
            path=[(0, 0), (1, 0), (2, 0)],
            total_cost=2.0,
            nodes_explored=5,
            success=True,
            explored_states=frozenset({(0, 0), (1, 0), (2, 0), (0, 1), (1, 1)}),
        )
        output = render_search_result(grid, result, show_explored=True)
        assert "." in output  # explored but not on path
