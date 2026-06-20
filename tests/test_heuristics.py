"""Tests for heuristic functions."""

import math

from search_library.heuristics.base import Heuristic
from search_library.heuristics.euclidean import EuclideanHeuristic
from search_library.heuristics.manhattan import ManhattanHeuristic


class TestManhattanHeuristic:
    """Tests for Manhattan distance heuristic."""

    def test_same_position(self) -> None:
        h = ManhattanHeuristic()
        assert h.estimate((0, 0), (0, 0)) == 0.0

    def test_horizontal_distance(self) -> None:
        h = ManhattanHeuristic()
        assert h.estimate((0, 0), (0, 5)) == 5.0

    def test_vertical_distance(self) -> None:
        h = ManhattanHeuristic()
        assert h.estimate((0, 0), (3, 0)) == 3.0

    def test_diagonal_distance(self) -> None:
        h = ManhattanHeuristic()
        assert h.estimate((0, 0), (3, 4)) == 7.0

    def test_negative_coordinates(self) -> None:
        h = ManhattanHeuristic()
        assert h.estimate((2, 3), (5, 1)) == 5.0

    def test_callable(self) -> None:
        h = ManhattanHeuristic()
        assert h((0, 0), (3, 4)) == 7.0


class TestEuclideanHeuristic:
    """Tests for Euclidean distance heuristic."""

    def test_same_position(self) -> None:
        h = EuclideanHeuristic()
        assert h.estimate((0, 0), (0, 0)) == 0.0

    def test_horizontal_distance(self) -> None:
        h = EuclideanHeuristic()
        assert h.estimate((0, 0), (0, 5)) == 5.0

    def test_vertical_distance(self) -> None:
        h = EuclideanHeuristic()
        assert h.estimate((0, 0), (3, 0)) == 3.0

    def test_diagonal_distance(self) -> None:
        h = EuclideanHeuristic()
        expected = math.sqrt(3**2 + 4**2)
        assert h.estimate((0, 0), (3, 4)) == expected

    def test_callable(self) -> None:
        h = EuclideanHeuristic()
        expected = math.sqrt(2)
        assert abs(h((0, 0), (1, 1)) - expected) < 1e-10


class TestCustomHeuristic:
    """Tests for custom heuristic extensibility."""

    def test_custom_heuristic(self) -> None:
        class ZeroHeuristic(Heuristic[tuple[int, int]]):
            def estimate(self, state: tuple[int, int], goal: tuple[int, int]) -> float:
                return 0.0

        h = ZeroHeuristic()
        assert h.estimate((0, 0), (10, 10)) == 0.0
        assert h((0, 0), (10, 10)) == 0.0
