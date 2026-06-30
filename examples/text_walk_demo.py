"""Text-walk demo: a chapter as a space-filling turtle walk over its sentences.

Run with:  uv run python examples/text_walk_demo.py
Writes text_walk.png to the current directory.
"""

from lexograph import load_demo_text, segment, text_walk


def main() -> None:
    """Walk the bundled chapter, colouring each step by its position in the text."""
    text = load_demo_text()
    units = segment(text, unit="sentences")
    print(f"Walking {len(units)} sentences.")

    # Colour each sentence by where it falls in the chapter (continuous), and let
    # the default size channel weight each stroke by sentence length.
    fig = text_walk(text, colour=list(range(len(units))), figsize=(10.0, 10.0))
    fig.savefig("text_walk.png", dpi=150)
    print("Saved text_walk.png")


if __name__ == "__main__":
    main()
