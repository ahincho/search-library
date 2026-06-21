"""Base interface for search algorithms."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic

from search_library.core.problem import SearchProblem
from search_library.core.result import SearchResult
from search_library.core.types import T


class SearchAlgorithm(ABC, Generic[T]):
    """Abstract base class for all search algorithms.

    Provides a unified interface for search algorithms that operate
    on SearchProblem instances and return SearchResult.
    """

    def __init__(self, problem: SearchProblem[T]) -> None:
        """Initialize with a search problem.

        Args:
            problem: The search problem to solve.
        """
        self._problem = problem

    @abstractmethod
    def search(
        self,
        *,
        max_iterations: int | None = None,
        strict: bool = False,
        track_explored: bool = False,
    ) -> SearchResult[T]:
        """Execute the search algorithm.

        Args:
            max_iterations: Maximum node expansions before aborting.
            strict: If True, raises exceptions on failure.
            track_explored: If True, populates explored_states in result.

        Returns:
            SearchResult containing path, cost, and stats.
        """
