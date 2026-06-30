"""Cross-cutting geometry properties of the layouts.

These property tests pin the invariants the layouts promise — the turn angle, the
turtle's perpendicularity, and the consistency of the 2-D and 3-D walks — beyond
the per-module unit tests.
"""

import numpy as np
from hypothesis import given
from hypothesis import strategies as st

from lexograph.layout.spiral import spiral_layout
from lexograph.layout.walk import walk_layout
from lexograph.layout.walk3d import walk3d_layout

positive_steps = st.lists(
    st.floats(min_value=0.1, max_value=1e3, allow_nan=False, allow_infinity=False),
    min_size=2,
    max_size=60,
)
turn_angles = st.floats(min_value=10.0, max_value=170.0, allow_nan=False)


def _signed_angles(coords: np.ndarray) -> np.ndarray:
    """Signed turn (degrees) between each pair of consecutive path segments."""
    directions = np.diff(coords, axis=0)
    units = directions / np.linalg.norm(directions, axis=1, keepdims=True)
    cross = units[:-1, 0] * units[1:, 1] - units[:-1, 1] * units[1:, 0]
    dot = np.sum(units[:-1] * units[1:], axis=1)
    return np.degrees(np.arctan2(cross, dot))


class TestWalkTurnInvariant:
    """Every step turns the heading by exactly the requested angle."""

    @given(positive_steps, turn_angles)
    def test_consecutive_segments_turn_by_turn(
        self, steps: list[float], turn: float
    ) -> None:
        coords = walk_layout(steps, turn=turn)
        angles = _signed_angles(coords)
        assert np.allclose(angles, turn, atol=1e-6)

    @given(positive_steps)
    def test_right_angle_walk_segments_are_perpendicular(
        self, steps: list[float]
    ) -> None:
        coords = walk_layout(steps, turn=-90.0)
        directions = np.diff(coords, axis=0)
        dots = np.sum(directions[:-1] * directions[1:], axis=1)
        assert np.allclose(dots, 0.0, atol=1e-6)


class TestWalkConsistency:
    """The 3-D corkscrew's projection is exactly the 2-D walk."""

    @given(positive_steps, st.floats(min_value=0.1, max_value=20.0))
    def test_xy_projection_matches_2d(self, steps: list[float], z_step: float) -> None:
        flat = walk_layout(steps)
        helix = walk3d_layout(steps, z_step=z_step)
        assert np.allclose(helix[:, :2], flat)
        assert np.allclose(np.diff(helix[:, 2]), z_step)


class TestSpiralMonotonicity:
    """The spiral winds strictly outward with near-uniform arc spacing."""

    @given(st.integers(min_value=3, max_value=200))
    def test_radius_strictly_increases(self, n: int) -> None:
        coords = spiral_layout(n, turns=5.0, r0=1.0, r_max=12.0)
        radii = np.hypot(coords[:, 0], coords[:, 1])
        assert np.all(np.diff(radii) > 0)
