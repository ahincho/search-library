"""Edge representation for weighted graphs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Edge(Generic[T]):
    """Represents a weighted edge in a graph.

    Attributes:
        source: The source node identifier.
        target: The target node identifier.
        weight: The cost/weight of traversing this edge.
    """

    source: T
    target: T
    weight: float = 1.0

    def __post_init__(self) -> None:
        """Validate edge weight is non-negative."""
        if self.weight < 0:
            msg = f"Edge weight must be non-negative, got {self.weight}"
            raise ValueError(msg)

    def reversed(self) -> Edge[T]:
        """Return a new edge with source and target swapped.

        Returns:
            A new Edge with reversed direction and same weight.
        """
        return Edge(source=self.target, target=self.source, weight=self.weight)
