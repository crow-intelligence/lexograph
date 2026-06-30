"""Shared type aliases for the lexograph package.

The visual-channel arrays named here are the package's public data contract:
``encode`` accepts plain per-unit arrays, and ``analyze``/``integrations`` only
ever *produce* arrays that satisfy these aliases. Nothing in the core needs to
know where the numbers came from.
"""

from __future__ import annotations

from typing import Literal, TypeAlias

import numpy as np
import numpy.typing as npt

Unit: TypeAlias = str
"""A single segmented unit of text: a character, token, or sentence."""

UnitKind: TypeAlias = Literal["chars", "tokens", "sentences"]
"""Which kind of unit a segmenter emits."""

FloatArray: TypeAlias = npt.NDArray[np.float64]
"""A 1-D array of floats: a per-unit scalar channel (e.g. ``size``)."""

Coords: TypeAlias = npt.NDArray[np.float64]
"""An ``(N, 2)`` or ``(N, 3)`` array of layout coordinates, one row per unit."""
