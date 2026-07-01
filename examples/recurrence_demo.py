"""Recurrence-dotplot demo: a chapter plotted against itself.

Run with:  uv run python examples/recurrence_demo.py
Writes recurrence.png to the current directory.
"""

from lexograph import load_demo_text, recurrence_plot


def main() -> None:
    """Draw the sentence x sentence self-similarity grid of the bundled chapter."""
    fig = recurrence_plot(load_demo_text(), threshold=0.7)
    fig.savefig("recurrence.png", dpi=150)
    print("Saved recurrence.png")


if __name__ == "__main__":
    main()
