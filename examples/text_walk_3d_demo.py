"""3-D text-walk demo: the chapter lifted into a corkscrew.

Run with:  uv run python examples/text_walk_3d_demo.py
Writes text_walk_3d.png to the current directory.
"""

from lexograph import load_demo_text, segment, text_walk


def main() -> None:
    """Walk the bundled chapter as a 3-D corkscrew, coloured by position."""
    text = load_demo_text()
    units = segment(text, unit="sentences")
    print(f"Winding {len(units)} sentences into a corkscrew.")

    fig = text_walk(
        text,
        colour=list(range(len(units))),
        helix=True,
        z_step=4.0,
    )
    fig.savefig("text_walk_3d.png", dpi=150)
    print("Saved text_walk_3d.png")


if __name__ == "__main__":
    main()
