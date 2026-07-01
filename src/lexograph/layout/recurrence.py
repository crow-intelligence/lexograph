"""The recurrence grid: a text's self-similarity, sentence against sentence.

The recurrence dotplot is the only layout that plots a text against *itself*. The
units are sentences; cell ``(i, j)`` measures how similar sentence ``i`` is to
sentence ``j``. Thresholding the distances turns the grid into a dotplot whose
lit cells expose internal echo structure — recurring themes, repeated phrasing,
digressions that return.

The built-in, dependency-free distance is token-set **Jaccard** (or character
n-gram Jaccard), so the grid works with no analysis stack. The ``[graph]`` extra
can supply an embedding distance matrix instead; pass it straight to
:func:`recurrence_matrix` or the preset.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from lexograph._types import FloatArray

__all__ = ["recurrence_distances", "recurrence_matrix"]


def _features(units: Sequence[str], shingle: int | None) -> list[frozenset[str]]:
    """Build a comparable feature set per unit: word tokens or char n-grams."""
    import re

    token_re = re.compile(r"\w+(?:['’-]\w+)*")
    features: list[frozenset[str]] = []
    for unit in units:
        lowered = unit.lower()
        if shingle is None:
            features.append(frozenset(token_re.findall(lowered)))
        else:
            squeezed = "".join(lowered.split())
            grams = {
                squeezed[i : i + shingle] for i in range(len(squeezed) - shingle + 1)
            }
            features.append(frozenset(grams))
    return features


def recurrence_distances(
    units: Sequence[str],
    *,
    shingle: int | None = None,
) -> FloatArray:
    """Return the pairwise Jaccard distance matrix between units.

    Args:
        units: The sentences (or any strings) to compare against each other.
        shingle: If ``None``, compare lowercased word-token sets. If a positive
            integer ``k``, compare sets of character ``k``-grams instead (robust
            to short or morphologically varied sentences).

    Returns:
        An ``(N, N)`` symmetric float array of Jaccard distances in ``[0, 1]``
        with a zero diagonal. Two units with no features in common are at
        distance 1; two empty units are at distance 0.

    Contract:
        - The matrix is symmetric with a zero diagonal.
        - Every entry lies in ``[0, 1]``.

    Examples:
        >>> d = recurrence_distances(["the cat sat", "the cat sat", "a dog ran"])
        >>> float(d[0, 1])
        0.0
        >>> bool(d[0, 2] > 0.9)
        True
    """
    n = len(units)
    features = _features(units, shingle)
    dist = np.zeros((n, n), dtype=float)
    for i in range(n):
        fi = features[i]
        for j in range(i + 1, n):
            fj = features[j]
            union = len(fi | fj)
            similarity = (len(fi & fj) / union) if union else 1.0
            dist[i, j] = dist[j, i] = 1.0 - similarity
    return dist


def recurrence_matrix(
    distances: FloatArray,
    *,
    threshold: float = 0.6,
) -> np.ndarray:
    """Threshold a distance matrix into a boolean recurrence (dotplot) grid.

    Args:
        distances: An ``(N, N)`` distance matrix (from
            :func:`recurrence_distances`, or an embedding distance matrix from
            the ``[graph]`` extra).
        threshold: Cells with distance ``<= threshold`` are lit (recurrent).

    Returns:
        An ``(N, N)`` boolean array; ``True`` marks a recurrent (similar) cell.
        The diagonal is always ``True`` (every sentence echoes itself).

    Raises:
        ValueError: If ``distances`` is not a square 2-D matrix.

    Examples:
        >>> import numpy as np
        >>> d = np.array([[0.0, 0.2, 0.9], [0.2, 0.0, 0.8], [0.9, 0.8, 0.0]])
        >>> recurrence_matrix(d, threshold=0.5).tolist()
        [[True, True, False], [True, True, False], [False, False, True]]
    """
    array = np.asarray(distances, dtype=float)
    if array.ndim != 2 or array.shape[0] != array.shape[1]:
        msg = f"distances must be a square (N, N) matrix, got {array.shape}"
        raise ValueError(msg)
    return array <= threshold
