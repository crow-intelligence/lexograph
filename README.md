<p align="center">
  <img src="https://raw.githubusercontent.com/crow-intelligence/lexograph/main/docs/assets/logo.png" alt="lexograph" width="480">
</p>

# lexograph

Spatialize linear text into pictures you can read — in pure Python, rendered with
matplotlib.

lexograph is the visualization member of the corpus-lx family (alongside
[chronowords](https://github.com/crow-intelligence/chronowords),
[kenon](https://github.com/crow-intelligence/kenon), and
[keyflux](https://github.com/crow-intelligence/keyflux)). It turns a text into a
picture through one four-step spine — **segment → layout → encode → render** — and
ships several presets that are each just a point on that spine:

- **Punctuation spiral** — every non-alphanumeric mark, in order, along an Archimedean
  spiral, coloured by symbol class.
- **Text walk (2-D / 3-D)** — each sentence steps forward and turns 90°, space-filling;
  size, colour, and glyph encode per-unit attributes. The 3-D variant lifts the walk
  into a corkscrew.
- **Recurrence dotplot** — the only preset that plots a text against *itself*: a
  sentence × sentence self-similarity grid that exposes internal echo structure.
- **Concordance** — a term's dispersion across the text (and across texts/time), with
  optional KWIC.

Every preset returns a matplotlib `Figure` and never calls `show()`, so it renders
inline in Jupyter and saves cleanly with `fig.savefig(...)`. The core is headless and
dependency-light; heavy analysis (sentence embeddings, graph centrality, communities)
lives behind an optional `[graph]` extra.

## Installation

```bash
uv add lexograph
```

The core depends only on `numpy`, `matplotlib`, and `nltk`.

## Quickstart

```python
from lexograph import (
    load_demo_text, punctuation_spiral, text_walk, recurrence_plot, concordance,
)

text = load_demo_text()  # Chapter 1 of Pride and Prejudice (public domain)

punctuation_spiral(text)                              # marks on an Archimedean spiral
text_walk(text)                                      # the 2-D space-filling walk
text_walk(text, helix=True, z_step=4.0)              # the 3-D corkscrew
recurrence_plot(text)                                # the text against itself
concordance(text, ["Bennet", "Bingley", "wife"])    # term dispersion
```

Every call returns a matplotlib `Figure`. For PageRank-sized, community-coloured, or
semantically-recurrent figures, install the `[graph]` extra and feed
`lexograph.analyze.analyze_text`'s arrays into any preset.

## The data contract

Every visual channel is fed by a **plain per-unit array** — a scalar array for `size`,
an array of labels or values for `colour`, an optional `glyph`/font. Nothing in the
core knows where those numbers came from, so you can drive a spiral or a walk from
`length`, `frequency`, or your own column with no analysis stack at all. The optional
`analyze` layer and the `[kenon]` / `[chronowords]` integrations only *produce* arrays
that satisfy this contract.

## Documentation

Full documentation — quickstart, a tutorial per preset, troubleshooting, and the API
reference — is at [lexograph.readthedocs.io](https://lexograph.readthedocs.io). The
sources live in `docs/`.

## Roadmap

Open modelling and packaging decisions are analysed in
[`CHANGES_SUMMARY.md`](CHANGES_SUMMARY.md), and the failure modes in
[`PRE-MORTEM.md`](PRE-MORTEM.md). The main not-yet-built pieces:

- [ ] Vendor the four OFL/Apache handwriting fonts so the handwriting walk works out of
      the box (the width-step already runs on any TTF).
- [ ] `integrations/` — thin `[kenon]` and `[chronowords]` adapters over the data contract.
- [ ] Optional interactive HTML/WebGL export (`render/html.py`), ported from the source
      viewers and gated behind a stretch extra.
- [ ] A space-filling / non-self-overlapping turn rule for very uniform texts.

## Made by

lexograph is made by [Crow Intelligence](https://crowintelligence.org/).

## License

MIT
