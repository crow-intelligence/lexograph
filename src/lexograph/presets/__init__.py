"""Presets: ready-made points on the segment-layout-encode-render spine."""

from lexograph.presets.concordance import concordance
from lexograph.presets.punctuation_spiral import is_accent, punctuation_spiral
from lexograph.presets.recurrence import recurrence_plot
from lexograph.presets.text_walk import text_walk

__all__ = [
    "punctuation_spiral",
    "is_accent",
    "text_walk",
    "recurrence_plot",
    "concordance",
]
