"""Text-walk preset: each sentence steps forward and turns, space-filling.

This is the 2-D walk. Each sentence is a unit; the turtle steps forward by the
sentence's rendered width (the Wittgenstein refinement — measured headlessly,
see :func:`lexograph.layout.widths.rendered_widths`) and turns 90° between
sentences. Per-unit attributes drive the visual channels: ``size`` sets the
stroke weight (or glyph size) and ``colour`` tints each step. With no channels
supplied the walk falls back to dependency-free built-ins — stroke by sentence
length, colour by position in the text — so it works with no analysis stack at
all.

Two modes: ``"path"`` draws the walk as a multi-coloured ribbon; ``"glyphs"``
sets each sentence's text along its segment (calligraphy-on-path).
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Literal, cast

import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.figure import Figure

from lexograph.encode.channels import (
    categorical_colors,
    continuous_colors,
    normalize_size,
)
from lexograph.layout.walk import heading_angles, walk_layout
from lexograph.layout.walk3d import walk3d_layout
from lexograph.layout.widths import rendered_widths
from lexograph.render.mpl import frame_axes
from lexograph.render.mpl3d import render_path_3d
from lexograph.segment.units import sentences as split_sentences

if TYPE_CHECKING:
    from matplotlib.font_manager import FontProperties

    from lexograph.encode.channels import RGBA

__all__ = ["text_walk"]

WalkMode = Literal["path", "glyphs"]
ColourKind = Literal["auto", "categorical", "continuous"]


def _resolve_colours(
    colour: Sequence[object] | None,
    n: int,
    kind: ColourKind,
) -> list[RGBA]:
    """Turn a per-unit colour channel into one RGBA per unit."""
    if colour is None:
        return continuous_colors(np.arange(n, dtype=float))
    values = list(colour)
    if len(values) != n:
        msg = f"colour must have one entry per sentence ({n}), got {len(values)}"
        raise ValueError(msg)
    if kind == "auto":
        numeric = all(
            isinstance(v, (int, float, np.integer, np.floating))
            and not isinstance(v, bool)
            for v in values
        )
        kind = "continuous" if numeric else "categorical"
    if kind == "continuous":
        return continuous_colors(cast("list[float]", values))
    return categorical_colors(values)


def text_walk(
    text: str,
    *,
    colour: Sequence[object] | None = None,
    colour_kind: ColourKind = "auto",
    size: Sequence[float] | None = None,
    mode: WalkMode = "path",
    helix: bool = False,
    z_step: float = 1.0,
    font: FontProperties | str | Path | None = None,
    font_size: float = 12.0,
    width_step: bool = True,
    turn: float = -90.0,
    background: str = "white",
    figsize: tuple[float, float] | None = None,
) -> Figure:
    """Draw a text as a space-filling turtle walk over its sentences.

    Args:
        text: The source text.
        colour: One value per sentence for the colour channel (category labels or
            numeric values). ``None`` colours by position in the text.
        colour_kind: How to read ``colour``: ``"categorical"``, ``"continuous"``,
            or ``"auto"`` (numeric values continuous, everything else categorical).
        size: One scalar per sentence for the size channel. ``None`` sizes by
            sentence length.
        mode: ``"path"`` draws a multi-coloured ribbon; ``"glyphs"`` sets each
            sentence's text along its segment. Only ``"path"`` is supported when
            ``helix`` is set.
        helix: If ``True``, lift the walk into a 3-D corkscrew (each sentence also
            climbs ``z_step``) and render it in matplotlib 3-D.
        z_step: The vertical lift per sentence for the corkscrew (used when
            ``helix`` is set).
        font: Font to measure widths and (in glyph mode) draw with.
        font_size: Base font size in points for width measurement and glyphs.
        width_step: If ``True``, step by each sentence's rendered width; if
            ``False``, step by its character count.
        turn: Degrees to turn between sentences (``-90`` is the rectangular walk).
        background: Figure and axes background colour.
        figsize: Figure size in inches. Defaults to ``(10, 10)`` flat, or
            ``(8, 10)`` for the helix.

    Returns:
        A :class:`matplotlib.figure.Figure` with one axes (2-D, or 3-D for the
        helix). Never calls ``show()``.

    Raises:
        ValueError: If the text has fewer than two sentences, a channel length
            does not match the sentence count, or ``helix`` is combined with
            glyph mode.

    Contract:
        - Returns a Figure with exactly one axes.
        - The colour and size channels stay aligned with the sentences.

    Examples:
        >>> from lexograph import load_demo_text
        >>> fig = text_walk(load_demo_text())
        >>> type(fig).__name__
        'Figure'
        >>> helix = text_walk(load_demo_text(), helix=True)
        >>> type(helix).__name__
        'Figure'
    """
    if helix and mode == "glyphs":
        msg = "glyph mode is not supported for the 3-D helix walk"
        raise ValueError(msg)
    units = split_sentences(text)
    n = len(units)
    if n < 2:
        msg = f"need at least two sentences to walk, got {n}"
        raise ValueError(msg)

    if width_step:
        steps = rendered_widths(units, prop=font, size=font_size)
    else:
        steps = np.array([len(u) for u in units], dtype=float)

    colours = _resolve_colours(colour, n, colour_kind)
    raw_size = [float(s) for s in size] if size is not None else [len(u) for u in units]
    if len(raw_size) != n:
        msg = f"size must have one entry per sentence ({n}), got {len(raw_size)}"
        raise ValueError(msg)
    weight = normalize_size(raw_size, lo=0.0, hi=1.0)

    if helix:
        coords3d = walk3d_layout(steps, turn=turn, z_step=z_step)
        return render_path_3d(
            coords3d,
            colors=colours,
            linewidths=[0.6 + 6.0 * float(w) for w in weight],
            background=background,
            figsize=figsize or (8.0, 10.0),
        )

    coords = walk_layout(steps, turn=turn)
    fig = Figure(figsize=figsize or (10.0, 10.0), facecolor=background)
    ax = fig.subplots()
    ax.set_facecolor(background)

    if mode == "glyphs":
        angles = heading_angles(steps, turn=turn)
        mids = (coords[:-1] + coords[1:]) / 2.0
        glyph_sizes = font_size * (0.6 + 2.4 * weight)
        for i, unit in enumerate(units):
            ax.text(
                mids[i, 0],
                mids[i, 1],
                unit,
                fontsize=glyph_sizes[i],
                color=colours[i],
                rotation=angles[i],
                rotation_mode="anchor",
                ha="center",
                va="center",
                fontproperties=font,
            )
    else:
        segments = list(np.stack([coords[:-1], coords[1:]], axis=1))
        linewidths = 0.6 + 6.0 * weight
        ax.add_collection(
            LineCollection(segments, colors=colours, linewidths=linewidths)
        )

    frame_axes(ax, coords)
    fig.tight_layout()
    return fig
