"""Spine demo: segment -> layout -> encode -> render on the bundled text.

Run with:  uv run python examples/spine_demo.py
Writes spine_demo.png to the current directory.
"""

from lexograph import (
    Channels,
    categorical_colors,
    linear_layout,
    normalize_size,
    render_points,
    segment,
)
from lexograph.datasets import load_demo_text


def main() -> None:
    """Lay Pride and Prejudice's first chapter out as a field of sentence tiles."""
    text = load_demo_text()
    units = segment(text, unit="sentences")
    print(f"Segmented {len(units)} sentences.")

    coords = linear_layout(len(units), columns=8)
    channels = Channels(
        # Size each tile by sentence length; colour by position in the chapter.
        sizes=normalize_size([len(u) for u in units], lo=6.0, hi=26.0, power=1.5),
        colors=categorical_colors([i // 8 for i in range(len(units))]),
    )

    fig = render_points(coords, channels=channels, figsize=(9.0, 9.0))
    fig.savefig("spine_demo.png", dpi=120)
    print("Saved spine_demo.png")


if __name__ == "__main__":
    main()
