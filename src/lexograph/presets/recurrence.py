"""Recurrence-dotplot preset: a text plotted against itself.

The text is segmented into sentences; the preset draws the sentence × sentence
self-similarity grid (see :mod:`lexograph.layout.recurrence`) with matplotlib
``imshow``. Lit cells off the main diagonal mark sentences that echo each other —
recurring themes, repeated phrasing, digressions that return.

The default distance is the dependency-free token/character Jaccard, so the plot
needs no analysis stack; pass a precomputed ``distances`` matrix (e.g. an
embedding distance from the ``[graph]`` extra) to drive it from semantics.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import numpy as np
from matplotlib.figure import Figure

from lexograph.layout.recurrence import recurrence_distances, recurrence_matrix
from lexograph.segment.units import sentences as split_sentences

if TYPE_CHECKING:
    from lexograph._types import FloatArray

__all__ = ["recurrence_plot"]

RecurrenceMode = Literal["binary", "distance"]


def recurrence_plot(
    text: str,
    *,
    threshold: float = 0.6,
    shingle: int | None = None,
    distances: FloatArray | None = None,
    mode: RecurrenceMode = "binary",
    figsize: tuple[float, float] = (8.0, 8.0),
    background: str = "white",
) -> Figure:
    """Draw the sentence × sentence recurrence dotplot of a text.

    Args:
        text: The source text.
        threshold: In ``"binary"`` mode, cells with distance ``<= threshold`` are
            lit.
        shingle: Passed to :func:`lexograph.layout.recurrence.recurrence_distances`
            — ``None`` for word-token Jaccard, or ``k`` for character ``k``-gram
            Jaccard. Ignored when ``distances`` is given.
        distances: A precomputed ``(N, N)`` distance matrix to use instead of the
            built-in Jaccard (e.g. an embedding distance from the ``[graph]``
            extra). Must match the sentence count.
        mode: ``"binary"`` draws the thresholded dotplot; ``"distance"`` draws the
            full similarity heatmap.
        figsize: Figure size in inches.
        background: Figure background colour.

    Returns:
        A :class:`matplotlib.figure.Figure` with one axes. Never calls ``show()``.

    Raises:
        ValueError: If the text has fewer than two sentences, or a supplied
            ``distances`` matrix does not match the sentence count.

    Contract:
        - Returns a Figure with exactly one axes.
        - The grid is square (sentence count on each axis) and symmetric.

    Examples:
        >>> from lexograph import load_demo_text
        >>> fig = recurrence_plot(load_demo_text())
        >>> type(fig).__name__
        'Figure'
    """
    units = split_sentences(text)
    n = len(units)
    if n < 2:
        msg = f"need at least two sentences for a recurrence plot, got {n}"
        raise ValueError(msg)

    if distances is not None:
        dist = np.asarray(distances, dtype=float)
        if dist.shape != (n, n):
            msg = f"distances must have shape ({n}, {n}), got {dist.shape}"
            raise ValueError(msg)
    else:
        dist = recurrence_distances(units, shingle=shingle)

    fig = Figure(figsize=figsize, facecolor=background)
    ax = fig.subplots()
    ax.set_facecolor(background)

    if mode == "distance":
        # Low distance (similar) renders dark.
        ax.imshow(dist, cmap="Greys_r", origin="upper", interpolation="nearest")
    else:
        grid = recurrence_matrix(dist, threshold=threshold)
        ax.imshow(grid, cmap="Greys", origin="upper", interpolation="nearest")

    ax.set_xlabel("sentence index")
    ax.set_ylabel("sentence index")
    ax.set_title("Recurrence dotplot")
    fig.tight_layout()
    return fig
