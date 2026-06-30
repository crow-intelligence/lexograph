"""lexograph — spatialize linear text into pictures you can read.

lexograph turns a linear text into a picture through one four-step spine:
**segment** the text into ordered units (characters, tokens, or sentences),
**lay them out** in 2-D or 3-D space, **encode** per-unit attributes onto
visual channels (size, colour, glyph), and **render** the result as a
matplotlib :class:`~matplotlib.figure.Figure` that displays inline in Jupyter
and saves cleanly with ``fig.savefig(...)``.
"""

__version__ = "0.1.0"

from lexograph.datasets import load_demo_text
from lexograph.encode import (
    Channels,
    categorical_colors,
    continuous_colors,
    normalize_size,
)
from lexograph.layout import (
    linear_layout,
    rendered_widths,
    spiral_layout,
    walk3d_layout,
    walk_layout,
)
from lexograph.presets import punctuation_spiral, text_walk
from lexograph.render import frame_axes, render_path, render_path_3d, render_points
from lexograph.segment import segment

__all__ = [
    "segment",
    "linear_layout",
    "walk_layout",
    "walk3d_layout",
    "spiral_layout",
    "rendered_widths",
    "normalize_size",
    "categorical_colors",
    "continuous_colors",
    "Channels",
    "render_points",
    "render_path",
    "render_path_3d",
    "frame_axes",
    "punctuation_spiral",
    "text_walk",
    "load_demo_text",
    "__version__",
]
