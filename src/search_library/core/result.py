"""Search result container."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic

from search_library.core.types import T


@dataclass(frozen=True)
class SearchResult(Generic[T]):
    """Container for search algorithm results.

    Attributes:
        path: The optimal path from start to goal (empty if no solution).
        total_cost: The total cost of the path.
        nodes_explored: Number of nodes explored during the search.
        success: Whether a solution was found.
        explored_states: Optional set of explored states (only populated if requested).
    """

    path: list[T] = field(default_factory=list)
    total_cost: float = 0.0
    nodes_explored: int = 0
    success: bool = False
    explored_states: frozenset[T] | None = None

    @property
    def path_length(self) -> int:
        """Return the number of states in the path."""
        return len(self.path)

    @property
    def steps(self) -> int:
        """Return the number of steps (edges) in the path."""
        return max(0, len(self.path) - 1)
