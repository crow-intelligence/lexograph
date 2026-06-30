"""Tests for the optional [graph] analysis layer.

The whole pipeline is exercised with synthetic embeddings, so no model is
downloaded. The real ``embed_sentences`` call is only smoke-tested when
sentence-transformers is importable (skipped otherwise).
"""

import os

import numpy as np
import pytest

pytest.importorskip("sklearn")
pytest.importorskip("networkx")

from lexograph.analyze import analyze_text  # noqa: E402
from lexograph.analyze.backbone import edge_alpha, extract_backbone  # noqa: E402
from lexograph.analyze.graph import (  # noqa: E402
    community_labels,
    embedding_distances,
    knn_graph,
    pagerank_scores,
)


@pytest.fixture
def two_clusters() -> np.ndarray:
    """Six unit vectors in two well-separated cosine clusters."""
    rng = np.random.default_rng(0)
    base_a = np.array([1.0, 0.0, 0.0])
    base_b = np.array([0.0, 1.0, 0.0])
    rows = []
    for base in (base_a, base_b):
        for _ in range(3):
            v = base + 0.01 * rng.standard_normal(3)
            rows.append(v / np.linalg.norm(v))
    return np.asarray(rows)


class TestKnnGraph:
    """The kNN graph wires sentences to their nearest neighbours by cosine."""

    def test_nodes_cover_all_sentences(self, two_clusters: np.ndarray) -> None:
        g = knn_graph(two_clusters, k=2)
        assert g.number_of_nodes() == 6

    def test_weights_are_similarities(self, two_clusters: np.ndarray) -> None:
        g = knn_graph(two_clusters, k=2)
        assert g.number_of_edges() > 0
        assert all(0.0 < d["weight"] <= 1.0 for _, _, d in g.edges(data=True))

    def test_single_node_has_no_edges(self) -> None:
        g = knn_graph(np.array([[1.0, 0.0]]), k=3)
        assert g.number_of_nodes() == 1
        assert g.number_of_edges() == 0


class TestEmbeddingDistances:
    """Cosine distance matrix is square with a (near-)zero diagonal."""

    def test_shape_and_diagonal(self, two_clusters: np.ndarray) -> None:
        d = embedding_distances(two_clusters)
        assert d.shape == (6, 6)
        assert np.allclose(np.diag(d), 0.0, atol=1e-6)


class TestPagerank:
    """PageRank aligns to every sentence and sums to ~1 over present nodes."""

    def test_aligned_length(self, two_clusters: np.ndarray) -> None:
        g = knn_graph(two_clusters, k=2)
        scores = pagerank_scores(g, 6)
        assert scores.shape == (6,)
        assert scores.sum() == pytest.approx(1.0, abs=1e-6)

    def test_no_edges_is_zeros(self) -> None:
        g = knn_graph(np.array([[1.0, 0.0]]), k=1)
        assert pagerank_scores(g, 1).tolist() == [0.0]


class TestCommunities:
    """Both community methods label every sentence; clusters are recovered."""

    def test_louvain_separates_clusters(self, two_clusters: np.ndarray) -> None:
        g = knn_graph(two_clusters, k=2)
        labels = community_labels(g, 6, method="louvain")
        assert labels.shape == (6,)
        # The two cosine clusters should not all collapse to one community.
        assert len(set(labels.tolist())) >= 2

    def test_kmeans(self, two_clusters: np.ndarray) -> None:
        g = knn_graph(two_clusters, k=2)
        labels = community_labels(
            g, 6, method="kmeans", embeddings=two_clusters, n_clusters=2
        )
        assert labels.shape == (6,)
        assert set(labels.tolist()) == {0, 1}

    def test_kmeans_without_embeddings_raises(self, two_clusters: np.ndarray) -> None:
        g = knn_graph(two_clusters, k=2)
        with pytest.raises(ValueError, match="requires embeddings"):
            community_labels(g, 6, method="kmeans")

    def test_unknown_method_raises(self, two_clusters: np.ndarray) -> None:
        g = knn_graph(two_clusters, k=2)
        with pytest.raises(ValueError, match="must be 'louvain' or 'kmeans'"):
            community_labels(g, 6, method="spectral")  # type: ignore[arg-type]


class TestBackbone:
    """The disparity filter returns a subgraph and never mutates the input."""

    def test_does_not_mutate_input(self, two_clusters: np.ndarray) -> None:
        g = knn_graph(two_clusters, k=3)
        before = g.number_of_edges()
        extract_backbone(g, min_alpha_ptile=0.5)
        assert g.number_of_edges() == before

    def test_subgraph(self, two_clusters: np.ndarray) -> None:
        g = knn_graph(two_clusters, k=3)
        bb = extract_backbone(g, min_alpha_ptile=0.3)
        assert bb.number_of_nodes() <= g.number_of_nodes()
        assert bb.number_of_edges() <= g.number_of_edges()

    def test_low_degree_node_alpha_zero(self) -> None:
        assert edge_alpha(0.9, 1.0) == 0.0


class TestAnalyzeText:
    """analyze_text returns aligned channel arrays from injected embeddings."""

    def test_arrays_align_to_sentences(self) -> None:
        from lexograph import segment

        text = "The cat sat. The cat sat again. A dog ran far away now."
        n = len(segment(text))
        rng = np.random.default_rng(1)
        emb = rng.standard_normal((n, 8))
        emb /= np.linalg.norm(emb, axis=1, keepdims=True)

        analysis = analyze_text(text, embeddings=emb)
        assert len(analysis.sentences) == n
        assert analysis.size.shape == (n,)
        assert analysis.community.shape == (n,)
        assert analysis.distances.shape == (n, n)

    def test_backbone_option(self) -> None:
        text = "The cat sat. The cat sat again. A dog ran far away now."
        from lexograph import segment

        n = len(segment(text))
        rng = np.random.default_rng(2)
        emb = rng.standard_normal((n, 8))
        emb /= np.linalg.norm(emb, axis=1, keepdims=True)
        analysis = analyze_text(text, embeddings=emb, backbone=True)
        assert analysis.size.shape == (n,)

    def test_wrong_embedding_count_raises(self) -> None:
        with pytest.raises(ValueError, match="one row per sentence"):
            analyze_text("One. Two. Three.", embeddings=np.zeros((2, 4)))


@pytest.mark.skipif(
    not os.environ.get("LEXOGRAPH_RUN_MODEL"),
    reason="set LEXOGRAPH_RUN_MODEL=1 to run the model download smoke test",
)
def test_embed_sentences_smoke() -> None:
    """Smoke-test the real embedder (downloads a model; opt-in via env var)."""
    pytest.importorskip("sentence_transformers")
    from lexograph.analyze.embeddings import embed_sentences

    vectors = embed_sentences(["hello world", "a second sentence"])
    assert vectors.shape[0] == 2
    norms = np.linalg.norm(vectors, axis=1)
    assert np.allclose(norms, 1.0, atol=1e-3)
