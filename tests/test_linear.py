import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st

from lexograph.layout import linear_layout


class TestLinearLayout:
    """Units flow left-to-right, wrapping into downward rows."""

    def test_single_row(self) -> None:
        assert linear_layout(3).tolist() == [[0.0, 0.0], [1.0, 0.0], [2.0, 0.0]]

    def test_wraps_into_rows(self) -> None:
        coords = linear_layout(4, columns=2)
        assert coords.tolist() == [
            [0.0, 0.0],
            [1.0, 0.0],
            [0.0, -1.0],
            [1.0, -1.0],
        ]

    def test_empty(self) -> None:
        assert linear_layout(0).shape == (0, 2)

    def test_negative_raises(self) -> None:
        with pytest.raises(ValueError, match="non-negative"):
            linear_layout(-1)

    def test_bad_columns_raises(self) -> None:
        with pytest.raises(ValueError, match="columns must be positive"):
            linear_layout(3, columns=0)

    @given(
        st.integers(min_value=0, max_value=500), st.integers(min_value=1, max_value=40)
    )
    def test_shape_matches_n(self, n: int, columns: int) -> None:
        coords = linear_layout(n, columns=columns)
        assert coords.shape == (n, 2)
        if n:
            assert np.all(coords[:, 1] <= 0)
