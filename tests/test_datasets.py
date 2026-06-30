from lexograph import load_demo_text


class TestLoadDemoText:
    """The bundled demo text is the opening chapter of Pride and Prejudice."""

    def test_opening_line(self, demo_text: str) -> None:
        assert demo_text.startswith("It is a truth universally acknowledged")

    def test_is_substantial(self, demo_text: str) -> None:
        # Enough sentences and characters to make a layout legible.
        assert len(demo_text) > 2_000
        assert "Bingley" in demo_text

    def test_is_deterministic(self) -> None:
        assert load_demo_text() == load_demo_text()
