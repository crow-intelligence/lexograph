"""The turtle-walk layout: step forward by a per-unit length, then turn.

This is the 2-D walk math ported from the Wittgenstein piece's ``compute_path``
(itself the descendant of the original turtle POC), reduced to plain coordinate
generation. For each unit the turtle steps forward along its heading by that
unit's step length, then rotates by a fixed turn angle (90° to the right by
default — the space-filling rectangular walk). The renderer is rebuilt in
matplotlib; this module only produces coordinates.

The returned array has one more row than there are steps: it starts at the
origin and appends a vertex after each step, so ``N`` units yield ``N + 1``
vertices and ``N`` segments. Segment ``i`` belongs to unit ``i``, which keeps a
per-unit colour channel aligned with the path drawn by
:func:`lexograph.render.mpl.render_path`.
"""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from lexograph._types import Coords, FloatArray

__all__ = ["walk_layout", "heading_angles"]


def _rotation(degrees: float) -> np.ndarray:
    """Return the 2x2 matrix that rotates a column vector counter-clockwise."""
    theta = np.deg2rad(degrees)
    cos, sin = np.cos(theta), np.sin(theta)
    return np.array([[cos, -sin], [sin, cos]])


def walk_layout(
    steps: Iterable[float],
    *,
    turn: float = -90.0,
    scale: float = 1.0,
    start: tuple[float, float] = (0.0, 0.0),
    heading: tuple[float, float] = (1.0, 0.0),
) -> Coords:
    """Walk a turtle forward by each step length, turning by ``turn`` between steps.

    Args:
        steps: One forward step length per unit (e.g. sentence length or rendered
            width). Negative steps are allowed (the turtle walks backward).
        turn: Degrees to rotate the heading after each step. The default ``-90``
            turns right, giving the space-filling rectangular walk; ``+90`` turns
            left. Non-right angles produce curved or spiralling paths.
        scale: A multiplier applied to every step length.
        start: The starting ``(x, y)`` position (the first vertex).
        heading: The initial heading vector; it is normalised internally.

    Returns:
        An ``(N + 1, 2)`` float array of vertices, where ``N`` is the number of
        steps. Row 0 is ``start``; row ``i + 1`` is the position after step ``i``.

    Raises:
        ValueError: If ``heading`` is the zero vector.

    Contract:
        - The result has exactly ``N + 1`` rows for ``N`` steps.
        - The distance between consecutive vertices equals ``abs(step * scale)``
          for that unit (up to floating-point error).
        - The output is deterministic in its inputs.

    Examples:
        >>> walk_layout([1.0, 1.0, 1.0]).round(6).tolist()
        [[0.0, 0.0], [1.0, 0.0], [1.0, -1.0], [0.0, -1.0]]
    """
    lengths = np.asarray(list(steps), dtype=float)
    head = np.asarray(heading, dtype=float)
    norm = float(np.hypot(head[0], head[1]))
    if norm == 0.0:
        msg = "heading must be a non-zero vector"
        raise ValueError(msg)
    head = head / norm
    rotation = _rotation(turn)

    pos = np.asarray(start, dtype=float)
    vertices = [pos.copy()]
    for length in lengths:
        pos = pos + head * (length * scale)
        vertices.append(pos.copy())
        head = rotation @ head
    return np.asarray(vertices)


def heading_angles(
    steps: Iterable[float],
    *,
    turn: float = -90.0,
    heading: tuple[float, float] = (1.0, 0.0),
) -> FloatArray:
    """Return the heading angle (degrees) the turtle travels along for each step.

    Useful for orienting per-unit glyphs along the walk (calligraphy-on-path):
    angle ``i`` is the direction of the segment drawn for unit ``i``.

    Args:
        steps: One step per unit; only the count is used.
        turn: Degrees rotated after each step (see :func:`walk_layout`).
        heading: The initial heading vector; normalised internally.

    Returns:
        A length-``N`` array of angles in degrees in ``[-180, 180]``.

    Examples:
        >>> heading_angles([1, 1, 1]).tolist()
        [0.0, -90.0, -180.0]
    """
    n = len(list(steps))
    head = np.asarray(heading, dtype=float)
    head = head / float(np.hypot(head[0], head[1]))
    rotation = _rotation(turn)
    angles = []
    for _ in range(n):
        angles.append(float(np.round(np.degrees(np.arctan2(head[1], head[0])), 6)))
        head = rotation @ head
    return np.asarray(angles, dtype=float)
