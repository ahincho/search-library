"""Tests for grid module."""

import pytest

from search_library.algorithms.astar import AStarSearch
from search_library.grid.grid import Grid
from search_library.grid.grid_search import GridSearchProblem
from search_library.heuristics.euclidean import EuclideanHeuristic
from search_library.heuristics.manhattan import ManhattanHeuristic


class TestGrid:
    """Tests for Grid class."""

    def test_grid_creation(self) -> None:
        grid = Grid(5, 5)
        assert grid.rows == 5
        assert grid.cols == 5

    def test_grid_invalid_dimensions(self) -> None:
        with pytest.raises(ValueError, match="positive"):
            Grid(0, 5)
        with pytest.raises(ValueError, match="positive"):
            Grid(5, -1)

    def test_set_obstacle(self) -> None:
        grid = Grid(5, 5)
        grid.set_obstacle(2, 3)
        assert grid.is_obstacle(2, 3)
        assert not grid.is_obstacle(0, 0)

    def test_set_obstacle_out_of_bounds(self) -> None:
        grid = Grid(5, 5)
        with pytest.raises(IndexError):
            grid.set_obstacle(5, 0)

    def test_remove_obstacle(self) -> None:
        grid = Grid(5, 5)
        grid.set_obstacle(2, 3)
        grid.remove_obstacle(2, 3)
        assert not grid.is_obstacle(2, 3)

    def test_in_bounds(self) -> None:
        grid = Grid(5, 5)
        assert grid.in_bounds(0, 0)
        assert grid.in_bounds(4, 4)
        assert not grid.in_bounds(5, 0)
        assert not grid.in_bounds(-1, 0)
        assert not grid.in_bounds(0, 5)

    def test_is_walkable(self) -> None:
        grid = Grid(5, 5)
        grid.set_obstacle(1, 1)
        assert grid.is_walkable(0, 0)
        assert not grid.is_walkable(1, 1)
        assert not grid.is_walkable(5, 5)  # out of bounds

    def test_get_neighbors_4dir(self) -> None:
        grid = Grid(3, 3)
        neighbors = grid.get_neighbors((1, 1))
        positions = [pos for pos, _ in neighbors]
        assert (0, 1) in positions  # up
        assert (2, 1) in positions  # down
        assert (1, 0) in positions  # left
        assert (1, 2) in positions  # right
        assert len(neighbors) == 4

    def test_get_neighbors_corner(self) -> None:
        grid = Grid(3, 3)
        neighbors = grid.get_neighbors((0, 0))
        positions = [pos for pos, _ in neighbors]
        assert len(positions) == 2
        assert (1, 0) in positions
        assert (0, 1) in positions

    def test_get_neighbors_with_obstacle(self) -> None:
        grid = Grid(3, 3)
        grid.set_obstacle(0, 1)
        neighbors = grid.get_neighbors((0, 0))
        positions = [pos for pos, _ in neighbors]
        assert (0, 1) not in positions
        assert (1, 0) in positions

    def test_get_neighbors_8dir(self) -> None:
        grid = Grid(3, 3, allow_diagonal=True)
        neighbors = grid.get_neighbors((1, 1))
        assert len(neighbors) == 8

    def test_set_cost(self) -> None:
        grid = Grid(5, 5)
        grid.set_cost(1, 1, 3.0)
        assert grid.get_cost((1, 1)) == 3.0
        assert grid.get_cost((0, 0)) == 1.0  # default

    def test_set_cost_negative_raises(self) -> None:
        grid = Grid(5, 5)
        with pytest.raises(ValueError, match="non-negative"):
            grid.set_cost(1, 1, -1.0)

    def test_set_cost_out_of_bounds_raises(self) -> None:
        grid = Grid(5, 5)
        with pytest.raises(IndexError):
            grid.set_cost(10, 10, 2.0)

    def test_from_matrix(self) -> None:
        matrix = [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0],
        ]
        grid = Grid.from_matrix(matrix)
        assert grid.rows == 3
        assert grid.cols == 3
        assert grid.is_obstacle(1, 1)
        assert not grid.is_obstacle(0, 0)

    def test_from_matrix_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            Grid.from_matrix([])

    def test_from_matrix_inconsistent_rows(self) -> None:
        matrix = [
            [0, 0, 0],
            [0, 1],
        ]
        with pytest.raises(ValueError, match="Inconsistent"):
            Grid.from_matrix(matrix)


