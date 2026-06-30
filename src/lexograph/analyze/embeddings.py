"""Embed sentences with a sentence-transformers model.

This is the only step that pulls in the heavy neural dependency, so the import is
deferred to call time: importing this module (and the rest of ``analyze``) is
cheap, and the model is loaded only when you actually embed. Every other
``analyze`` function takes the embedding array, so the whole graph pipeline can
be exercised with your own vectors and no model at all.

Part of the optional ``lexograph[graph]`` extra.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from lexograph._types import FloatArray

__all__ = ["embed_sentences", "DEFAULT_MODEL"]

DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
"""The default embedding model: small, CPU-fast, 384-dimensional."""


def embed_sentences(
    sentences: Sequence[str],
    *,
    model_name: str = DEFAULT_MODEL,
    batch_size: int = 64,
) -> FloatArray:
    """Embed sentences into L2-normalised vectors.

    The model is downloaded on first use and cached by ``sentence-transformers``.
    Because the embeddings are L2-normalised, a dot product equals cosine
    similarity.

    Args:
        sentences: The sentences to embed.
        model_name: A sentence-transformers model id.
        batch_size: Encoding batch size.

    Returns:
        An ``(N, D)`` float array of unit-norm sentence embeddings.

    Example:
        Not run as a doctest (it would download the model)::

            from lexograph import segment, load_demo_text
            from lexograph.analyze.embeddings import embed_sentences

            sentences = segment(load_demo_text())
            embeddings = embed_sentences(sentences)
    """
    import sentence_transformers as st  # ty: ignore[unresolved-import]

    model = st.SentenceTransformer(model_name)
    vectors = model.encode(
        list(sentences),
        batch_size=batch_size,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
    return np.asarray(vectors, dtype=float)
