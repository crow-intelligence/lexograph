# Quickstart

From a clean install to a bundled text in one sitting. Every snippet is runnable as-is.

## Installation

```bash
uv add lexograph
```

lexograph is pure Python — it renders figures with matplotlib and needs no JavaScript
runtime. Its core dependencies are `numpy`, `matplotlib`, and `nltk`.

## Load the bundled text

lexograph ships a tiny public-domain demo text — the first chapter of Jane Austen's
*Pride and Prejudice* — so every example runs with no downloads.

```python
from lexograph import load_demo_text

text = load_demo_text()
print(text[:52])
# It is a truth universally acknowledged, that a singl
```

## Draw a preset

Each preset segments the text, lays the units out, encodes per-unit attributes, and
returns a matplotlib `Figure`.

```python
from lexograph import load_demo_text, punctuation_spiral, text_walk

text = load_demo_text()

# Every punctuation mark and logical sign, wound onto an Archimedean spiral.
spiral = punctuation_spiral(text)
spiral.savefig("punctuation_spiral.png", dpi=150)

# Each sentence as a step of a space-filling turtle walk, coloured by position.
walk = text_walk(text)
walk.savefig("text_walk.png", dpi=150)
```

Both return a `Figure` and never call `show()`, so they display inline in Jupyter and
save cleanly from a script. The `text_walk` colour and size channels accept any
per-sentence array — `length`, `frequency`, a community id, or your own column — which
is the [data contract](index.md#the-data-contract) that keeps lexograph general.

## More presets

The same `text` drives every preset:

```python
from lexograph import recurrence_plot, concordance

recurrence_plot(text)                                  # the text against itself
concordance(text, ["Bennet", "Bingley", "wife"])       # term dispersion
text_walk(text, helix=True, z_step=4.0)                # the 3-D corkscrew
```

For semantics (PageRank size, community colour, embedding-distance dotplots), install the
`[graph]` extra and use `lexograph.analyze.analyze_text`.

## Next steps

- [The spine](tutorials/the_spine.md) — the four steps every preset shares, and the data
  contract that keeps lexograph general.
- The [examples](examples/punctuation_spiral.md) render each preset from the bundled text.
