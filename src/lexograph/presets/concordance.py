"""Concordance preset: a term's dispersion across the text, with optional KWIC.

For each term, every occurrence is a tick at its token offset; the terms stack on
the vertical axis. This is the classic lexical-dispersion plot — a *term × text*
grid, distinct from the recurrence dotplot's *sentence × sentence* self-similarity.
Keyword-in-context (KWIC) lines for any term are available from
:func:`lexograph.layout.dispersion.kwic`.
"""

from __future__ import annotations

from collections.abc import Sequence

from matplotlib.figure import Figure

from lexograph.encode.channels import categorical_colors
from lexograph.layout.dispersion import term_offsets
from lexograph.segment.units import tokens

__all__ = ["concordance"]


def concordance(
    text: str,
    terms: Sequence[str],
    *,
    ignore_case: bool = True,
    normalize: bool = False,
    figsize: tuple[float, float] | None = None,
    background: str = "white",
) -> Figure:
    """Draw a lexical-dispersion plot of where each term falls in the text.

    Args:
        text: The source text.
        terms: The terms to plot, one row each (top to bottom in this order).
        ignore_case: Match terms case-insensitively.
        normalize: If ``True``, scale the x-axis to ``[0, 1]`` (fraction of the
            text) instead of absolute token offset.
        figsize: Figure size in inches. Defaults to a height that grows with the
            number of terms.
        background: Figure and axes background colour.

    Returns:
        A :class:`matplotlib.figure.Figure` with one axes. Never calls ``show()``.

    Raises:
        ValueError: If ``terms`` is empty.

    Contract:
        - Returns a Figure with exactly one axes.
        - There is exactly one y-row per term, in the given order.

    Examples:
        >>> from lexograph import load_demo_text
        >>> fig = concordance(load_demo_text(), ["Bennet", "Bingley", "wife"])
        >>> type(fig).__name__
        'Figure'
        >>> len(fig.axes[0].get_yticks())
        3
    """
    if len(terms) == 0:
        msg = "need at least one term for a concordance plot"
        raise ValueError(msg)

    total = len(tokens(text))
    span = float(total) if total else 1.0
    offsets = term_offsets(text, terms, ignore_case=ignore_case)
    colours = categorical_colors(list(range(len(terms))))

    if figsize is None:
        figsize = (10.0, 0.6 * len(terms) + 1.5)
    fig = Figure(figsize=figsize, facecolor=background)
    ax = fig.subplots()
    ax.set_facecolor(background)

    for row, term in enumerate(terms):
        xs = offsets[term]
        if normalize and len(xs):
            xs = xs / span
        if len(xs):
            ax.vlines(xs, row - 0.4, row + 0.4, color=colours[row])

    ax.set_yticks(range(len(terms)))
    ax.set_yticklabels(list(terms))
    ax.set_ylim(-0.5, len(terms) - 0.5)
    ax.invert_yaxis()  # first term on top
    ax.set_xlim(0.0, 1.0 if normalize else span)
    ax.set_xlabel(
        "position in text" + (" (fraction)" if normalize else " (token offset)")
    )
    ax.set_title("Lexical dispersion")
    fig.tight_layout()
    return fig
