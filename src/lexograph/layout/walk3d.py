"""The 3-D corkscrew layout: the 2-D walk lifted by a constant step in z.

This is the 2-D turtle walk (:func:`lexograph.layout.walk.walk_layout`) with a
fixed vertical lift added per unit, so the rectangular walk winds upward into a
corkscrew. It mirrors the Wittgenstein piece's helical handwriting layout, where
each sentence both advances the in-plane turtle and climbs a constant ``z_step``.
The geometry is plain coordinate generation; the renderer is matplotlib 3-D.
"""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from lexograph._types import Coords
from lexograph.layout.walk import walk_layout

__all__ = ["walk3d_layout"]


def walk3d_layout(
    steps: Iterable[float],
    *,
    turn: float = -90.0,
    z_step: float = 1.0,
    scale: float = 1.0,
    start: tuple[float, float, float] = (0.0, 0.0, 0.0),
    heading: tuple[float, float] = (1.0, 0.0),
) -> Coords:
    """Walk the 2-D turtle in the xy-plane while climbing a constant step in z.

    Args:
        steps: One forward (in-plane) step length per unit.
        turn: Degrees to turn the in-plane heading after each step.
        z_step: The constant vertical lift added per unit (the corkscrew pitch).
        scale: A multiplier applied to every in-plane step length.
        start: The starting ``(x, y, z)`` position.
        heading: The initial in-plane heading; normalised internally.

    Returns:
        An ``(N + 1, 3)`` float array of vertices. Row 0 is ``start``; the
        ``z`` coordinate of row ``i`` is ``start[2] + i * z_step``.

    Contract:
        - The result has exactly ``N + 1`` rows for ``N`` steps.
        - The ``z`` column increases by exactly ``z_step`` between consecutive
          rows.
        - The ``xy`` columns equal the 2-D walk with the same parameters.

    Examples:
        >>> walk3d_layout([1.0, 1.0], z_step=2.0).round(6).tolist()
        [[0.0, 0.0, 0.0], [1.0, 0.0, 2.0], [1.0, -1.0, 4.0]]
    """
    lengths = list(steps)
    xy = walk_layout(
        lengths,
        turn=turn,
        scale=scale,
        start=(start[0], start[1]),
        heading=heading,
    )
    z = start[2] + np.arange(len(lengths) + 1, dtype=float) * z_step
    return np.column_stack([xy, z])
