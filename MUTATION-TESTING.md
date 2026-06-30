# Mutation testing

lexograph uses [mutmut](https://github.com/boxed/mutmut) to check that the test suite
actually pins the behaviour of the numeric core, rather than merely executing it. It is
a **dev-only** gate — it is not run in CI (a full run is slow), but it should be run
before a release and after any change to the layout geometry.

## Scope

Mutation is scoped (in `pyproject.toml`, `[tool.mutmut]`) to the math-heavy layout
modules, where a silently-passing test is most dangerous:

- `layout/walk.py` — the turtle step/turn geometry
- `layout/walk3d.py` — the corkscrew lift
- `layout/spiral.py` — the Archimedean arc-length placement
- `layout/recurrence.py` — the Jaccard self-similarity
- `layout/dispersion.py` — the term offsets and KWIC windows

Rendering, presets, and the optional analysis layer are excluded: their correctness is
about *what is drawn*, which is verified by structural assertions and eyeballed example
figures, not by arithmetic a mutant would flip.

## Running

```bash
LEXOGRAPH_MUTATION=1 uv run mutmut run
uv run mutmut results
```

The `LEXOGRAPH_MUTATION` environment variable loads a Hypothesis profile (see
`tests/conftest.py`) that suppresses the `differing_executors` health check, which the
forked mutmut workers would otherwise trip, and disables the shared example database so
runs are independent.

The selected test files (`tests/test_walk.py`, `test_spiral.py`, `test_recurrence.py`,
`test_dispersion.py`, plus `test_geometry.py`) are fast and plotting-free, which keeps a
run tractable.
