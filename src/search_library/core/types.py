"""Core type definitions for the search library."""

from __future__ import annotations

from collections.abc import Hashable
from typing import TypeVar

# Central TypeVar bound to Hashable — ensures all states can be used in sets/dicts.
T = TypeVar("T", bound=Hashable)
