import pytest

from lexograph.layout.dispersion import kwic, term_offsets


class TestTermOffsets:
    """Term offsets are the token indices where each term occurs."""

    def test_offsets(self) -> None:
        offsets = term_offsets("the cat and the dog and the cat", ["cat", "dog"])
        assert offsets["cat"].tolist() == [1.0, 7.0]
        assert offsets["dog"].tolist() == [4.0]

    def test_case_sensitivity(self) -> None:
        sensitive = term_offsets("Cat cat CAT", ["cat"], ignore_case=False)
        assert sensitive["cat"].tolist() == [1.0]
        insensitive = term_offsets("Cat cat CAT", ["cat"], ignore_case=True)
        assert insensitive["cat"].tolist() == [0.0, 1.0, 2.0]

    def test_missing_term_is_empty(self) -> None:
        offsets = term_offsets("the cat sat", ["dog"])
        assert offsets["dog"].tolist() == []

    def test_preserves_term_order(self) -> None:
        offsets = term_offsets("a b c", ["c", "a", "b"])
        assert list(offsets.keys()) == ["c", "a", "b"]


class TestKwic:
    """KWIC returns the context tokens around each occurrence."""

    def test_basic(self) -> None:
        lines = kwic("the small cat sat on the cat mat", "cat", width=2)
        assert len(lines) == 2
        assert (lines[0].left, lines[0].keyword, lines[0].right) == (
            "the small",
            "cat",
            "sat on",
        )

    def test_edge_truncates_context(self) -> None:
        lines = kwic("cat sat down", "cat", width=3)
        assert lines[0].left == ""
        assert lines[0].right == "sat down"

    def test_keyword_preserves_original_case(self) -> None:
        lines = kwic("The Cat sat", "cat", width=1)
        assert lines[0].keyword == "Cat"

    def test_negative_width_raises(self) -> None:
        with pytest.raises(ValueError, match="non-negative"):
            kwic("the cat", "cat", width=-1)
