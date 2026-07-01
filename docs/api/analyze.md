# Analysis layer (`[graph]` extra)

The optional analysis pipeline: sentence embeddings → cosine kNN graph →
(optional disparity backbone) → PageRank and community detection. Install it with
`uv add "lexograph[graph]"`. Everything here only *produces* the plain per-unit
arrays the `encode` channels accept; the core never imports it.

::: lexograph.analyze.analyze_text

::: lexograph.analyze.Analysis

::: lexograph.analyze.embeddings.embed_sentences

::: lexograph.analyze.graph.knn_graph

::: lexograph.analyze.graph.embedding_distances

::: lexograph.analyze.graph.pagerank_scores

::: lexograph.analyze.graph.community_labels

::: lexograph.analyze.backbone.extract_backbone
