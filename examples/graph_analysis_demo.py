"""Graph-analysis demo: drive the walk and the dotplot from semantics.

Requires the optional extra:  uv add "lexograph[graph]"
Run with:  uv run python examples/graph_analysis_demo.py
Writes semantic_walk.png and semantic_recurrence.png. The first run downloads a
small sentence-transformers model.
"""

from lexograph import load_demo_text, recurrence_plot, text_walk
from lexograph.analyze import analyze_text


def main() -> None:
    """Embed the chapter, then colour a walk by community and size it by PageRank."""
    text = load_demo_text()
    analysis = analyze_text(text, community="louvain")
    print(f"Analysed {len(analysis.sentences)} sentences.")

    # PageRank centrality -> size; Louvain community -> colour.
    walk = text_walk(
        text,
        colour=analysis.community.tolist(),
        colour_kind="categorical",
        size=analysis.size.tolist(),
    )
    walk.savefig("semantic_walk.png", dpi=150)
    print("Saved semantic_walk.png")

    # Embedding cosine distance -> a semantic recurrence dotplot.
    dots = recurrence_plot(text, distances=analysis.distances, threshold=0.35)
    dots.savefig("semantic_recurrence.png", dpi=150)
    print("Saved semantic_recurrence.png")


if __name__ == "__main__":
    main()
