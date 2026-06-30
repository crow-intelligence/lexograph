# Graph analysis (`[graph]` extra)

Drive the presets from semantics. The analysis layer embeds the sentences, builds
a cosine kNN graph, and reads two channels off it — **PageRank** centrality for
size and **Louvain** community for colour — plus a cosine distance matrix for a
semantic recurrence dotplot.

Install the extra first:

```bash
uv add "lexograph[graph]"
```

```python
--8<-- "examples/graph_analysis_demo.py"
```

Run it with:

```bash
uv run python examples/graph_analysis_demo.py
```

The same arrays feed any preset: this is the [data contract](../index.md#the-data-contract)
in action — `analyze_text` just *produces* arrays, and the core draws them without
ever importing a transformer.
