from lexograph.scalars import frequencies, lengths, positions


class TestScalars:
    """The dependency-free per-unit channel sources."""

    def test_lengths(self) -> None:
        assert lengths(["hi", "there"]).tolist() == [2.0, 5.0]

    def test_positions(self) -> None:
        assert positions(4).tolist() == [0.0, 1.0, 2.0, 3.0]

    def test_frequencies(self) -> None:
        assert frequencies(["the", "cat", "the"]).tolist() == [2.0, 1.0, 2.0]

    def test_frequencies_case_insensitive(self) -> None:
        assert frequencies(["The", "the"]).tolist() == [2.0, 2.0]

    def test_frequencies_case_sensitive(self) -> None:
        assert frequencies(["The", "the"], ignore_case=False).tolist() == [1.0, 1.0]
