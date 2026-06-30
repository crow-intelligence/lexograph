"""Dependency-free per-unit scalars for the visual channels.

These are the built-in channel sources that need no analysis stack: a unit's
length, its position in the sequence, and how often each unit's value recurs.
They satisfy the same plain-array contract as the optional ``analyze`` layer, so
a walk or spiral can be driven by them with nothing installed beyond the core.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence

import numpy as np

from lexograph._types import FloatArray

__all__ = ["lengths", "positions", "frequencies"]


def lengths(units: Sequence[str]) -> FloatArray:
    """Return the character length of each unit.

    Args:
        units: The segmented units.

    Returns:
        A float array of per-unit character counts.

    Examples:
        >>> lengths(["hi", "there"]).tolist()
        [2.0, 5.0]
    """
    return np.asarray([len(u) for u in units], dtype=float)


def positions(n: int) -> FloatArray:
    """Return ``0, 1, ..., n - 1`` as a position channel.

    Args:
        n: The number of units.

    Returns:
        A float array of positions in sequence order.

    Examples:
        >>> positions(3).tolist()
        [0.0, 1.0, 2.0]
    """
    return np.arange(n, dtype=float)


def frequencies(units: Sequence[str], *, ignore_case: bool = True) -> FloatArray:
    """Return how many times each unit's value occurs in the sequence.

    Args:
        units: The segmented units (typically tokens).
        ignore_case: Count case-insensitively.

    Returns:
        A float array the same length as ``units``; entry ``i`` is the total
        number of occurrences of ``units[i]``.

    Examples:
        >>> frequencies(["the", "cat", "the"]).tolist()
        [2.0, 1.0, 2.0]
    """
    keys = [u.lower() for u in units] if ignore_case else list(units)
    counts = Counter(keys)
    return np.asarray([counts[k] for k in keys], dtype=float)