class TestGridSearchProblem:
    """Tests for grid-based A* search."""

    def test_simple_grid_search(self) -> None:
        grid = Grid(3, 3)
        problem = GridSearchProblem(grid, (0, 0), (2, 2))
        solver = AStarSearch(problem)
        result = solver.search()

        assert result.success is True
        assert result.path[0] == (0, 0)
        assert result.path[-1] == (2, 2)
        assert result.total_cost == 4.0  # Manhattan optimal

    def test_grid_with_obstacles(self) -> None:
        """Grid with wall blocking direct path."""
        matrix = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        grid = Grid.from_matrix(matrix)
        problem = GridSearchProblem(grid, (0, 0), (4, 4))
        solver = AStarSearch(problem)
        result = solver.search()

        assert result.success is True
        assert result.path[0] == (0, 0)
        assert result.path[-1] == (4, 4)
        # Verify path doesn't go through obstacles
        for pos in result.path:
            assert not grid.is_obstacle(pos[0], pos[1])

    def test_grid_no_path(self) -> None:
        """Goal completely surrounded by obstacles."""
        matrix = [
            [0, 0, 0],
            [0, 1, 1],
            [0, 1, 0],
        ]
        grid = Grid.from_matrix(matrix)
        problem = GridSearchProblem(grid, (0, 0), (2, 2))
        solver = AStarSearch(problem)
        result = solver.search()

        assert result.success is False
        assert result.path == []

    def test_start_equals_goal_grid(self) -> None:
        grid = Grid(3, 3)
        problem = GridSearchProblem(grid, (1, 1), (1, 1))
        solver = AStarSearch(problem)
        result = solver.search()

        assert result.success is True
        assert result.path == [(1, 1)]
        assert result.total_cost == 0.0

    def test_grid_large_maze(self) -> None:
        """Test a larger maze-like grid."""
        matrix = [
            [0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]
        grid = Grid.from_matrix(matrix)
        problem = GridSearchProblem(grid, (0, 0), (6, 6))
        solver = AStarSearch(problem)
        result = solver.search()

        assert result.success is True
        assert result.path[0] == (0, 0)
        assert result.path[-1] == (6, 6)
        for pos in result.path:
            assert not grid.is_obstacle(pos[0], pos[1])

    def test_grid_with_euclidean_heuristic(self) -> None:
        grid = Grid(5, 5)
        heuristic = EuclideanHeuristic()
        problem = GridSearchProblem(grid, (0, 0), (4, 4), heuristic)
        solver = AStarSearch(problem)
        result = solver.search()

        assert result.success is True
        assert result.total_cost == 8.0

    def test_grid_with_manhattan_heuristic(self) -> None:
        grid = Grid(5, 5)
        heuristic = ManhattanHeuristic()
        problem = GridSearchProblem(grid, (0, 0), (4, 4), heuristic)
        solver = AStarSearch(problem)
        result = solver.search()

        assert result.success is True
        assert result.total_cost == 8.0

    def test_invalid_start_out_of_bounds(self) -> None:
        grid = Grid(3, 3)
        with pytest.raises(ValueError, match="out of bounds"):
            GridSearchProblem(grid, (5, 5), (0, 0))

    def test_invalid_goal_out_of_bounds(self) -> None:
        grid = Grid(3, 3)
        with pytest.raises(ValueError, match="out of bounds"):
            GridSearchProblem(grid, (0, 0), (5, 5))

    def test_start_on_obstacle(self) -> None:
        grid = Grid(3, 3)
        grid.set_obstacle(0, 0)
        with pytest.raises(ValueError, match="obstacle"):
            GridSearchProblem(grid, (0, 0), (2, 2))

    def test_goal_on_obstacle(self) -> None:
        grid = Grid(3, 3)
        grid.set_obstacle(2, 2)
        with pytest.raises(ValueError, match="obstacle"):
            GridSearchProblem(grid, (0, 0), (2, 2))

    def test_nodes_explored_tracked(self) -> None:
        grid = Grid(5, 5)
        problem = GridSearchProblem(grid, (0, 0), (4, 4))
        solver = AStarSearch(problem)
        result = solver.search()

        assert result.nodes_explored > 0
        assert len(result.explored_states) > 0

    def test_path_continuity(self) -> None:
        """Verify each step in path is adjacent to the previous."""
        grid = Grid(5, 5)
        problem = GridSearchProblem(grid, (0, 0), (4, 4))
        solver = AStarSearch(problem)
        result = solver.search()

        for i in range(1, len(result.path)):
            prev = result.path[i - 1]
            curr = result.path[i]
            dist = abs(prev[0] - curr[0]) + abs(prev[1] - curr[1])
            assert dist == 1, f"Non-adjacent step: {prev} -> {curr}"
