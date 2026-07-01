# Spine demo

The four steps of the spine — **segment → layout → encode → render** — composed
end to end on the bundled *Pride and Prejudice* text. The chapter's sentences are
laid out as a field of tiles, each tile sized by sentence length and coloured by
its row in the chapter.

```python
--8<-- "examples/spine_demo.py"
```

Run it with:

```bash
uv run python examples/spine_demo.py
```

It writes `spine_demo.png` to the current directory. The function returns a
matplotlib `Figure`, so in a notebook you can display it inline instead of saving.
