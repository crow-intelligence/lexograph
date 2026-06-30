"""Punctuation-spiral demo: a text's marks wound onto an Archimedean spiral.

Run with:  uv run python examples/punctuation_spiral_demo.py
Writes punctuation_spiral.png to the current directory.
"""

from lexograph import load_demo_text, punctuation_spiral


def main() -> None:
    """Draw the punctuation of Pride and Prejudice's first chapter as a spiral."""
    fig = punctuation_spiral(load_demo_text(), turns=12.0)
    fig.savefig("punctuation_spiral.png", dpi=150)
    print("Saved punctuation_spiral.png")


if __name__ == "__main__":
    main()
