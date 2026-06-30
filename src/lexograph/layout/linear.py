"""A trivial reading-order layout: units flow left-to-right, top-to-bottom.

This is the simplest point on the layout step of the spine — it just places the
``i``-th unit on a grid in reading order. It exists so the spine
(segment → layout → encode → render) is exercisable end to end before the
richer walk, spiral, and grid layouts arrive, and it is genuinely useful on its
own for "text as a field of tiles" figures.
"""

from __future__ import annotations

import numpy as np

from lexograph._types import Coords

__all__ = ["linear_layout"]


def linear_layout(
    n: int,
    *,
    columns: int | None = None,
    col_width: float = 1.0,
    line_height: float = 1.0,
) -> Coords:
    """Lay ``n`` units out on a reading-order grid.

    Unit ``i`` is placed at column ``i % columns`` and row ``i // columns``,
    with rows running downward (decreasing ``y``) so the first unit is top-left.

    Args:
        n: The number of units to place.
        columns: Units per row. ``None`` puts them all on a single row.
        col_width: Horizontal spacing between columns.
        line_height: Vertical spacing between rows.

    Returns:
        An ``(n, 2)`` float array of ``(x, y)`` coordinates.

    Raises:
        ValueError: If ``n`` is negative or ``columns`` is not positive.

    Contract:
        - Returns exactly ``n`` rows.
        - Coordinates are deterministic in ``n`` and the spacing parameters.

    Examples:
        >>> linear_layout(3).tolist()
        [[0.0, 0.0], [1.0, 0.0], [2.0, 0.0]]
        >>> linear_layout(3, columns=2).tolist()
        [[0.0, 0.0], [1.0, 0.0], [0.0, -1.0]]
    """
    if n < 0:
        msg = f"n must be non-negative, got {n}"
        raise ValueError(msg)
    if columns is not None and columns <= 0:
        msg = f"columns must be positive, got {columns}"
        raise ValueError(msg)
    if n == 0:
        return np.zeros((0, 2), dtype=float)
    width = n if columns is None else columns
    index = np.arange(n)
    x = (index % width) * col_width
    y = -(index // width) * line_height
    return np.column_stack([x, y]).astype(float)
