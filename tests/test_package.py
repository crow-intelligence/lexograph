import lexograph


class TestPackage:
    """The package exposes a version and its top-level public surface."""

    def test_version_is_a_string(self) -> None:
        assert isinstance(lexograph.__version__, str)
        assert lexograph.__version__.count(".") >= 2

    def test_public_api_is_importable(self) -> None:
        for name in lexograph.__all__:
            assert hasattr(lexograph, name)
