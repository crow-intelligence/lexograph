"""Measure the rendered width of each unit's text, headlessly.

The Wittgenstein piece's key refinement over the original turtle POC was to step
the walk by each sentence's *rendered width* — the width it actually occupies
when set in a font — instead of a flat ``length / 15``. That version measured
the width inside Blender; here we rebuild it headlessly with matplotlib's
:class:`~matplotlib.textpath.TextPath`, which lays out glyph outlines without a
display, canvas, or font server. The resulting per-unit widths feed straight
into :func:`lexograph.layout.walk.walk_layout` as step lengths.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import numpy as np
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath

from lexograph._types import FloatArray

__all__ = ["rendered_widths"]


def _as_font_properties(prop: FontProperties | str | Path | None) -> FontProperties:
    """Coerce a font argument into a :class:`FontProperties`."""
    if prop is None:
        return FontProperties()
    if isinstance(prop, FontProperties):
        return prop
    return FontProperties(fname=str(prop))


def rendered_widths(
    strings: Iterable[str],
    *,
    prop: FontProperties | str | Path | None = None,
    size: float = 12.0,
) -> FloatArray:
    """Return the rendered width of each string, set in the given font.

    Args:
        strings: One string per unit (typically the sentences).
        prop: The font to measure with — a :class:`FontProperties`, a path to a
            ``.ttf``/``.otf`` file, or ``None`` for matplotlib's default font.
        size: The font size to measure at (in points).

    Returns:
        A float array of widths, one per input string. Empty or whitespace-only
        strings get a width proportional to their character count so the walk
        still advances past them.

    Contract:
        - The result has one entry per input string, all non-negative.
        - Widths are deterministic for a given font, size, and string.

    Examples:
        >>> w = rendered_widths(["i", "wwww"])
        >>> bool(w[1] > w[0])
        True
    """
    font = _as_font_properties(prop)
    widths: list[float] = []
    for string in strings:
        widths.append(_one_width(string, font, size))
    return np.asarray(widths, dtype=float)


def _one_width(string: str, font: FontProperties, size: float) -> float:
    """Measure one string's width, falling back to a per-character estimate."""
    # Whitespace, empty, and any string whose glyphs cannot be laid out have no
    # usable outline extent; advance by a plain per-character estimate so the
    # turtle still moves on past them.
    estimate = len(string) * size * 0.3
    if string.strip() == "":
        return estimate
    try:
        width = float(
            TextPath((0.0, 0.0), string, size=size, prop=font).get_extents().width
        )
    except (ValueError, RuntimeError):
        return estimate
    if not np.isfinite(width) or width < 0.0:
        return estimate
    return width
