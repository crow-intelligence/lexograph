# The spine: segment → layout → encode → render

Every lexograph preset is the same four steps. Understanding them lets you compose your
own figure when no preset fits, and shows why the package stays general.

## 1. Segment

Turn the text into an ordered list of units — characters, tokens, or sentences.

```python
from lexograph import load_demo_text, segment

text = load_demo_text()
units = segment(text, unit="sentences")   # or "tokens", or "chars"
```

The sentence splitter is offline and abbreviation-aware by default; pass `punkt=True`
for NLTK Punkt.

## 2. Layout

Give each unit a position in 2-D or 3-D space. The layouts are pure coordinate
generators:

```python
from lexograph import walk_layout, rendered_widths

steps = rendered_widths(units)          # the width-step
coords = walk_layout(steps)             # (N+1, 2) vertices
```

Other layouts: `spiral_layout`, `walk3d_layout`, `linear_layout`, and the grid builders
in `lexograph.layout.recurrence` and `lexograph.layout.dispersion`.

## 3. Encode

Map per-unit attributes onto visual channels. **This is the data contract**: every
channel is fed by a plain per-unit array. The numbers can come from anywhere.

```python
from lexograph import normalize_size, categorical_colors, lengths

sizes = normalize_size(lengths(units), lo=0.5, hi=6.0)
colours = categorical_colors([i // 8 for i in range(len(units))])
```

Built-in scalars (`lengths`, `positions`, `frequencies`) need nothing installed. The
optional `lexograph.analyze` layer *produces arrays of exactly the same shape* — PageRank
for size, community for colour — so swapping in semantics is a one-liner and the core
never learns where the numbers came from.

## 4. Render

Draw it. Every renderer returns a `matplotlib.figure.Figure` and never calls `show()`.

```python
from lexograph import render_path

fig = render_path(coords, colors=colours, linewidth=2.0)
fig.savefig("walk.png", dpi=150)   # or display inline in Jupyter
```

## Why this matters

Because the seam between steps is a plain array, someone with no analysis stack can draw a
spiral or a walk from `length`, `frequency`, or their own column — and someone with
embeddings, a `kenon` network, or `chronowords` shift scores can feed the *same* channels.
That is what makes lexograph a general package rather than an internal tool. Each preset
is just a convenient path through these four steps.
