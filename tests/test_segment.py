import pytest
from hypothesis import given
from hypothesis import strategies as st

from lexograph.segment import characters, segment, sentences, tokens


class TestSegment:
    """The unified segment() entry point dispatches on unit kind."""

    def test_sentences_default(self) -> None:
        assert segment("One. Two.") == ["One.", "Two."]

    def test_tokens(self) -> None:
        assert segment("a b c", unit="tokens") == ["a", "b", "c"]

    def test_chars_keeps_everything(self) -> None:
        assert segment("a b", unit="chars") == ["a", " ", "b"]

    def test_unknown_unit_raises(self) -> None:
        with pytest.raises(ValueError, match="unit must be"):
            segment("x", unit="paragraphs")  # type: ignore[arg-type]


class TestSentences:
    """The offline splitter ends on .!? but guards abbreviations and initials."""

    def test_abbreviation_not_split(self) -> None:
        assert sentences("Mr. Bennet went home. He slept.") == [
            "Mr. Bennet went home.",
            "He slept.",
        ]

    def test_question_and_quote(self) -> None:
        assert sentences('"Is it let?" she asked. He nodded.') == [
            '"Is it let?" she asked.',
            "He nodded.",
        ]

    def test_initials_not_split(self) -> None:
        assert sentences("A. B. Smith arrived. They waited.") == [
            "A. B. Smith arrived.",
            "They waited.",
        ]

    def test_no_terminal_punctuation(self) -> None:
        assert sentences("just a fragment") == ["just a fragment"]

    def test_empty(self) -> None:
        assert sentences("") == []

    @given(st.text())
    def test_sentences_are_stripped_and_nonempty(self, text: str) -> None:
        for sentence in sentences(text):
            assert sentence == sentence.strip()
            assert sentence != ""


class TestTokensAndChars:
    """Tokens drop punctuation; chars keep every character in order."""

    def test_internal_apostrophe_and_hyphen(self) -> None:
        assert tokens("It's good-humoured.") == ["It's", "good-humoured"]

    @given(st.text())
    def test_chars_roundtrip(self, text: str) -> None:
        assert "".join(characters(text)) == text
