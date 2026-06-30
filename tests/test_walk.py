import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st

from lexograph.layout.walk import heading_angles, walk_layout

step_lists = st.lists(
    st.floats(min_value=0.0, max_value=1e3, allow_nan=False, allow_infinity=False),
    min_size=1,
    max_size=80,
)


class TestWalkLayout:
    """The turtle steps forward then turns; geometry is exact and deterministic."""

    def test_unit_square(self) -> None:
        coords = walk_layout([1.0, 1.0, 1.0]).round(6)
        assert coords.tolist() == [
            [0.0, 0.0],
            [1.0, 0.0],
            [1.0, -1.0],
            [0.0, -1.0],
        ]

    def test_returns_n_plus_one_vertices(self) -> None:
        assert walk_layout([1, 2, 3, 4]).shape == (5, 2)

    def test_left_turn_mirrors_right(self) -> None:
        right = walk_layout([1, 1, 1], turn=-90.0)
        left = walk_layout([1, 1, 1], turn=90.0)
        # Left turn is the right turn reflected across the x-axis.
        assert np.allclose(right[:, 1], -left[:, 1])

    def test_zero_heading_raises(self) -> None:
        with pytest.raises(ValueError, match="non-zero"):
            walk_layout([1, 2], heading=(0.0, 0.0))

    @given(step_lists)
    def test_segment_lengths_match_steps(self, steps: list[float]) -> None:
        coords = walk_layout(steps, scale=1.0)
        seg = np.hypot(np.diff(coords[:, 0]), np.diff(coords[:, 1]))
        assert np.allclose(seg, np.abs(steps), atol=1e-6)

    @given(step_lists)
    def test_deterministic(self, steps: list[float]) -> None:
        assert np.array_equal(walk_layout(steps), walk_layout(steps))

    @given(step_lists)
    def test_bounded_box(self, steps: list[float]) -> None:
        coords = walk_layout(steps)
        reach = float(np.sum(np.abs(steps)))
        assert np.all(np.abs(coords) <= reach + 1e-6)


class TestHeadingAngles:
    """Heading rotates by the turn angle each step."""

    def test_right_turn_sequence(self) -> None:
        assert heading_angles([1, 1, 1]).tolist() == [0.0, -90.0, -180.0]

    @given(step_lists)
    def test_one_angle_per_step(self, steps: list[float]) -> None:
        assert heading_angles(steps).shape == (len(steps),)
