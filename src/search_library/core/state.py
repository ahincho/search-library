"""State protocol for search problems."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class State(Protocol):
    """Protocol defining the interface for a search state.

    Any object that is hashable and supports equality comparison
    can be used as a state in search problems.
    """

    def __hash__(self) -> int:
        """Return hash of the state for use in sets and dicts."""
        ...

    def __eq__(self, other: object) -> bool:
        """Check equality between states."""
        ...
