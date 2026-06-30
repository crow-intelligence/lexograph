# Recurrence dotplot

The bundled chapter plotted against itself. The strong main diagonal is each
sentence matching itself; the symmetric off-diagonal dots mark sentences that
echo one another — here, the repeated dialogue exchanges between the Bennets.

```python
--8<-- "examples/recurrence_demo.py"
```

Run it with:

```bash
uv run python examples/recurrence_demo.py
```

Pass `mode="distance"` for the full similarity heatmap, `shingle=k` for
character-`k`-gram similarity, or a precomputed `distances` matrix (e.g. an
embedding distance from the `[graph]` extra) to drive it from semantics.
