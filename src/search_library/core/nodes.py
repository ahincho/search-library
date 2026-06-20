"""Node representation for search algorithms."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(order=False)
class Node(Generic[T]):
    """Represents a node in the search tree.

    Attributes:
        state: The state this node represents.
        parent: The parent node in the search tree (None for root).
        g_cost: The cost from the start node to this node.
        h_cost: The heuristic estimate from this node to the goal.
        f_cost: The total estimated cost (g + h).
    """

    state: T
    parent: Node[T] | None = field(default=None, repr=False)
    g_cost: float = 0.0
    h_cost: float = 0.0
    f_cost: float = field(init=False)

    def __post_init__(self) -> None:
        """Calculate f_cost after initialization."""
        self.f_cost = self.g_cost + self.h_cost

    def __lt__(self, other: object) -> bool:
        """Compare nodes by f_cost for priority queue ordering."""
        if not isinstance(other, Node):
            return NotImplemented
        return self.f_cost < other.f_cost

    def __le__(self, other: object) -> bool:
        """Compare nodes by f_cost."""
        if not isinstance(other, Node):
            return NotImplemented
        return self.f_cost <= other.f_cost

    def reconstruct_path(self) -> list[T]:
        """Reconstruct the path from start to this node.

        Returns:
            List of states from start to current node (inclusive).
        """
        path: list[T] = []
        current: Node[T] | None = self
        while current is not None:
            path.append(current.state)
            current = current.parent
        path.reverse()
        return path
