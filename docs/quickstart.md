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

## Next steps

The preset front ends (punctuation spiral, text walk, recurrence dotplot, concordance)
land over the following build phases. Each one segments this text, lays the units out,
encodes per-unit attributes, and returns a matplotlib `Figure` you can save with
`fig.savefig(...)` or display inline in Jupyter.
