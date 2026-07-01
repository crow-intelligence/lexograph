"""End-to-end: segment -> layout -> encode -> render on the bundled text."""

import numpy as np
from matplotlib.figure import Figure

from lexograph import (
    Channels,
    categorical_colors,
    linear_layout,
    normalize_size,
    render_points,
    segment,
)


class TestSpineEndToEnd:
    """The four steps compose into a Figure from real text."""

    def test_demo_text_to_figure(self, demo_text: str) -> None:
        units = segment(demo_text, unit="sentences")
        assert len(units) > 20

        coords = linear_layout(len(units), columns=8)
        channels = Channels(
            sizes=normalize_size([len(u) for u in units], lo=4.0, hi=20.0),
            colors=categorical_colors([i % 4 for i in range(len(units))]),
        )
        fig = render_points(coords, channels=channels)

        assert isinstance(fig, Figure)
        assert coords.shape == (len(units), 2)
        assert len(channels.sizes) == len(units)

    def test_lengths_stay_aligned(self, demo_text: str) -> None:
        units = segment(demo_text, unit="tokens")
        sizes = normalize_size([len(u) for u in units])
        coords = linear_layout(len(units))
        assert len(units) == len(sizes) == coords.shape[0]
        assert np.all(sizes >= 6.0 - 1e-9)
