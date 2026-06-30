# Changelog

All notable changes to lexograph are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/), and the project adheres to
semantic versioning.

## [Unreleased]

### Added

- Phase 6 quality + docs.
  - `tests/test_geometry.py` — cross-cutting Hypothesis properties: every step turns the
    heading by exactly the turn angle, right-angle walk segments are perpendicular, the
    3-D corkscrew's xy projection equals the 2-D walk, and the spiral radius strictly
    increases.
  - `PRE-MORTEM.md` (failure modes and guards), `MUTATION-TESTING.md` (mutmut scope),
    `CHANGES_SUMMARY.md` (open decisions).
  - The spine tutorial; README quickstart showing all presets and a roadmap.
- Phase 5 analysis: the optional `lexograph[graph]` layer plus core scalars.
  - `lexograph.scalars` (core) — `lengths`, `positions`, `frequencies`: the
    dependency-free channel sources.
  - `lexograph.analyze` (`[graph]` extra) — `analyze_text` runs the pipeline
    (sentence embeddings → cosine kNN graph → optional disparity-filter backbone
    → PageRank for size, Louvain/KMeans communities for colour) and returns an
    `Analysis` of plain arrays, including a cosine `distances` matrix for a
    semantic recurrence dotplot. The core never imports this; the adapters
    depend inward.
  - The disparity-filter backbone is ported from the sibling `kenon` package
    (Serrano et al. 2009).
- Phase 4 grids: the two grid presets, each on a different grid.
  - `recurrence_plot` — the sentence × sentence self-similarity dotplot (a text
    against itself), via matplotlib `imshow`. Dependency-free token/character
    Jaccard distance by default (`layout.recurrence_distances` /
    `recurrence_matrix`), or a precomputed embedding distance matrix.
  - `concordance` — a term × text lexical-dispersion plot, with
    `layout.term_offsets` and keyword-in-context (`layout.kwic` / `KWIC`).
- Phase 3 corkscrew: the 3-D walk.
  - `layout.walk3d_layout` — the 2-D walk lifted by a constant step in z.
  - `render.render_path_3d` — a matplotlib 3-D path renderer with per-segment
    colours and line widths.
  - `text_walk(..., helix=True, z_step=...)` winds the walk into a corkscrew;
    `examples/text_walk_3d_demo.py` and docs.
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
