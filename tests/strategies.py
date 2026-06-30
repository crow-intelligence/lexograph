"""Shared Hypothesis strategies for lexograph tests."""

from __future__ import annotations

import string

from hypothesis import strategies as st

word = st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=12)
"""A lowercase alphabetic word type (1-12 chars)."""

unit_length = st.integers(min_value=1, max_value=400)
"""A per-unit step length (e.g. a sentence's character count)."""
