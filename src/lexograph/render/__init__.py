"""Render: draw a laid-out, encoded text as a matplotlib Figure."""

from lexograph.render.mpl import frame_axes, render_path, render_points
from lexograph.render.mpl3d import render_path_3d

__all__ = ["render_points", "render_path", "render_path_3d", "frame_axes"]
