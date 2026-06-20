"""Tests for exceptions module."""

import pytest

from search_library.exceptions import (
    InvalidHeuristicError,
    InvalidNodeError,
    NoSolutionFoundError,
    SearchError,
    SearchTimeoutError,
)


class TestExceptions:
    """Tests for custom exceptions."""

    def test_search_error_base(self) -> None:
        with pytest.raises(SearchError):
            raise SearchError("test error")

    def test_no_solution_found_default_message(self) -> None:
        err = NoSolutionFoundError()
        assert "No solution found" in str(err)

    def test_no_solution_found_custom_message(self) -> None:
        err = NoSolutionFoundError("Custom message")
        assert "Custom message" in str(err)

    def test_invalid_node_error(self) -> None:
        err = InvalidNodeError("node_x", "not in graph")
        assert "node_x" in str(err)
        assert "not in graph" in str(err)

    def test_invalid_node_error_no_reason(self) -> None:
        err = InvalidNodeError("node_y")
        assert "node_y" in str(err)

    def test_invalid_heuristic_error(self) -> None:
        err = InvalidHeuristicError(-5.0, "must be non-negative")
        assert "-5.0" in str(err)
        assert "non-negative" in str(err)

    def test_invalid_heuristic_error_no_reason(self) -> None:
        err = InvalidHeuristicError(-1.0)
        assert "-1.0" in str(err)

    def test_search_timeout_error(self) -> None:
        err = SearchTimeoutError(1000)
        assert "1000" in str(err)

    def test_search_timeout_error_custom_message(self) -> None:
        err = SearchTimeoutError(500, "Took too long")
        assert "Took too long" in str(err)

    def test_exception_hierarchy(self) -> None:
        assert issubclass(NoSolutionFoundError, SearchError)
        assert issubclass(InvalidNodeError, SearchError)
        assert issubclass(InvalidHeuristicError, SearchError)
        assert issubclass(SearchTimeoutError, SearchError)
        assert issubclass(SearchError, Exception)
