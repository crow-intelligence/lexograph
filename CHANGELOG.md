# Changelog

All notable changes to lexograph are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/), and the project adheres to
semantic versioning.

## [Unreleased]

### Added

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
