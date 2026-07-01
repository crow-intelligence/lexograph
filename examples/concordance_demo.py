"""Concordance demo: where the main characters fall across the chapter.

Run with:  uv run python examples/concordance_demo.py
Writes concordance.png to the current directory and prints KWIC for "Bingley".
"""

from lexograph import concordance, load_demo_text
from lexograph.layout.dispersion import kwic


def main() -> None:
    """Plot the dispersion of a few terms and print their keyword-in-context lines."""
    text = load_demo_text()
    fig = concordance(text, ["Bennet", "Bingley", "wife", "daughters", "fortune"])
    fig.savefig("concordance.png", dpi=150)
    print("Saved concordance.png")

    print('\nKWIC for "Bingley":')
    for line in kwic(text, "Bingley", width=4):
        print(f"  {line.left:>30}  [{line.keyword}]  {line.right}")


if __name__ == "__main__":
    main()
