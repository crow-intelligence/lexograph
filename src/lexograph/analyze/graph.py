"""Build a sentence graph from embeddings and read channels off it.

The pipeline ported from the Wittgenstein piece: sentence embeddings → a cosine
k-nearest-neighbour graph → PageRank centrality (the **size** channel) and
community detection (the **colour** channel). All functions take and return plain
arrays / a networkx graph, so the results drop straight into ``encode``.

Part of the optional ``lexograph[graph]`` extra.
"""

from __future__ import annotations

from typing import Literal, cast

import networkx as nx
import numpy as np
from sklearn.metrics.pairwise import cosine_distances
from sklearn.neighbors import kneighbors_graph

from lexograph._types import FloatArray

__all__ = [
    "knn_graph",
    "embedding_distances",
    "pagerank_scores",
    "community_labels",
]

CommunityMethod = Literal["louvain", "kmeans"]


def knn_graph(embeddings: FloatArray, *, k: int = 5) -> nx.Graph:
    """Build a weighted cosine k-nearest-neighbour graph over the embeddings.

    Node ``i`` is sentence ``i``; an edge carries the cosine **similarity**
    (``1 - cosine distance``) as its ``weight``. The graph is undirected: the
    mutual edge keeps the stronger of the two directed similarities.

    Args:
        embeddings: An ``(N, D)`` array of sentence embeddings.
        k: Neighbours per node (capped at ``N - 1``).

    Returns:
        A networkx graph with nodes ``0 .. N-1`` and weighted edges.

    Examples:
        >>> import numpy as np
        >>> emb = np.eye(4)
        >>> g = knn_graph(emb, k=1)
        >>> g.number_of_nodes()
        4
    """
    n = len(embeddings)
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    if n < 2:
        return graph
    k_eff = min(k, n - 1)
    adjacency = kneighbors_graph(
        np.asarray(embeddings, dtype=float),
        n_neighbors=k_eff,
        mode="distance",
        metric="cosine",
        include_self=False,
    ).tocoo()
    for i, j, distance in zip(
        adjacency.row, adjacency.col, adjacency.data, strict=True
    ):
        weight = 1.0 - float(distance)
        if weight <= 0.0:
            continue
        if graph.has_edge(int(i), int(j)):
            graph[int(i)][int(j)]["weight"] = max(
                graph[int(i)][int(j)]["weight"], weight
            )
        else:
            graph.add_edge(int(i), int(j), weight=weight)
    return graph


def embedding_distances(embeddings: FloatArray) -> FloatArray:
    """Return the pairwise cosine distance matrix of the embeddings.

    Ready to pass as ``distances`` to
    :func:`lexograph.presets.recurrence.recurrence_plot` for a semantic
    recurrence dotplot.

    Args:
        embeddings: An ``(N, D)`` array of sentence embeddings.

    Returns:
        An ``(N, N)`` cosine distance matrix with a zero diagonal.

    Examples:
        >>> import numpy as np
        >>> d = embedding_distances(np.eye(3))
        >>> d.shape
        (3, 3)
    """
    return np.asarray(
        cosine_distances(np.asarray(embeddings, dtype=float)), dtype=float
    )


def pagerank_scores(graph: nx.Graph, n: int) -> FloatArray:
    """Return weighted PageRank as a per-sentence array (the size channel).

    Args:
        graph: A weighted sentence graph (e.g. from :func:`knn_graph`).
        n: The total sentence count, so the result aligns to every sentence even
            if the graph has dropped some nodes.

    Returns:
        A length-``n`` float array; entry ``i`` is the PageRank of node ``i`` (or
        ``0.0`` if the node is absent or the graph has no edges).

    Examples:
        >>> import networkx as nx
        >>> g = nx.path_graph(3)
        >>> for u, v in g.edges():
        ...     g[u][v]["weight"] = 1.0
        >>> pagerank_scores(g, 3).shape
        (3,)
    """
    if graph.number_of_edges() == 0:
        return np.zeros(n, dtype=float)
    ranks = nx.pagerank(graph, weight="weight")
    return np.asarray([ranks.get(i, 0.0) for i in range(n)], dtype=float)


def community_labels(
    graph: nx.Graph,
    n: int,
    *,
    method: CommunityMethod = "louvain",
    embeddings: FloatArray | None = None,
    n_clusters: int = 10,
    seed: int = 42,
) -> np.ndarray:
    """Return a per-sentence community label (the colour channel).

    Args:
        graph: A weighted sentence graph (used by the Louvain method).
        n: The total sentence count, so labels align to every sentence.
        method: ``"louvain"`` (graph communities, the default) or ``"kmeans"``
            (clusters the embeddings directly).
        embeddings: Required for ``"kmeans"``; the ``(N, D)`` embedding array.
        n_clusters: Number of clusters for ``"kmeans"`` (capped at ``N``).
        seed: Random seed for reproducibility.

    Returns:
        A length-``n`` integer array of community ids. For Louvain, id ``0`` is
        the largest community; a node absent from the graph gets ``-1``.

    Raises:
        ValueError: If ``method`` is ``"kmeans"`` and ``embeddings`` is ``None``,
            or ``method`` is unrecognised.

    Examples:
        >>> import networkx as nx
        >>> g = nx.path_graph(4)
        >>> for u, v in g.edges():
        ...     g[u][v]["weight"] = 1.0
        >>> labels = community_labels(g, 4)
        >>> labels.shape
        (4,)
    """
    if method == "kmeans":
        if embeddings is None:
            msg = "kmeans community detection requires embeddings"
            raise ValueError(msg)
        from sklearn.cluster import KMeans

        k = min(n_clusters, n)
        labels = KMeans(n_clusters=k, random_state=seed, n_init=10).fit_predict(
            np.asarray(embeddings, dtype=float)
        )
        return labels.astype(int)
    if method == "louvain":
        raw = cast(
            "list[set[int]]",
            nx.community.louvain_communities(graph, weight="weight", seed=seed),
        )
        communities = sorted(raw, key=len, reverse=True)
        label_of = {
            node: cid for cid, members in enumerate(communities) for node in members
        }
        return np.asarray([label_of.get(i, -1) for i in range(n)], dtype=int)
    msg = f"method must be 'louvain' or 'kmeans', got {method!r}"
    raise ValueError(msg)
