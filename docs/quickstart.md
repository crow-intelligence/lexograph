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

## Next steps

The remaining presets (3-D walk, recurrence dotplot, concordance) land over the
following build phases, each on the same spine.
