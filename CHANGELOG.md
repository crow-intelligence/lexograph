# Changelog

All notable changes to lexograph are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/), and the project adheres to
semantic versioning.

## [Unreleased]

### Added

- Phase 2 walk + spiral: the first two presets and their layouts.
  - `layout.walk_layout` / `heading_angles` — the 2-D turtle walk (step forward,
    turn 90°), ported from the Wittgenstein piece's `compute_path`.
  - `layout.spiral_layout` / `tangent_angles` — equal-arc-length placement along
    an Archimedean spiral.
  - `layout.rendered_widths` — headless rendered-width measurement (matplotlib
    `TextPath`), the width-step that drives the walk.
  - `text_walk` preset — sentences as a space-filling walk, with `"path"` and
    `"glyphs"` (calligraphy-on-path) modes; built-in length/position channels.
  - `punctuation_spiral` preset — a text's marks on a spiral, accenting logical,
    mathematical, and Greek signs in gold.
  - `render.frame_axes` helper; `examples/` and docs for both presets.
- Phase 1 spine: the four-step pipeline end to end.
  - `segment` — split text into characters, tokens, or sentences. Sentence
    splitting defaults to a self-contained, abbreviation-aware offline splitter
    (keeps `Mr. Bennet` and `"Is it let?" she asked.` whole); `punkt=True` opts
    into NLTK Punkt.
  - `encode.channels` — the plain-array data contract: `normalize_size`,
    `categorical_colors`, `continuous_colors`, and the `Channels` container.
  - `layout.linear_layout` — a trivial reading-order grid layout.
  - `render` — `render_points` and `render_path` return a matplotlib `Figure`
    (no `pyplot`, never `show()`), rendering inline in Jupyter and saving with
    `fig.savefig(...)`.
  - `examples/spine_demo.py` renders the bundled chapter as a field of sentence
    tiles.
- Phase 0 scaffold: package layout mirroring the corpus-lx family (keyflux), uv build
  backend, ruff + ty + pytest (`--doctest-modules`) config, CI and publish workflows,
  mkdocs documentation skeleton, and the bundled *Pride and Prejudice* demo text
  (`lexograph.load_demo_text`).
