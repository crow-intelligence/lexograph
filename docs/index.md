# lexograph

Spatialize linear text into pictures you can read — in pure Python, rendered with
matplotlib.

lexograph turns a text into a picture through one four-step spine: **segment** the text
into ordered units (characters, tokens, or sentences), **lay them out** in 2-D or 3-D
space, **encode** per-unit attributes onto visual channels (size, colour, glyph), and
**render** a matplotlib figure. Each preset is just a point on that spine.

## Presets

- **Punctuation spiral** — non-alphanumeric marks along an Archimedean spiral, coloured
  by symbol class.
- **Text walk (2-D / 3-D)** — sentences stepping forward and turning 90°, space-filling;
  the 3-D variant lifts into a corkscrew.
- **Recurrence dotplot** — a sentence × sentence self-similarity grid: the text against
  itself.
- **Concordance** — a term's dispersion across text and time, with optional KWIC.

## The data contract

Every visual channel is fed by a **plain per-unit array**: a scalar array for `size`, an
array of labels or values for `colour`, an optional `glyph`/font. The core never needs
to know where the numbers came from — you can drive a figure from `length`, `frequency`,
or your own column with no analysis stack at all.

## Quick links

- [Quickstart](quickstart.md) — install and load the bundled text
- [Troubleshooting](troubleshooting.md) — common errors and fixes
- [API Reference](api/datasets.md) — every public function and its contract

---

Made by [Crow Intelligence](https://crowintelligence.org/)
