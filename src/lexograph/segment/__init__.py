"""Segmentation: turn raw text into ordered units (chars, tokens, sentences)."""

from lexograph.segment.units import characters, segment, sentences, tokens

__all__ = ["segment", "characters", "tokens", "sentences"]
