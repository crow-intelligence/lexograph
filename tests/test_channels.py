import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st

from lexograph.encode import (
    categorical_colors,
    continuous_colors,
    normalize_size,
)


class TestNormalizeSize:
    """Sizes are min-max normalised, shaped, and scaled into [lo, hi]."""

    def test_endpoints_map_to_range(self) -> None:
        sizes = normalize_size([0, 10], lo=2.0, hi=8.0)
        assert sizes.tolist() == [2.0, 8.0]

    def test_constant_input_maps_to_lo(self) -> None:
        sizes = normalize_size([5, 5, 5], lo=3.0, hi=9.0)
        assert sizes.tolist() == [3.0, 3.0, 3.0]

    def test_empty(self) -> None:
        assert normalize_size([]).tolist() == []

    def test_bad_range_raises(self) -> None:
        with pytest.raises(ValueError, match="must be >= lo"):
            normalize_size([1, 2], lo=5.0, hi=1.0)

    def test_bad_power_raises(self) -> None:
        with pytest.raises(ValueError, match="power must be positive"):
            normalize_size([1, 2], power=0.0)

    @given(
        st.lists(st.floats(min_value=-1e6, max_value=1e6), min_size=1, max_size=50),
        st.floats(min_value=0.0, max_value=10.0),
        st.floats(min_value=0.0, max_value=10.0),
    )
    def test_stays_within_bounds(self, values: list[float], a: float, b: float) -> None:
        lo, hi = min(a, b), max(a, b)
        sizes = normalize_size(values, lo=lo, hi=hi)
        assert np.all(sizes >= lo - 1e-9)
        assert np.all(sizes <= hi + 1e-9)


class TestCategoricalColors:
    """Labels colour by first appearance: same label, same colour."""

    def test_same_label_same_color(self) -> None:
        colors = categorical_colors([0, 1, 0, 2])
        assert colors[0] == colors[2]
        assert colors[0] != colors[1]

    def test_one_per_label(self) -> None:
        labels = ["a", "b", "c", "a"]
        assert len(categorical_colors(labels)) == len(labels)

    def test_many_categories_use_hsv(self) -> None:
        colors = categorical_colors(list(range(30)))
        assert len(colors) == 30
        assert len(set(colors)) == 30


class TestContinuousColors:
    """Numeric values map through a continuous colormap."""

    def test_one_per_value(self) -> None:
        assert len(continuous_colors([0.0, 0.5, 1.0])) == 3

    def test_constant_input_uses_midpoint(self) -> None:
        colors = continuous_colors([2.0, 2.0])
        assert colors[0] == colors[1]

    def test_empty(self) -> None:
        assert continuous_colors([]) == []
