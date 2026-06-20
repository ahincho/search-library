"""Custom exceptions for the search library."""


class SearchError(Exception):
    """Base exception for all search library errors."""


class NoSolutionFoundError(SearchError):
    """Raised when no solution exists for the search problem."""

    def __init__(self, message: str = "No solution found for the given problem") -> None:
        """Initialize with an optional message.

        Args:
            message: Error description.
        """
        super().__init__(message)


class InvalidNodeError(SearchError):
    """Raised when an invalid node is encountered."""

    def __init__(self, node: object, reason: str = "") -> None:
        """Initialize with the invalid node and reason.

        Args:
            node: The invalid node.
            reason: Why the node is invalid.
        """
        msg = f"Invalid node: {node!r}"
        if reason:
            msg += f" - {reason}"
        super().__init__(msg)


class InvalidHeuristicError(SearchError):
    """Raised when a heuristic returns an invalid value."""

    def __init__(self, value: float, reason: str = "") -> None:
        """Initialize with the invalid value and reason.

        Args:
            value: The invalid heuristic value.
            reason: Why the value is invalid.
        """
        msg = f"Invalid heuristic value: {value}"
        if reason:
            msg += f" - {reason}"
        super().__init__(msg)


class SearchTimeoutError(SearchError):
    """Raised when a search exceeds its time or iteration limit."""

    def __init__(self, limit: int, message: str = "") -> None:
        """Initialize with the limit that was exceeded.

        Args:
            limit: The limit value that was exceeded.
            message: Optional additional message.
        """
        msg = message or f"Search exceeded limit of {limit} iterations"
        super().__init__(msg)
