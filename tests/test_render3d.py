import numpy as np
import pytest
from matplotlib.figure import Figure

from lexograph.encode import categorical_colors
from lexograph.layout.walk3d import walk3d_layout
from lexograph.render.mpl3d import render_path_3d


class TestRenderPath3D:
    """render_path_3d draws the corkscrew and returns a 3-D Figure."""

    def test_returns_figure(self) -> None:
        coords = walk3d_layout([1.0, 2.0, 1.5, 3.0])
        fig = render_path_3d(coords)
        assert isinstance(fig, Figure)
        assert len(fig.axes) == 1

    def test_per_segment_colours(self) -> None:
        coords = walk3d_layout([1.0, 2.0, 1.5])  # 4 vertices, 3 segments
        colours = categorical_colors([0, 1, 0])
        fig = render_path_3d(coords, colors=colours)
        assert isinstance(fig, Figure)

    def test_per_segment_linewidths(self) -> None:
        coords = walk3d_layout([1.0, 2.0, 1.5])
        fig = render_path_3d(coords, linewidths=[1.0, 2.0, 3.0])
        assert isinstance(fig, Figure)

    def test_bad_shape_raises(self) -> None:
        with pytest.raises(ValueError, match=r"shape \(N, 3\)"):
            render_path_3d(np.zeros((3, 2)))

    def test_wrong_colour_count_raises(self) -> None:
        coords = walk3d_layout([1.0, 2.0, 1.5])
        with pytest.raises(ValueError, match="length N-1"):
            render_path_3d(coords, colors=categorical_colors([0, 1]))

    def test_wrong_linewidth_count_raises(self) -> None:
        coords = walk3d_layout([1.0, 2.0, 1.5])
        with pytest.raises(ValueError, match="linewidths must have length"):
            render_path_3d(coords, linewidths=[1.0, 2.0])
