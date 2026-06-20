"""Custom exceptions for the search library."""

from search_library.exceptions.exceptions import (
    InvalidHeuristicError,
    InvalidNodeError,
    NoSolutionFoundError,
    SearchError,
    SearchTimeoutError,
)

__all__ = [
    "InvalidHeuristicError",
    "InvalidNodeError",
    "NoSolutionFoundError",
    "SearchError",
    "SearchTimeoutError",
]
