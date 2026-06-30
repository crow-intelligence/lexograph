"""Punctuation-spiral preset: every mark of a text along an Archimedean spiral.

Each non-alphanumeric, non-whitespace character of the text becomes a unit and
is placed, in reading order, along an outward Archimedean spiral (see
:func:`lexograph.layout.spiral.spiral_layout`). Ordinary punctuation is set in a
dim warm grey; logical, mathematical, and Greek signs are picked out in a gold
accent, set bold and a little larger so they read out of the ribbon. The marks
grow gently in size as the spiral winds outward.

Ported from the Wittgenstein piece's punctuation-spiral generator, minus the
central portrait (a cosmetic the core does not need). The figure is built
directly, so it stays headless and returns a :class:`matplotlib.figure.Figure`.
"""

from __future__ import annotations

import numpy as np
from matplotlib.figure import Figure

from lexograph.layout.spiral import spiral_layout, tangent_angles
from lexograph.render.mpl import frame_axes
from lexograph.segment.units import characters

__all__ = ["punctuation_spiral", "is_accent"]

_BACKGROUND = "#1a1a1f"
_DIM = "#cfc7b3"  # ordinary punctuation — warm grey, legible on dark
_ACCENT = "#f0cf7f"  # logical / mathematical / Greek — gold
_ACCENT_SCALE = 1.6  # accent marks render this much larger so they pop

# Logical, mathematical, and Greek signs get the accent colour. The explicit
# set covers the common marks; the codepoint ranges future-proof it.
_ACCENT_CHARS = frozenset("∃∨∼⊃∑≡×′♯♭=~±÷∞∂∇∈∉⊂⊆⊇∧¬∀→↔⇒⇔")
_ACCENT_RANGES = (
    (0x2200, 0x22FF),  # Mathematical Operators
    (0x2A00, 0x2AFF),  # Supplemental Mathematical Operators
    (0x0370, 0x03FF),  # Greek and Coptic
    (0x1F00, 0x1FFF),  # Greek Extended
    (0x2100, 0x214F),  # Letterlike Symbols
    (0x27C0, 0x27EF),  # Miscellaneous Mathematical Symbols-A
)


def is_accent(char: str) -> bool:
    """Return whether ``char`` is a logical, mathematical, or Greek sign.

    Args:
        char: A single character.

    Returns:
        ``True`` if the character should take the gold accent colour.

    Examples:
        >>> is_accent("=")
        True
        >>> is_accent(",")
        False
    """
    if char in _ACCENT_CHARS:
        return True
    codepoint = ord(char)
    return any(lo <= codepoint <= hi for lo, hi in _ACCENT_RANGES)


def _marks(text: str) -> list[str]:
    """Punctuation and symbols in order (drop letters, digits, and whitespace)."""
    return [c for c in characters(text) if not c.isalnum() and not c.isspace()]


def punctuation_spiral(
    text: str,
    *,
    turns: float = 16.0,
    size_min: float = 7.0,
    size_max: float = 12.0,
    figsize: tuple[float, float] = (9.0, 9.0),
) -> Figure:
    """Draw a text's punctuation and logical signs as a spiral plate.

    Args:
        text: The source text.
        turns: How many revolutions the spiral makes.
        size_min: Font size (points) of the innermost marks.
        size_max: Font size (points) of the outermost marks.
        figsize: Figure size in inches.

    Returns:
        A :class:`matplotlib.figure.Figure` with one axes, dark-themed. Never
        calls ``show()``, so it renders inline in Jupyter and saves with
        ``fig.savefig(...)``.

    Raises:
        ValueError: If ``text`` contains no punctuation or symbol marks.

    Contract:
        - Returns a Figure with exactly one axes.
        - Accent marks (logical/mathematical/Greek) are drawn larger and on top.

    Examples:
        >>> from lexograph import load_demo_text
        >>> fig = punctuation_spiral(load_demo_text())
        >>> type(fig).__name__
        'Figure'
        >>> len(fig.axes)
        1
    """
    marks = _marks(text)
    if not marks:
        msg = "text contains no punctuation or symbol marks to plot"
        raise ValueError(msg)

    n = len(marks)
    coords = spiral_layout(n, turns=turns, r0=1.0, r_max=10.0)
    angles = tangent_angles(coords)
    # Marks grow linearly in size from the centre outward.
    sizes = np.linspace(size_min, size_max, n)

    fig = Figure(figsize=figsize, facecolor=_BACKGROUND)
    ax = fig.subplots()
    ax.set_facecolor(_BACKGROUND)

    for i, mark in enumerate(marks):
        accent = is_accent(mark)
        ax.text(
            coords[i, 0],
            coords[i, 1],
            mark,
            fontsize=sizes[i] * (_ACCENT_SCALE if accent else 1.0),
            color=_ACCENT if accent else _DIM,
            fontweight="bold" if accent else "normal",
            rotation=angles[i],
            ha="center",
            va="center",
            zorder=3 if accent else 2,
        )

    frame_axes(ax, coords, margin=0.08)
    fig.tight_layout()
    return fig
