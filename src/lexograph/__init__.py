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

__all__ = [
    "load_demo_text",
    "__version__",
]
