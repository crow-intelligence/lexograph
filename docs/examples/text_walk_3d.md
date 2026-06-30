# 3-D text walk

The bundled chapter as a 3-D corkscrew: the same space-filling turtle walk, but
each sentence also climbs a constant step in z, so the rectangular walk winds
upward. Rendered with matplotlib's `mplot3d`.

```python
--8<-- "examples/text_walk_3d_demo.py"
```

Run it with:

```bash
uv run python examples/text_walk_3d_demo.py
```

It is the same `text_walk` preset as the 2-D walk, with `helix=True`. Raise
`z_step` for a taller, more tightly wound corkscrew.
