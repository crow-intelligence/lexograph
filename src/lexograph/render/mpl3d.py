"""Render a 3-D layout (the corkscrew walk) as a matplotlib ``Figure``.

Matplotlib's ``mplot3d`` toolkit draws the path as a 3-D line collection. As in
the 2-D renderer, the figure is built directly (no ``pyplot``) and never shown,
so it displays inline in Jupyter and saves with ``fig.savefig(...)``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.art3d import Line3DCollection

if TYPE_CHECKING:
    from collections.abc import Sequence

    from lexograph._types import Coords
    from lexograph.encode.channels import RGBA

__all__ = ["render_path_3d"]

_DEFAULT_LINE_COLOR = "#333333"


def _coords_3d(coords: Coords) -> np.ndarray:
    """Validate and return a 3-D ``(N, 3)`` float coordinate array."""
    array = np.asarray(coords, dtype=float)
    if array.ndim != 2 or array.shape[1] != 3:
        msg = f"coords must have shape (N, 3), got {array.shape}"
        raise ValueError(msg)
    return array


def render_path_3d(
    coords: Coords,
    *,
    colors: list[RGBA] | None = None,
    color: str = _DEFAULT_LINE_COLOR,
    linewidth: float = 1.5,
    linewidths: Sequence[float] | None = None,
    background: str = "white",
    figsize: tuple[float, float] = (8.0, 10.0),
    elev: float = 18.0,
    azim: float = -60.0,
    axes_off: bool = True,
) -> Figure:
    """Draw a 3-D path through the layout coordinates as a corkscrew.

    Args:
        coords: An ``(N, 3)`` array of vertices in path order.
        colors: Per-segment RGBA colours (length ``N - 1``). ``None`` draws a
            single-colour path.
        color: The path colour when ``colors`` is ``None``.
        linewidth: Line width in points, used when ``linewidths`` is ``None``.
        linewidths: Per-segment line widths (length ``N - 1``); overrides
            ``linewidth`` so the size channel can vary the stroke.
        background: Figure and axes background colour.
        figsize: Figure size in inches.
        elev: Camera elevation angle in degrees.
        azim: Camera azimuth angle in degrees.
        axes_off: Hide the 3-D axes, panes, and ticks for a clean plate.

    Returns:
        A :class:`matplotlib.figure.Figure` with one 3-D axes. Never calls
        ``show()``.

    Raises:
        ValueError: If ``coords`` is not ``(N, 3)`` or ``colors`` has the wrong
            length.

    Contract:
        - Returns a Figure with exactly one axes.
        - Inputs are never mutated.

    Examples:
        >>> import numpy as np
        >>> coords = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 1.0], [1.0, 1.0, 2.0]])
        >>> fig = render_path_3d(coords)
        >>> type(fig).__name__
        'Figure'
    """
    array = _coords_3d(coords)
    n = array.shape[0]

    fig = Figure(figsize=figsize, facecolor=background)
    # Axes3D exposes 3-D-only methods (view_init, set_zlim, add_collection3d)
    # that the 2-D-focused matplotlib stubs do not model; treat it as ``Any``.
    ax: Any = fig.add_subplot(projection="3d")
    ax.set_facecolor(background)

    if n >= 2:
        segments = list(np.stack([array[:-1], array[1:]], axis=1))
        seg_colors = colors if colors is not None else [color] * (n - 1)
        if len(seg_colors) != n - 1:
            msg = f"colors must have length N-1 ({n - 1}), got {len(seg_colors)}"
            raise ValueError(msg)
        widths: float | list[float] = linewidth
        if linewidths is not None:
            if len(linewidths) != n - 1:
                msg = (
                    f"linewidths must have length N-1 ({n - 1}), got {len(linewidths)}"
                )
                raise ValueError(msg)
            widths = [float(w) for w in linewidths]
        ax.add_collection3d(
            Line3DCollection(segments, colors=seg_colors, linewidths=widths)
        )

    _frame_3d(ax, array, elev=elev, azim=azim, axes_off=axes_off)
    return fig


def _frame_3d(
    ax: Any,  # noqa: ANN401  # an mplot3d Axes3D, untyped by the 2-D-focused stubs
    array: np.ndarray,
    *,
    elev: float,
    azim: float,
    axes_off: bool,
) -> None:
    """Fit the 3-D axes to the data, set the camera, and tidy the frame."""
    ax.view_init(elev=elev, azim=azim)
    if array.shape[0]:
        mins = array.min(axis=0)
        maxs = array.max(axis=0)
        spans = np.where(maxs > mins, maxs - mins, 1.0)
        ax.set_xlim(mins[0], mins[0] + spans[0])
        ax.set_ylim(mins[1], mins[1] + spans[1])
        ax.set_zlim(mins[2], mins[2] + spans[2])
        # Keep the corkscrew's true proportions (it is usually tall in z).
        ax.set_box_aspect(tuple(float(s) for s in spans))
    if axes_off:
        ax.set_axis_off()
