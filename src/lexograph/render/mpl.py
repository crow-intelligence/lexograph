"""Render laid-out, encoded units as a matplotlib ``Figure``.

This is the final step of the spine. It takes coordinates from a layout and
optional visual channels (sizes, colours, glyphs) and draws them. Following the
family convention, every entry point constructs a :class:`matplotlib.figure.Figure`
directly (no global ``pyplot`` state) and never calls ``show()``, so figures
render inline in Jupyter and save cleanly with ``fig.savefig(...)``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.figure import Figure

if TYPE_CHECKING:
    from matplotlib.axes import Axes

    from lexograph._types import Coords
    from lexograph.encode.channels import RGBA, Channels

__all__ = ["render_points", "render_path", "frame_axes"]

_DEFAULT_POINT_COLOR = "#1f77b4"
_DEFAULT_LINE_COLOR = "#333333"


def _coords_2d(coords: Coords) -> np.ndarray:
    """Validate and return a 2-D ``(N, 2)`` float coordinate array."""
    array = np.asarray(coords, dtype=float)
    if array.ndim != 2 or array.shape[1] != 2:
        msg = f"coords must have shape (N, 2), got {array.shape}"
        raise ValueError(msg)
    return array


def frame_axes(ax: Axes, coords: Coords, *, margin: float = 0.05) -> None:
    """Equalise the aspect ratio, hide the axes, and fit ``coords`` with a margin.

    A small helper shared by the renderers and presets: it makes an axes show a
    spatial figure (equal aspect, no ticks or spines) framed to the data.

    Args:
        ax: The axes to configure.
        coords: An ``(N, 2)`` array the limits are fitted to.
        margin: Fractional padding added around the data extent.

    Examples:
        >>> import numpy as np
        >>> from matplotlib.figure import Figure
        >>> ax = Figure().subplots()
        >>> frame_axes(ax, np.array([[0.0, 0.0], [1.0, 1.0]]))
        >>> ax.get_aspect()
        1.0
    """
    array = np.asarray(coords, dtype=float)
    ax.set_aspect("equal")
    ax.axis("off")
    if array.shape[0] == 0:
        return
    xmin, ymin = array.min(axis=0)
    xmax, ymax = array.max(axis=0)
    span_x = xmax - xmin or 1.0
    span_y = ymax - ymin or 1.0
    ax.set_xlim(xmin - margin * span_x, xmax + margin * span_x)
    ax.set_ylim(ymin - margin * span_y, ymax + margin * span_y)


def render_points(
    coords: Coords,
    *,
    channels: Channels | None = None,
    sizes: np.ndarray | None = None,
    colors: list[RGBA] | None = None,
    glyphs: list[str] | None = None,
    background: str = "white",
    figsize: tuple[float, float] = (8.0, 8.0),
) -> Figure:
    """Draw one mark per unit at its layout coordinate.

    If ``glyphs`` are given, each unit is drawn as text; otherwise each unit is a
    scatter marker. Channel arrays may be passed individually or bundled in a
    :class:`~lexograph.encode.channels.Channels`; individual arguments win.

    Args:
        coords: An ``(N, 2)`` array of unit positions.
        channels: Resolved channels to use as defaults for ``sizes``/``colors``/
            ``glyphs``.
        sizes: Per-unit size in points (marker diameter, or glyph font size).
        colors: Per-unit RGBA colour.
        glyphs: Per-unit text; when given, units are drawn as text not markers.
        background: Figure and axes background colour.
        figsize: Figure size in inches.

    Returns:
        A :class:`matplotlib.figure.Figure` with a single axes. Never calls
        ``show()``.

    Raises:
        ValueError: If ``coords`` is not ``(N, 2)``, or a channel length does
            not match the number of units.

    Contract:
        - Returns a Figure with exactly one axes.
        - Inputs are never mutated.

    Examples:
        >>> import numpy as np
        >>> fig = render_points(np.array([[0.0, 0.0], [1.0, 1.0]]))
        >>> type(fig).__name__
        'Figure'
        >>> len(fig.axes)
        1
    """
    array = _coords_2d(coords)
    n = array.shape[0]
    if channels is not None:
        sizes = sizes if sizes is not None else channels.sizes
        colors = colors if colors is not None else channels.colors
        glyphs = glyphs if glyphs is not None else channels.glyphs
    _check_lengths(n, sizes=sizes, colors=colors, glyphs=glyphs)

    fig = Figure(figsize=figsize, facecolor=background)
    ax = fig.subplots()
    ax.set_facecolor(background)

    if glyphs is not None:
        for i in range(n):
            ax.text(
                array[i, 0],
                array[i, 1],
                glyphs[i],
                fontsize=(float(sizes[i]) if sizes is not None else 12.0),
                color=(colors[i] if colors is not None else _DEFAULT_POINT_COLOR),
                ha="center",
                va="center",
            )
    elif n:
        marker_area = (
            (np.asarray(sizes, dtype=float) ** 2) if sizes is not None else 36.0
        )
        ax.scatter(
            array[:, 0],
            array[:, 1],
            s=marker_area,
            c=(colors if colors is not None else _DEFAULT_POINT_COLOR),
        )

    frame_axes(ax, array)
    fig.tight_layout()
    return fig


def render_path(
    coords: Coords,
    *,
    colors: list[RGBA] | None = None,
    color: str = _DEFAULT_LINE_COLOR,
    linewidth: float = 1.5,
    background: str = "white",
    figsize: tuple[float, float] = (8.0, 8.0),
) -> Figure:
    """Draw the units as a connected path through their layout coordinates.

    This is the renderer behind the text walk: consecutive units are joined by
    line segments. When ``colors`` is given (one colour per segment, i.e. one
    per unit after the first), the path is drawn as a multi-coloured
    :class:`~matplotlib.collections.LineCollection`.

    Args:
        coords: An ``(N, 2)`` array of vertices in path order.
        colors: Per-segment RGBA colours (length ``N - 1``). ``None`` draws a
            single-colour path.
        color: The path colour when ``colors`` is ``None``.
        linewidth: Line width in points.
        background: Figure and axes background colour.
        figsize: Figure size in inches.

    Returns:
        A :class:`matplotlib.figure.Figure` with a single axes. Never calls
        ``show()``.

    Raises:
        ValueError: If ``coords`` is not ``(N, 2)``, or ``colors`` has the wrong
            length.

    Contract:
        - Returns a Figure with exactly one axes.
        - Inputs are never mutated.

    Examples:
        >>> import numpy as np
        >>> fig = render_path(np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]]))
        >>> type(fig).__name__
        'Figure'
    """
    array = _coords_2d(coords)
    n = array.shape[0]
    fig = Figure(figsize=figsize, facecolor=background)
    ax = fig.subplots()
    ax.set_facecolor(background)

    if n >= 2:
        if colors is not None:
            if len(colors) != n - 1:
                msg = f"colors must have length N-1 ({n - 1}), got {len(colors)}"
                raise ValueError(msg)
            segments = list(np.stack([array[:-1], array[1:]], axis=1))
            ax.add_collection(
                LineCollection(segments, colors=colors, linewidths=linewidth)
            )
        else:
            ax.plot(array[:, 0], array[:, 1], color=color, linewidth=linewidth)

    frame_axes(ax, array)
    fig.tight_layout()
    return fig


def _check_lengths(
    n: int,
    *,
    sizes: np.ndarray | None,
    colors: list[RGBA] | None,
    glyphs: list[str] | None,
) -> None:
    """Raise if any provided channel does not have one entry per unit."""
    for name, channel in (("sizes", sizes), ("colors", colors), ("glyphs", glyphs)):
        if channel is not None and len(channel) != n:
            msg = f"{name} must have one entry per unit ({n}), got {len(channel)}"
            raise ValueError(msg)
