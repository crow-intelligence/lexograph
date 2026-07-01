import numpy as np
import pytest
from matplotlib.figure import Figure

from lexograph.encode import Channels, categorical_colors, normalize_size
from lexograph.render import render_path, render_points


class TestRenderPoints:
    """render_points draws one mark or glyph per unit and returns a Figure."""

    def test_returns_figure_with_one_axes(self) -> None:
        fig = render_points(np.array([[0.0, 0.0], [1.0, 1.0]]))
        assert isinstance(fig, Figure)
        assert len(fig.axes) == 1

    def test_accepts_channels(self) -> None:
        coords = np.array([[0.0, 0.0], [1.0, 0.0], [2.0, 0.0]])
        channels = Channels(
            sizes=normalize_size([1, 2, 3]),
            colors=categorical_colors([0, 1, 0]),
        )
        fig = render_points(coords, channels=channels)
        assert isinstance(fig, Figure)

    def test_glyphs_render_as_text(self) -> None:
        coords = np.array([[0.0, 0.0], [1.0, 0.0]])
        fig = render_points(coords, glyphs=["a", "b"])
        assert len(fig.axes[0].texts) == 2

    def test_empty(self) -> None:
        fig = render_points(np.zeros((0, 2)))
        assert isinstance(fig, Figure)

    def test_bad_shape_raises(self) -> None:
        with pytest.raises(ValueError, match=r"shape \(N, 2\)"):
            render_points(np.zeros((3, 3)))

    def test_channel_length_mismatch_raises(self) -> None:
        with pytest.raises(ValueError, match="one entry per unit"):
            render_points(np.zeros((2, 2)), glyphs=["only-one"])


class TestRenderPath:
    """render_path joins the units into a connected (optionally coloured) path."""

    def test_returns_figure(self) -> None:
        fig = render_path(np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]]))
        assert isinstance(fig, Figure)

    def test_per_segment_colors(self) -> None:
        coords = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]])
        colors = categorical_colors([0, 1])  # N-1 == 2 segments
        fig = render_path(coords, colors=colors)
        assert len(fig.axes[0].collections) == 1

    def test_wrong_color_count_raises(self) -> None:
        coords = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]])
        with pytest.raises(ValueError, match="length N-1"):
            render_path(coords, colors=categorical_colors([0, 1, 2]))
