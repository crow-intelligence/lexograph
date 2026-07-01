"""Encode: map per-unit attributes onto visual channels (size, colour, glyph)."""

from lexograph.encode.channels import (
    RGBA,
    Channels,
    categorical_colors,
    continuous_colors,
    normalize_size,
)

__all__ = [
    "RGBA",
    "Channels",
    "normalize_size",
    "categorical_colors",
    "continuous_colors",
]
