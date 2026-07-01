# Concordance

Where the main characters and themes fall across the chapter. Each term is a row;
each tick is one occurrence at its token offset.

```python
--8<-- "examples/concordance_demo.py"
```

Run it with:

```bash
uv run python examples/concordance_demo.py
```

It also prints keyword-in-context lines for one term via
`lexograph.layout.dispersion.kwic`. Pass `normalize=True` to scale the x-axis to
the fraction of the text rather than absolute token offset.
