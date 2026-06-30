"""The Archimedean spiral layout: place units evenly along an outward spiral.

Ported from the Wittgenstein piece's ``spiral_xy``. Units are spread by equal
*arc length* (not equal angle) along the Archimedean spiral ``r = r0 + b·theta``,
so the spacing between consecutive units stays visually uniform as the spiral
winds outward. This is the layout behind the punctuation-spiral preset, where
each non-alphanumeric mark is a unit.
"""

from __future__ import annotations

import numpy as np

from lexograph._types import Coords, FloatArray

__all__ = ["spiral_layout", "tangent_angles"]

# Resolution of the arc-length integration grid. Large enough that the
# equal-arc-length resampling is smooth for any realistic unit count.
_ARC_SAMPLES = 200_000


def spiral_layout(
    n: int,
    *,
    turns: float = 16.0,
    r0: float = 1.0,
    r_max: float = 10.0,
) -> Coords:
    """Place ``n`` units evenly by arc length along an Archimedean spiral.

    Args:
        n: The number of units to place.
        turns: How many full revolutions the spiral makes from ``r0`` to
            ``r_max``.
        r0: The starting radius (the innermost unit sits here).
        r_max: The outermost radius (the last unit sits near here).

    Returns:
        An ``(n, 2)`` float array of ``(x, y)`` positions, ordered from the
        innermost unit outward.

    Raises:
        ValueError: If ``n`` is negative, ``turns`` is not positive, or
            ``r_max < r0``.

    Contract:
        - Returns exactly ``n`` rows.
        - Radius increases monotonically from the first unit to the last.
        - The output is deterministic in its inputs.

    Examples:
        >>> coords = spiral_layout(5, turns=2.0, r0=1.0, r_max=4.0)
        >>> coords.shape
        (5, 2)
        >>> import numpy as np
        >>> radii = np.hypot(coords[:, 0], coords[:, 1])
        >>> bool(np.all(np.diff(radii) > 0))
        True
    """
    if n < 0:
        msg = f"n must be non-negative, got {n}"
        raise ValueError(msg)
    if turns <= 0:
        msg = f"turns must be positive, got {turns}"
        raise ValueError(msg)
    if r_max < r0:
        msg = f"r_max ({r_max}) must be >= r0 ({r0})"
        raise ValueError(msg)
    if n == 0:
        return np.zeros((0, 2), dtype=float)

    theta_max = 2.0 * np.pi * turns
    b = (r_max - r0) / theta_max
    grid = np.linspace(0.0, theta_max, _ARC_SAMPLES)
    r_grid = r0 + b * grid
    # Arc length ds = sqrt(r^2 + (dr/dtheta)^2) dtheta, with dr/dtheta = b.
    integrand = np.hypot(r_grid, b)
    arc = np.concatenate([[0.0], np.cumsum(np.diff(grid) * integrand[:-1])])
    theta = np.interp(np.linspace(0.0, arc[-1], n), arc, grid)
    r = r0 + b * theta
    x, y = r * np.cos(theta), r * np.sin(theta)
    return np.column_stack([x, y]).astype(float)


def tangent_angles(coords: Coords) -> FloatArray:
    """Return the tangent direction (degrees) of an ordered path at each point.

    Computed from the local gradient of the coordinates, this orients per-unit
    glyphs so they follow the curve (used to set the rotation of each mark on
    the punctuation spiral).

    Args:
        coords: An ``(N, 2)`` array of ordered positions.

    Returns:
        A length-``N`` array of tangent angles in degrees.

    Raises:
        ValueError: If ``coords`` is not ``(N, 2)``.

    Examples:
        >>> import numpy as np
        >>> tangent_angles(np.array([[0.0, 0.0], [1.0, 0.0], [2.0, 0.0]])).tolist()
        [0.0, 0.0, 0.0]
    """
    array = np.asarray(coords, dtype=float)
    if array.ndim != 2 or array.shape[1] != 2:
        msg = f"coords must have shape (N, 2), got {array.shape}"
        raise ValueError(msg)
    if array.shape[0] == 0:
        return np.zeros((0,), dtype=float)
    dx = np.gradient(array[:, 0])
    dy = np.gradient(array[:, 1])
    return np.degrees(np.arctan2(dy, dx))
