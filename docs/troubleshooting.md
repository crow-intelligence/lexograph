# Troubleshooting

## A figure window never appears

lexograph never calls `matplotlib.pyplot.show()`. Every preset *returns* a
`matplotlib.figure.Figure`. In a script, save it; in Jupyter, let the cell display it:

```python
fig.savefig("out.png", dpi=150)  # script
fig                              # Jupyter: display the returned figure
```

## Running headless (CI, a server, a container)

The core is headless. If you import `matplotlib.pyplot` yourself in a no-display
environment, select the Agg backend before doing so:

```python
import matplotlib
matplotlib.use("Agg")
```

lexograph's own rendering does not require a display.

## The `[graph]` extra is not installed

The embedding-, centrality-, and community-based channels live behind an optional
extra. Install it with:

```bash
uv add "lexograph[graph]"
```

The dependency-light core (frequency, length, and position scalars) works without it.
