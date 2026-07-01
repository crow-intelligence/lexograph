import numpy as np
import pytest
from matplotlib.figure import Figure

from lexograph import (
    concordance,
    punctuation_spiral,
    recurrence_plot,
    segment,
    text_walk,
)
from lexograph.presets.punctuation_spiral import is_accent


class TestPunctuationSpiral:
    """The punctuation spiral plots every mark, accenting logical signs."""

    def test_returns_figure(self, demo_text: str) -> None:
        fig = punctuation_spiral(demo_text)
        assert isinstance(fig, Figure)
        assert len(fig.axes) == 1

    def test_draws_one_text_per_mark(self, demo_text: str) -> None:
        marks = [c for c in demo_text if not c.isalnum() and not c.isspace()]
        fig = punctuation_spiral(demo_text)
        assert len(fig.axes[0].texts) == len(marks)

    def test_no_marks_raises(self) -> None:
        with pytest.raises(ValueError, match="no punctuation"):
            punctuation_spiral("letters only no marks here")

    def test_is_accent(self) -> None:
        assert is_accent("=")
        assert is_accent("∀")
        assert not is_accent(",")
        assert not is_accent(";")


class TestTextWalk:
    """The text walk turns each sentence into a step of a space-filling path."""

    def test_returns_figure_path_mode(self, demo_text: str) -> None:
        fig = text_walk(demo_text)
        assert isinstance(fig, Figure)
        assert len(fig.axes[0].collections) == 1

    def test_glyph_mode_draws_text(self, demo_text: str) -> None:
        fig = text_walk(demo_text, mode="glyphs")
        assert len(fig.axes[0].texts) == len(segment(demo_text))

    def test_char_step_matches_width_step_shape(self, demo_text: str) -> None:
        fig = text_walk(demo_text, width_step=False)
        assert isinstance(fig, Figure)

    def test_custom_categorical_colour(self, demo_text: str) -> None:
        units = segment(demo_text)
        labels = [i % 3 for i in range(len(units))]
        fig = text_walk(demo_text, colour=labels, colour_kind="categorical")
        assert isinstance(fig, Figure)

    def test_helix_returns_3d_figure(self, demo_text: str) -> None:
        fig = text_walk(demo_text, helix=True)
        assert isinstance(fig, Figure)
        assert fig.axes[0].name == "3d"

    def test_helix_with_glyphs_raises(self, demo_text: str) -> None:
        with pytest.raises(ValueError, match="helix"):
            text_walk(demo_text, helix=True, mode="glyphs")

    def test_too_few_sentences_raises(self) -> None:
        with pytest.raises(ValueError, match="at least two sentences"):
            text_walk("Only one sentence here.")

    def test_wrong_colour_length_raises(self, demo_text: str) -> None:
        with pytest.raises(ValueError, match="one entry per sentence"):
            text_walk(demo_text, colour=[0, 1, 2])


class TestRecurrencePlot:
    """The recurrence dotplot plots the text against itself."""

    def test_returns_figure_with_image(self, demo_text: str) -> None:
        fig = recurrence_plot(demo_text)
        assert isinstance(fig, Figure)
        assert len(fig.axes[0].images) == 1

    def test_distance_mode(self, demo_text: str) -> None:
        fig = recurrence_plot(demo_text, mode="distance")
        assert isinstance(fig, Figure)

    def test_character_shingle(self, demo_text: str) -> None:
        fig = recurrence_plot(demo_text, shingle=4)
        assert isinstance(fig, Figure)

    def test_external_distances(self, demo_text: str) -> None:
        n = len(segment(demo_text))
        rng = np.zeros((n, n))
        fig = recurrence_plot(demo_text, distances=rng)
        assert isinstance(fig, Figure)

    def test_grid_is_square(self, demo_text: str) -> None:
        n = len(segment(demo_text))
        fig = recurrence_plot(demo_text)
        assert fig.axes[0].images[0].get_array().shape == (n, n)

    def test_bad_distances_shape_raises(self, demo_text: str) -> None:
        with pytest.raises(ValueError, match="must have shape"):
            recurrence_plot(demo_text, distances=np.zeros((3, 3)))

    def test_too_few_sentences_raises(self) -> None:
        with pytest.raises(ValueError, match="at least two sentences"):
            recurrence_plot("One sentence only.")


class TestConcordance:
    """The concordance plots each term's dispersion as a row of ticks."""

    def test_returns_figure(self, demo_text: str) -> None:
        fig = concordance(demo_text, ["Bennet", "Bingley", "wife"])
        assert isinstance(fig, Figure)
        assert len(fig.axes[0].get_yticks()) == 3

    def test_normalize(self, demo_text: str) -> None:
        fig = concordance(demo_text, ["Bennet"], normalize=True)
        assert fig.axes[0].get_xlim() == (0.0, 1.0)

    def test_empty_terms_raises(self, demo_text: str) -> None:
        with pytest.raises(ValueError, match="at least one term"):
            concordance(demo_text, [])
