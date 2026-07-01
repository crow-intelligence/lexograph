# Pre-mortem

Where lexograph is most likely to mislead or break, and what guards each risk. The
goal is to name the failure modes before a user hits them.

## Segmentation

- **The offline sentence splitter mis-splits.** The default splitter is a regex with
  an abbreviation guard and a dialogue-attribution guard (`"Is it let?" she asked.`
  stays whole). It will still err on abbreviations outside its list, ellipses used as
  terminators, or sentences that genuinely begin lowercase. *Guard:* `segment(...,
  punkt=True)` switches to NLTK Punkt for higher quality; the splitter is documented as
  a heuristic, and the units it returns are the package's seam, so a caller can supply
  their own list.
- **Tokenisation is deliberately simple.** `tokens` is a word-character regex; it is not
  linguistic tokenisation. For real lemmatised tokens, pre-tokenise (e.g. with `kenon`)
  and pass the units in.

## The walk

- **The rectangular walk self-overlaps.** Always turning the same way means the path
  crosses itself; with near-uniform step lengths it collapses into a tight knot. This is
  faithful to the source algorithm, **not** a bug — but there is no space-filling or
  de-overlap guarantee, and a walk of very uniform sentences can be illegible. *Guard:*
  the width-step spreads real prose out; `turn` is configurable for non-rectangular
  walks; the documentation states the overlap is expected.
- **Rendered width is an outline extent, not an advance width.** `rendered_widths`
  measures the glyph-outline bounding box via `TextPath`, which omits side bearings and
  trailing spaces. Steps are therefore slightly short of true set width. *Guard:* the
  step is a *relative* quantity (the walk is scale-free), and whitespace-only units fall
  back to a per-character estimate so the turtle still advances.

## Grids

- **Jaccard is noisy on short sentences.** Two short sentences sharing one function word
  can read as "recurrent"; two paraphrases with no shared surface tokens read as
  unrelated. *Guard:* `shingle=k` switches to character n-grams; the `[graph]` extra
  supplies an embedding distance matrix for semantic recurrence.
- **Recurrence is O(N²).** The distance matrix and the plot are quadratic in sentence
  count; a book-length text is slow and the dotplot is dense. *Guard:* documented; the
  bundled examples are chapter-sized.
- **Concordance matches single whole tokens.** A multi-word term or a lemma family is not
  matched. *Guard:* documented; `term_offsets`/`kwic` operate on the same tokeniser the
  user can inspect.

## The `[graph]` analysis layer

- **First use downloads a model.** `embed_sentences` fetches a sentence-transformers
  model over the network. *Guard:* the import is deferred, embeddings are injectable
  (`analyze_text(text, embeddings=...)`), and every pipeline test uses synthetic vectors,
  so nothing in CI depends on a download.
- **Community labels can drift across library versions.** Louvain is seeded, but the
  result can still vary with the networkx version. *Guard:* the seed is fixed and exposed;
  KMeans is offered as a deterministic alternative.

## Rendering and packaging

- **Figures need a headless backend in some environments.** lexograph builds `Figure`
  objects directly and never calls `show()`, so it is headless by construction; a user
  who imports `pyplot` themselves on a no-display box must select Agg. *Guard:*
  documented in Troubleshooting.
- **Handwriting fonts are not vendored.** The width-step and glyph modes use matplotlib's
  default font; the four OFL/Apache handwriting faces from the source piece are not
  bundled. *Guard:* `text_walk(font=...)` accepts any TTF. Vendoring them (with licence
  notices) is tracked in `CHANGES_SUMMARY.md`.
