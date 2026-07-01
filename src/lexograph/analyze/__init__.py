"""Optional analysis layer: turn a text into per-sentence channel arrays.

Behind the ``lexograph[graph]`` extra. It runs the Wittgenstein pipeline —
sentence embeddings → cosine kNN graph → (optional disparity backbone) → PageRank
and community detection — and hands back plain arrays that satisfy the
``encode`` data contract: a ``size`` array (PageRank centrality), a ``community``
array (colour labels), and a cosine ``distances`` matrix (for a semantic
recurrence dotplot). The core never imports this; the arrow points inward.

The core dependency-free scalars (length, position, frequency) live in
:mod:`lexograph.scalars`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from lexograph.analyze.backbone import extract_backbone
from lexograph.analyze.embeddings import embed_sentences
from lexograph.analyze.graph import (
    community_labels,
    embedding_distances,
    knn_graph,
    pagerank_scores,
)
from lexograph.segment.units import sentences as split_sentences

if TYPE_CHECKING:
    import numpy as np

    from lexograph._types import FloatArray
    from lexograph.analyze.graph import CommunityMethod

__all__ = [
    "Analysis",
    "analyze_text",
    "embed_sentences",
    "knn_graph",
    "embedding_distances",
    "pagerank_scores",
    "community_labels",
    "extract_backbone",
]


@dataclass(frozen=True, slots=True)
class Analysis:
    """The per-sentence channel arrays derived from a text.

    Attributes:
        sentences: The segmented sentences (length ``N``).
        embeddings: The ``(N, D)`` sentence embeddings.
        size: PageRank centrality per sentence — the size channel.
        community: Community id per sentence — the colour channel.
        distances: The ``(N, N)`` cosine distance matrix — pass it to
            ``recurrence_plot(distances=...)`` for a semantic dotplot.
    """

    sentences: list[str]
    embeddings: FloatArray
    size: FloatArray
    community: np.ndarray
    distances: FloatArray


def analyze_text(
    text: str,
    *,
    embeddings: FloatArray | None = None,
    k: int = 5,
    community: CommunityMethod = "louvain",
    n_clusters: int = 10,
    backbone: bool = False,
    min_alpha_ptile: float = 0.5,
    seed: int = 42,
) -> Analysis:
    """Run the analysis pipeline and return per-sentence channel arrays.

    Args:
        text: The source text.
        embeddings: Precomputed ``(N, D)`` embeddings to use. If ``None``, the
            sentences are embedded with the default model (a model download).
        k: Neighbours per node in the kNN graph.
        community: Community method — ``"louvain"`` (default) or ``"kmeans"``.
        n_clusters: Number of clusters for the ``"kmeans"`` method.
        backbone: If ``True``, sparsify the kNN graph with the disparity filter
            before PageRank and community detection.
        min_alpha_ptile: Disparity-filter threshold (used when ``backbone``).
        seed: Random seed for reproducibility.

    Returns:
        An :class:`Analysis` whose arrays align to the segmented sentences.

    Raises:
        ValueError: If ``embeddings`` is given but its length does not match the
            sentence count.

    Example:
        Drive a walk and a semantic dotplot from the analysis (not run as a
        doctest — embedding downloads a model)::

            from lexograph import text_walk, recurrence_plot, load_demo_text
            from lexograph.analyze import analyze_text

            a = analyze_text(load_demo_text())
            walk = text_walk(load_demo_text(), colour=a.community,
                             colour_kind="categorical", size=a.size)
            dots = recurrence_plot(load_demo_text(), distances=a.distances,
                                   threshold=0.4)
    """
    units = split_sentences(text)
    n = len(units)
    if embeddings is None:
        embeddings = embed_sentences(units)
    elif len(embeddings) != n:
        msg = f"embeddings must have one row per sentence ({n}), got {len(embeddings)}"
        raise ValueError(msg)

    graph = knn_graph(embeddings, k=k)
    if backbone:
        graph = extract_backbone(graph, min_alpha_ptile=min_alpha_ptile)
    size = pagerank_scores(graph, n)
    labels = community_labels(
        graph,
        n,
        method=community,
        embeddings=embeddings,
        n_clusters=n_clusters,
        seed=seed,
    )
    distances = embedding_distances(embeddings)
    return Analysis(
        sentences=units,
        embeddings=embeddings,
        size=size,
        community=labels,
        distances=distances,
    )
