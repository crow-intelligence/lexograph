import numpy as np
from hypothesis import given
from hypothesis import strategies as st

from lexograph.layout.walk import walk_layout
from lexograph.layout.walk3d import walk3d_layout

step_lists = st.lists(
    st.floats(min_value=0.0, max_value=1e3, allow_nan=False, allow_infinity=False),
    min_size=1,
    max_size=60,
)


class TestWalk3DLayout:
    """The corkscrew is the 2-D walk with a constant lift in z."""

    def test_known_corkscrew(self) -> None:
        coords = walk3d_layout([1.0, 1.0], z_step=2.0).round(6)
        assert coords.tolist() == [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 2.0],
            [1.0, -1.0, 4.0],
        ]

    def test_returns_n_plus_one_vertices(self) -> None:
        assert walk3d_layout([1, 2, 3]).shape == (4, 3)

    @given(step_lists, st.floats(min_value=0.01, max_value=50.0))
    def test_z_increases_by_z_step(self, steps: list[float], z_step: float) -> None:
        coords = walk3d_layout(steps, z_step=z_step)
        dz = np.diff(coords[:, 2])
        assert np.allclose(dz, z_step)

    @given(step_lists)
    def test_xy_matches_2d_walk(self, steps: list[float]) -> None:
        flat = walk_layout(steps)
        helix = walk3d_layout(steps)
        assert np.allclose(helix[:, :2], flat)

    @given(step_lists)
    def test_deterministic(self, steps: list[float]) -> None:
        assert np.array_equal(walk3d_layout(steps), walk3d_layout(steps))
