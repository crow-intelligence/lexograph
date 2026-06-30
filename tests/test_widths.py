import string as _string

import numpy as np
from hypothesis import given, settings
from hypothesis import strategies as st

from lexograph.layout.widths import rendered_widths

# Printable ASCII keeps TextPath layout fast and deterministic across platforms.
printable_text = st.text(alphabet=_string.printable, min_size=0, max_size=20)


class TestRenderedWidths:
    """Rendered width grows with content and is deterministic per font/size."""

    def test_wider_string_is_wider(self) -> None:
        widths = rendered_widths(["i", "wwwwww"])
        assert widths[1] > widths[0]

    def test_one_per_string(self) -> None:
        strings = ["alpha", "beta", "gamma"]
        assert rendered_widths(strings).shape == (len(strings),)

    def test_size_scales_width(self) -> None:
        small = rendered_widths(["hello"], size=8.0)[0]
        large = rendered_widths(["hello"], size=24.0)[0]
        assert large > small

    def test_whitespace_still_advances(self) -> None:
        assert rendered_widths(["   "])[0] > 0.0

    def test_deterministic(self) -> None:
        a = rendered_widths(["The quick brown fox."])
        b = rendered_widths(["The quick brown fox."])
        assert np.array_equal(a, b)

    @settings(max_examples=40, deadline=None)
    @given(st.lists(printable_text, min_size=1, max_size=12))
    def test_all_finite_and_non_negative(self, strings: list[str]) -> None:
        widths = rendered_widths(strings)
        assert np.all(np.isfinite(widths))
        assert np.all(widths >= 0.0)
