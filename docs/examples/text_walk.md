# Text walk

The bundled chapter as a space-filling turtle walk: each sentence steps forward
by its rendered width and turns 90°. Each step is coloured by its position in the
chapter and weighted by sentence length.

```python
--8<-- "examples/text_walk_demo.py"
```

Run it with:

```bash
uv run python examples/text_walk_demo.py
```

Pass `mode="glyphs"` to set each sentence's text along its segment
(calligraphy-on-path) instead of drawing a coloured ribbon.
