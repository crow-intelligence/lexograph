"""Segment raw text into an ordered list of units.

A *unit* is the atom lexograph lays out and draws: a single character, a token,
or a sentence. Segmentation is the first step of the spine; everything
downstream (layout, encode, render) consumes the ordered list this module
returns.

Sentence splitting defaults to a self-contained, offline regex splitter that
guards common abbreviations (so ``Mr. Bennet`` is not cut in two). Pass
``punkt=True`` to use NLTK's Punkt model instead — higher quality, at the cost
of a one-time model download.
"""

from __future__ import annotations

import re

from lexograph._types import Unit, UnitKind

__all__ = ["segment", "characters", "tokens", "sentences"]

# A token: a run of word characters, allowing internal apostrophes and hyphens
# (so ``good-humoured`` and ``don't`` stay whole).
_TOKEN_RE = re.compile(r"\w+(?:['’-]\w+)*")

# A candidate sentence terminator: end punctuation, optional closing quotes or
# brackets, then whitespace. The whitespace requirement avoids splitting inside
# decimals and ellipses mid-token.
_SENTENCE_END_RE = re.compile(r'[.!?]+["\'”’)\]]*\s+')

# The word immediately before a candidate terminator.
_TRAILING_WORD_RE = re.compile(r"(\w+)\W*$")

# The first letter at or after a position (Unicode-aware, excludes digits).
_NEXT_LETTER_RE = re.compile(r"[^\W\d_]")

# Abbreviations whose trailing period is not a sentence boundary.
_ABBREVIATIONS = frozenset(
    {
        "mr", "mrs", "ms", "dr", "prof", "sr", "jr", "st", "mt", "rev", "hon",
        "gen", "col", "capt", "sgt", "lt", "messrs",
        "vs", "etc", "al", "no", "vol", "fig", "pp", "inc", "ltd", "co",
        "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep", "sept",
        "oct", "nov", "dec",
    }
)  # fmt: skip


def characters(text: str) -> list[Unit]:
    """Return every character of ``text`` in order.

    Args:
        text: The source text.

    Returns:
        One single-character string per character, including whitespace and
        punctuation (the punctuation-spiral preset filters these itself).

    Examples:
        >>> characters("Hi!")
        ['H', 'i', '!']
    """
    return list(text)


def tokens(text: str) -> list[Unit]:
    """Return the word tokens of ``text`` in order.

    A token is a run of word characters with optional internal apostrophes or
    hyphens; punctuation and whitespace are dropped.

    Args:
        text: The source text.

    Returns:
        The ordered list of word tokens.

    Examples:
        >>> tokens("It's a good-humoured day.")
        ["It's", 'a', 'good-humoured', 'day']
    """
    return _TOKEN_RE.findall(text)


def sentences(text: str, *, punkt: bool = False) -> list[Unit]:
    """Split ``text`` into sentences, in order.

    Args:
        text: The source text.
        punkt: If ``True``, use NLTK's Punkt sentence tokenizer (downloading the
            model on first use). If ``False`` (the default), use the bundled
            offline regex splitter, which guards common abbreviations.

    Returns:
        The ordered list of sentences, each stripped of surrounding whitespace.
        Empty or whitespace-only sentences are dropped.

    Examples:
        >>> sentences("Mr. Bennet replied that he had not. He said no more.")
        ['Mr. Bennet replied that he had not.', 'He said no more.']
    """
    if punkt:
        return _punkt_sentences(text)
    return _regex_sentences(text)


def _regex_sentences(text: str) -> list[Unit]:
    """Split into sentences with the offline, abbreviation-aware regex splitter."""
    result: list[Unit] = []
    start = 0
    for match in _SENTENCE_END_RE.finditer(text):
        prefix = text[start : match.start()]
        trailing = _TRAILING_WORD_RE.search(prefix)
        if trailing is not None:
            word = trailing.group(1)
            if word.lower() in _ABBREVIATIONS:
                continue
            # A single capital letter is an initial (e.g. "A. Bennet"), not an end.
            if len(word) == 1 and word.isalpha() and word.isupper():
                continue
        # If the next sentence would start with a lowercase letter, this
        # terminator sits inside a larger sentence — e.g. dialogue followed by
        # an attribution: '"Is it let?" she asked.' — so it is not a boundary.
        following = _NEXT_LETTER_RE.search(text, match.end())
        if following is not None and following.group(0).islower():
            continue
        sentence = text[start : match.end()].strip()
        if sentence:
            result.append(sentence)
        start = match.end()
    tail = text[start:].strip()
    if tail:
        result.append(tail)
    return result


def _punkt_sentences(text: str) -> list[Unit]:
    """Split into sentences with NLTK Punkt, fetching the model if needed."""
    import nltk

    try:
        nltk.data.find("tokenizers/punkt_tab")
    except LookupError:
        nltk.download("punkt_tab", quiet=True)
    from nltk.tokenize import sent_tokenize

    return [s.strip() for s in sent_tokenize(text) if s.strip()]


def segment(
    text: str, unit: UnitKind = "sentences", *, punkt: bool = False
) -> list[Unit]:
    """Segment ``text`` into ordered units of the requested kind.

    This is the single entry point to the segmentation step of the spine.

    Args:
        text: The source text.
        unit: ``"chars"``, ``"tokens"``, or ``"sentences"``.
        punkt: Use NLTK Punkt for sentence splitting (ignored for other kinds).

    Returns:
        The ordered list of units.

    Raises:
        ValueError: If ``unit`` is not one of the three recognised kinds.

    Contract:
        - The returned list preserves source order.
        - ``"chars"`` keeps every character; ``"tokens"`` and ``"sentences"``
          drop pure-whitespace units.

    Examples:
        >>> segment("One. Two.", unit="sentences")
        ['One.', 'Two.']
        >>> segment("One two", unit="tokens")
        ['One', 'two']
        >>> len(segment("abc", unit="chars"))
        3
    """
    if unit == "chars":
        return characters(text)
    if unit == "tokens":
        return tokens(text)
    if unit == "sentences":
        return sentences(text, punkt=punkt)
    msg = f"unit must be 'chars', 'tokens', or 'sentences', got {unit!r}"
    raise ValueError(msg)
