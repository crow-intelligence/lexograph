"""Disparity-filter backbone extraction for weighted graphs.

The multiscale backbone of Serrano, Boguñá & Vespignani (2009),
https://arxiv.org/pdf/0904.2389.pdf — it keeps the statistically significant
edges of a weighted graph and discards the rest. Ported from the sibling
``kenon`` package's ``backbone`` module (which in turn follows DerwenAI's
``disparity_filter``); used here to sparsify the kNN sentence graph before
PageRank and community detection.

Part of the optional ``lexograph[graph]`` extra.
"""

from __future__ import annotations

import copy

import networkx as nx
import numpy as np

__all__ = [
    "disparity_integral",
    "edge_alpha",
    "apply_disparity_filter",
    "extract_backbone",
]


def disparity_integral(x: float, degree: float) -> float:
    """Evaluate the disparity-filter PDF integral ``(1-x)^k / ((k-1)(x-1))``.

    Args:
        x: A normalised edge weight (must not be exactly 1.0).
        degree: A node degree ``k`` (must not be exactly 1.0).

    Returns:
        The value of the integral at ``x`` for degree ``degree``.

    Examples:
        >>> disparity_integral(0.5, 3.0) != disparity_integral(0.0, 3.0)
        True
    """
    return ((1.0 - x) ** degree) / ((degree - 1.0) * (x - 1.0))


def edge_alpha(norm_weight: float, degree: float) -> float:
    """Return the disparity significance ``alpha`` of one edge endpoint.

    Args:
        norm_weight: The edge weight divided by the node's strength.
        degree: The node's degree.

    Returns:
        ``alpha`` in ``[0, 1]``; lower means more significant. A node of degree
        ``<= 1`` yields ``0.0``.

    Examples:
        >>> 0.0 <= edge_alpha(0.5, 3.0) <= 1.0
        True
        >>> edge_alpha(0.9, 1.0)
        0.0
    """
    if degree <= 1.0:
        return 0.0
    return 1.0 - (degree - 1.0) * (
        disparity_integral(norm_weight, degree) - disparity_integral(0.0, degree)
    )


def apply_disparity_filter(graph: nx.Graph) -> list[float]:
    """Attach disparity statistics to every edge and node, in place.

    Each node gains a ``strength`` (sum of incident weights); each edge gains
    ``norm_weight``, ``alpha`` (the more significant of its two endpoints), and
    ``alpha_ptile`` (the percentile of its alpha among all edges).

    Args:
        graph: A weighted networkx graph (edges carry a ``weight``).

    Returns:
        The list of all edge alpha values.

    Examples:
        >>> import networkx as nx
        >>> g = nx.Graph()
        >>> g.add_edge("a", "b", weight=0.8)
        >>> g.add_edge("b", "c", weight=0.3)
        >>> g.add_edge("a", "c", weight=0.5)
        >>> len(apply_disparity_filter(g)) == g.number_of_edges()
        True
    """
    if graph.number_of_edges() == 0:
        return []

    for node in graph.nodes():
        graph.nodes[node]["strength"] = sum(
            data.get("weight", 1.0) for _, _, data in graph.edges(node, data=True)
        )

    alphas: list[float] = []
    for u, v, data in graph.edges(data=True):
        weight = data.get("weight", 1.0)
        alpha_u = _endpoint_alpha(graph, u, weight)
        alpha_v = _endpoint_alpha(graph, v, weight)
        data["alpha"] = min(alpha_u, alpha_v)
        alphas.append(data["alpha"])

    sorted_alphas = np.array(sorted(alphas))
    for _u, _v, data in graph.edges(data=True):
        data["alpha_ptile"] = float(
            np.searchsorted(sorted_alphas, data["alpha"])
        ) / len(sorted_alphas)
    return alphas


def _endpoint_alpha(graph: nx.Graph, node: object, weight: float) -> float:
    """Disparity alpha of ``weight`` as seen from one endpoint ``node``."""
    strength = graph.nodes[node]["strength"]
    degree = float(graph.degree(node))
    norm = weight / strength if strength > 0 else 0.0
    return edge_alpha(norm, degree)


def extract_backbone(
    graph: nx.Graph,
    *,
    min_alpha_ptile: float = 0.5,
    min_degree: int = 1,
) -> nx.Graph:
    """Return the disparity-filter backbone of a weighted graph.

    The input is copied (never mutated): edges below ``min_alpha_ptile`` are
    dropped, then nodes whose degree falls below ``min_degree`` are pruned
    iteratively until stable.

    Args:
        graph: A weighted networkx graph.
        min_alpha_ptile: Edges with an alpha percentile below this are removed.
        min_degree: Nodes left with a degree below this are pruned (``1`` keeps
            any node that still has an edge).

    Returns:
        A new graph containing only the backbone.

    Examples:
        >>> import networkx as nx
        >>> g = nx.path_graph(5)
        >>> for u, v in g.edges():
        ...     g[u][v]["weight"] = float(v + 1)
        >>> bb = extract_backbone(g, min_alpha_ptile=0.3)
        >>> bb.number_of_nodes() <= g.number_of_nodes()
        True
    """
    if graph.number_of_edges() == 0:
        return nx.Graph()

    result = copy.deepcopy(graph)
    apply_disparity_filter(result)
    result.remove_edges_from(
        [
            (u, v)
            for u, v, data in result.edges(data=True)
            if data.get("alpha_ptile", 0.0) < min_alpha_ptile
        ]
    )
    changed = True
    while changed:
        prune = [n for n in list(result.nodes()) if result.degree(n) < min_degree]
        changed = bool(prune)
        result.remove_nodes_from(prune)
    return result
