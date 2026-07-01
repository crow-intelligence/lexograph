# Open decisions

Modelling and packaging choices that are deliberate but worth revisiting. Each is a
place where a reasonable person might choose differently.

## Segmentation default

The default sentence splitter is the bundled offline regex, not NLTK Punkt. It keeps the
core dependency-light and deterministic and needs no model download, at the cost of some
accuracy on unusual abbreviations and lowercase-initial sentences. Punkt is one keyword
away (`punkt=True`). **Open:** whether to flip the default to Punkt once a text exceeds
some size, or to ship a small curated abbreviation list per language.

## The walk turns one way

`walk_layout` turns by a fixed angle every step (−90° by default), faithfully reproducing
the source piece's rectangular walk — which self-overlaps. We did **not** add a
space-filling (Hilbert-style) or collision-avoiding layout. **Open:** offer an alternating
or serpentine turn rule, or a true space-filling curve, as additional layouts for texts
whose sentences are too uniform to spread out under the rectangular walk.

## Rendered width vs advance width

The width-step uses the glyph **outline** extent from `TextPath`, not the typographic
advance width (which includes side bearings and trailing whitespace). It is simpler and
fully headless. **Open:** switch to advance widths if trailing-space-sensitive layouts
turn out to matter.

## Handwriting fonts not vendored

The source piece sets each sentence in one of four OFL/Apache handwriting faces. We did
**not** vendor them into the wheel; the width-step and glyph modes use matplotlib's
default font, and `text_walk(font=...)` accepts any TTF. **Open:** vendor the four faces
into `datasets/fonts/` with their licence notices and add an `assign_fonts`
adjacent-distinct selector, so the handwriting aesthetic works out of the box.

## Recurrence is quadratic

The recurrence distance matrix is computed with plain Python set operations, O(N²) in
sentences. Fine for a chapter, slow for a book. **Open:** vectorise the Jaccard (or accept
only the `[graph]` embedding path) for large inputs, and offer a windowed/banded dotplot.

## Interactive HTML/WebGL export

The source project ships Three.js/troika viewers. The optional HTML tier
(`render/html.py`) is **not** built yet. **Open:** port the viewers behind a stretch extra
once the matplotlib core is settled.

## Integrations

The `[kenon]` and `[chronowords]` adapters described in the spec are **not** built yet.
The data contract is in place (`encode` accepts plain arrays; `analyze` already produces
them), so the adapters are thin. **Open:** add `integrations/` with the two thin adapters.
