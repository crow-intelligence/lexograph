import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st

from lexograph.layout.spiral import spiral_layout, tangent_angles


class TestSpiralLayout:
    """Units are spread by equal arc length along an outward Archimedean spiral."""

    def test_shape(self) -> None:
        assert spiral_layout(10).shape == (10, 2)

    def test_radius_increases(self) -> None:
        coords = spiral_layout(20, turns=3.0, r0=1.0, r_max=8.0)
        radii = np.hypot(coords[:, 0], coords[:, 1])
        assert np.all(np.diff(radii) > 0)

    def test_equal_arc_length_spacing(self) -> None:
        coords = spiral_layout(40, turns=4.0, r0=1.0, r_max=10.0)
        steps = np.hypot(np.diff(coords[:, 0]), np.diff(coords[:, 1]))
        # Equal-arc-length resampling keeps consecutive gaps near-uniform.
        assert steps.std() / steps.mean() < 0.05

    def test_empty(self) -> None:
        assert spiral_layout(0).shape == (0, 2)

    def test_negative_raises(self) -> None:
        with pytest.raises(ValueError, match="non-negative"):
            spiral_layout(-1)

    def test_bad_turns_raises(self) -> None:
        with pytest.raises(ValueError, match="turns must be positive"):
            spiral_layout(5, turns=0.0)

    def test_bad_radius_raises(self) -> None:
        with pytest.raises(ValueError, match="r_max"):
            spiral_layout(5, r0=10.0, r_max=1.0)

    @given(st.integers(min_value=1, max_value=300))
    def test_count_matches(self, n: int) -> None:
        assert spiral_layout(n).shape == (n, 2)


class TestTangentAngles:
    """Tangent angles follow the local direction of an ordered path."""

    def test_horizontal_path(self) -> None:
        coords = np.array([[0.0, 0.0], [1.0, 0.0], [2.0, 0.0]])
        assert tangent_angles(coords).tolist() == [0.0, 0.0, 0.0]

    def test_one_per_point(self) -> None:
        coords = spiral_layout(15)
        assert tangent_angles(coords).shape == (15,)

    def test_bad_shape_raises(self) -> None:
        with pytest.raises(ValueError, match=r"shape \(N, 2\)"):
            tangent_angles(np.zeros((3, 3)))
