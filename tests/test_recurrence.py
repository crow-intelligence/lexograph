import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st

from lexograph.layout.recurrence import recurrence_distances, recurrence_matrix

sentence_lists = st.lists(
    st.text(alphabet="abcde ", min_size=0, max_size=20),
    min_size=1,
    max_size=12,
)


class TestRecurrenceDistances:
    """Jaccard self-distance is symmetric, zero-diagonal, and in [0, 1]."""

    def test_identical_sentences_distance_zero(self) -> None:
        d = recurrence_distances(["the cat sat", "the cat sat"])
        assert d[0, 1] == 0.0

    def test_disjoint_sentences_distance_one(self) -> None:
        d = recurrence_distances(["alpha beta", "gamma delta"])
        assert d[0, 1] == 1.0

    def test_character_shingle(self) -> None:
        d = recurrence_distances(["running", "runner"], shingle=3)
        assert 0.0 < d[0, 1] < 1.0

    @given(sentence_lists)
    def test_symmetric_zero_diagonal_bounded(self, units: list[str]) -> None:
        d = recurrence_distances(units)
        assert np.allclose(d, d.T)
        assert np.allclose(np.diag(d), 0.0)
        assert np.all((d >= 0.0) & (d <= 1.0))


class TestRecurrenceMatrix:
    """Thresholding lights similar cells; the diagonal is always on."""

    def test_threshold(self) -> None:
        d = np.array([[0.0, 0.2, 0.9], [0.2, 0.0, 0.8], [0.9, 0.8, 0.0]])
        grid = recurrence_matrix(d, threshold=0.5)
        assert grid.tolist() == [
            [True, True, False],
            [True, True, False],
            [False, False, True],
        ]

    def test_diagonal_always_on(self) -> None:
        d = recurrence_distances(["a b", "c d", "e f"])
        grid = recurrence_matrix(d, threshold=0.0)
        assert np.all(np.diag(grid))

    def test_non_square_raises(self) -> None:
        with pytest.raises(ValueError, match="square"):
            recurrence_matrix(np.zeros((2, 3)))
