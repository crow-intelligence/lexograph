"""Tiny bundled text for docs, tests, and every preset's worked example.

The demo text is the first chapter of Jane Austen's *Pride and Prejudice*
(public domain; see :mod:`lexograph.datasets._pride_and_prejudice`). It is large
enough to make a walk, spiral, dotplot, or concordance legible, and small enough
to keep the wheel tiny and the doctests fast.
"""

from __future__ import annotations

from lexograph.datasets._pride_and_prejudice import PRIDE_AND_PREJUDICE_CH1


def load_demo_text() -> str:
    """Return the bundled demo text: Chapter 1 of *Pride and Prejudice*.

    Returns:
        The chapter as a single string, paragraphs separated by blank lines.

    Examples:
        >>> text = load_demo_text()
        >>> text.startswith("It is a truth universally acknowledged")
        True
        >>> "Bingley" in text
        True
    """
    return PRIDE_AND_PREJUDICE_CH1


__all__ = ["load_demo_text"]
