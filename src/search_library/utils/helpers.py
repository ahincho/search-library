"""Utility helpers for the search library."""

from __future__ import annotations

from typing import TypeVar

from search_library.core.result import SearchResult

T = TypeVar("T")


def format_path(result: SearchResult[T], separator: str = " -> ") -> str:
    """Format a search result path as a readable string.

    Args:
        result: The search result to format.
        separator: String to place between path elements.

    Returns:
        Formatted path string, or "No path found" if unsuccessful.
    """
    if not result.success:
        return "No path found"
    return separator.join(str(state) for state in result.path)


def format_result_summary(result: SearchResult[T]) -> str:
    """Format a summary of the search result.

    Args:
        result: The search result to summarize.

    Returns:
        Multi-line summary string.
    """
    lines = [
        f"Success: {result.success}",
        f"Path length: {result.path_length} states ({result.steps} steps)",
        f"Total cost: {result.total_cost:.2f}",
        f"Nodes explored: {result.nodes_explored}",
    ]
    if result.success:
        lines.append(f"Path: {format_path(result)}")
    return "\n".join(lines)
