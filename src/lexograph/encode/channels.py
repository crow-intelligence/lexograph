"""Map per-unit attributes onto visual channels — the package's data seam.

Every function here accepts a **plain per-unit array** and returns matplotlib-ready
values. ``size`` comes from a scalar array; ``colour`` comes from either an array
of category labels (mapped to a qualitative palette) or an array of numeric values
(mapped through a continuous colormap). Nothing here knows where the numbers came
from, which is exactly what lets a caller drive a figure from ``length``,
``frequency``, a graph centrality, or their own column.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

import matplotlib as mpl
import numpy as np
from matplotlib.colors import Normalize

from lexograph._types import FloatArray

if TYPE_CHECKING:
    from collections.abc import Iterable

__all__ = [
    "RGBA",
    "Channels",
    "normalize_size",
    "categorical_colors",
    "continuous_colors",
]

RGBA = tuple[float, float, float, float]
"""A matplotlib ``(red, green, blue, alpha)`` colour, each component in ``[0, 1]``."""


def normalize_size(
    values: Iterable[float],
    *,
    lo: float = 6.0,
    hi: float = 24.0,
    power: float = 1.0,
) -> FloatArray:
    """Scale a per-unit scalar array into a size range.

    The values are min-max normalised to ``[0, 1]``, raised to ``power`` (a
    ``power`` above 1 compresses the low end so only the largest units stand
    out, mirroring the PageRank-driven sizing in the Wittgenstein piece), then
    mapped onto ``[lo, hi]``.

    Args:
        values: One scalar per unit (e.g. sentence length or a centrality).
        lo: The smallest output size.
        hi: The largest output size.
        power: Exponent applied to the normalised values before scaling.

    Returns:
        A float array of sizes, one per input value. A constant or empty input
        maps every unit to ``lo``.

    Raises:
        ValueError: If ``hi < lo`` or ``power`` is not positive.

    Examples:
        >>> normalize_size([0, 5, 10], lo=1.0, hi=3.0).tolist()
        [1.0, 2.0, 3.0]
    """
    if hi < lo:
        msg = f"hi ({hi}) must be >= lo ({lo})"
        raise ValueError(msg)
    if power <= 0:
        msg = f"power must be positive, got {power}"
        raise ValueError(msg)
    array = np.asarray(list(values), dtype=float)
    if array.size == 0:
        return array
    vmin, vmax = float(array.min()), float(array.max())
    if vmax == vmin:
        norm = np.zeros_like(array)
    else:
        norm = (array - vmin) / (vmax - vmin)
    return lo + (hi - lo) * norm**power


def categorical_colors(
    labels: Sequence[object], *, cmap: str | None = None
) -> list[RGBA]:
    """Map category labels to a stable qualitative palette.

    Labels are coloured in order of first appearance, so the same label always
    gets the same colour and adjacent distinct labels are visually separated.
    The default palette follows the Wittgenstein piece: ``tab20`` for up to 20
    categories, evenly spaced ``hsv`` beyond that.

    Args:
        labels: One hashable label per unit (e.g. a cluster or community id).
        cmap: Override colormap name. ``None`` selects the default by count.

    Returns:
        One RGBA colour per input label.

    Examples:
        >>> colors = categorical_colors([0, 1, 0, 2])
        >>> len(colors)
        4
        >>> colors[0] == colors[2]
        True
    """
    order: dict[object, int] = {}
    for label in labels:
        if label not in order:
            order[label] = len(order)
    count = len(order)
    if cmap is None:
        cmap = "tab20" if count <= 20 else "hsv"
    colormap = mpl.colormaps[cmap]
    if count <= 20 and cmap == "tab20":
        palette = [colormap(i) for i in range(count)]
    else:
        palette = [colormap(i / max(count, 1)) for i in range(count)]
    return [palette[order[label]] for label in labels]


def continuous_colors(values: Iterable[float], *, cmap: str = "viridis") -> list[RGBA]:
    """Map a per-unit numeric array through a continuous colormap.

    Args:
        values: One scalar per unit.
        cmap: A continuous matplotlib colormap name.

    Returns:
        One RGBA colour per value. A constant or empty input maps every unit to
        the colormap's midpoint.

    Examples:
        >>> colors = continuous_colors([0.0, 0.5, 1.0])
        >>> len(colors)
        3
    """
    array = np.asarray(list(values), dtype=float)
    colormap = mpl.colormaps[cmap]
    if array.size == 0:
        return []
    vmin, vmax = float(array.min()), float(array.max())
    if vmax == vmin:
        return [colormap(0.5) for _ in array]
    norm = Normalize(vmin=vmin, vmax=vmax)
    return [colormap(float(norm(v))) for v in array]


@dataclass(frozen=True, slots=True)
class Channels:
    """Resolved visual channels, one entry per unit.

    Attributes:
        sizes: Per-unit size in points, or ``None`` for a uniform size.
        colors: Per-unit RGBA colour, or ``None`` for a single default colour.
        glyphs: Per-unit text to draw, or ``None`` to draw markers/segments.
    """

    sizes: FloatArray | None = None
    colors: list[RGBA] | None = None
    glyphs: list[str] | None = None
