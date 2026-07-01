"""The dispersion grid: where terms fall across a text (and texts/time).

The concordance preset plots a term's *dispersion* — a different grid from the
recurrence dotplot. Here one axis is position in the text and the other indexes
the terms (or, across a corpus, the texts or time slices); each occurrence is a
tick. This module produces the plain per-term offset arrays the preset draws,
plus keyword-in-context (KWIC) lines.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np

from lexograph._types import FloatArray
from lexograph.segment.units import tokens

__all__ = ["term_offsets", "kwic", "KWIC"]


def term_offsets(
    text: str,
    terms: Sequence[str],
    *,
    ignore_case: bool = True,
) -> dict[str, FloatArray]:
    """Return the token offsets at which each term occurs, in order.

    Args:
        text: The source text.
        terms: The terms to locate (each matched as a whole token).
        ignore_case: Match case-insensitively.

    Returns:
        A mapping from each input term to a float array of the token indices at
        which it occurs (empty if it never does). The mapping preserves the
        order of ``terms``.

    Examples:
        >>> offsets = term_offsets("the cat and the dog and the cat", ["cat", "dog"])
        >>> offsets["cat"].tolist()
        [1.0, 7.0]
        >>> offsets["dog"].tolist()
        [4.0]
    """
    toks = tokens(text)
    haystack = [t.lower() for t in toks] if ignore_case else toks
    result: dict[str, FloatArray] = {}
    for term in terms:
        needle = term.lower() if ignore_case else term
        positions = [i for i, tok in enumerate(haystack) if tok == needle]
        result[term] = np.asarray(positions, dtype=float)
    return result


@dataclass(frozen=True, slots=True)
class KWIC:
    """One keyword-in-context line.

    Attributes:
        offset: The token index of the keyword.
        left: The context tokens to the left, space-joined.
        keyword: The matched token, as it appeared in the text.
        right: The context tokens to the right, space-joined.
    """

    offset: int
    left: str
    keyword: str
    right: str


def kwic(
    text: str,
    term: str,
    *,
    width: int = 5,
    ignore_case: bool = True,
) -> list[KWIC]:
    """Return keyword-in-context lines for ``term``.

    Args:
        text: The source text.
        term: The term to find (matched as a whole token).
        width: How many context tokens to keep on each side.
        ignore_case: Match case-insensitively.

    Returns:
        One :class:`KWIC` per occurrence, in text order.

    Raises:
        ValueError: If ``width`` is negative.

    Examples:
        >>> lines = kwic("the small cat sat on the cat mat", "cat", width=2)
        >>> len(lines)
        2
        >>> lines[0].left, lines[0].keyword, lines[0].right
        ('the small', 'cat', 'sat on')
    """
    if width < 0:
        msg = f"width must be non-negative, got {width}"
        raise ValueError(msg)
    toks = tokens(text)
    haystack = [t.lower() for t in toks] if ignore_case else toks
    needle = term.lower() if ignore_case else term
    lines: list[KWIC] = []
    for i, tok in enumerate(haystack):
        if tok != needle:
            continue
        left = " ".join(toks[max(0, i - width) : i])
        right = " ".join(toks[i + 1 : i + 1 + width])
        lines.append(KWIC(offset=i, left=left, keyword=toks[i], right=right))
    return lines
