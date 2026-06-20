"""Tests for utility functions."""

from search_library.core.result import SearchResult
from search_library.utils.helpers import format_path, format_result_summary


class TestFormatPath:
    """Tests for format_path utility."""

    def test_successful_path(self) -> None:
        result = SearchResult(path=["A", "B", "C"], success=True, total_cost=2.0)
        assert format_path(result) == "A -> B -> C"

    def test_failed_path(self) -> None:
        result = SearchResult(path=[], success=False)
        assert format_path(result) == "No path found"

    def test_custom_separator(self) -> None:
        result = SearchResult(path=["A", "B", "C"], success=True, total_cost=2.0)
        assert format_path(result, separator=" → ") == "A → B → C"

    def test_single_node_path(self) -> None:
        result = SearchResult(path=["A"], success=True, total_cost=0.0)
        assert format_path(result) == "A"


class TestFormatResultSummary:
    """Tests for format_result_summary utility."""

    def test_successful_summary(self) -> None:
        result = SearchResult(
            path=["A", "B", "C"],
            total_cost=5.0,
            nodes_explored=10,
            success=True,
        )
        summary = format_result_summary(result)
        assert "Success: True" in summary
        assert "3 states" in summary
        assert "2 steps" in summary
        assert "5.00" in summary
        assert "10" in summary
        assert "A -> B -> C" in summary

    def test_failed_summary(self) -> None:
        result = SearchResult(
            path=[],
            total_cost=0.0,
            nodes_explored=5,
            success=False,
        )
        summary = format_result_summary(result)
        assert "Success: False" in summary
        assert "0 states" in summary
