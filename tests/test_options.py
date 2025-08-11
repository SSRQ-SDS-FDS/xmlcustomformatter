"""This module tests the behavior of the Options class."""

import pytest
from xmlcustomformatter.options import Options


class TestDefaultOptions:
    """This class tests the default behavior of the Options class."""

    @staticmethod
    @pytest.fixture
    def default_options() -> Options:
        """Fixture that provides an Options instance with default values."""
        return Options()

    @staticmethod
    @pytest.fixture
    def default_indentation() -> int:
        """Fixture for the default indentation value."""
        return 4

    @staticmethod
    @pytest.fixture
    def default_max_line_length() -> int:
        """Fixture for the default max_line_length value."""
        return 80

    @staticmethod
    @pytest.fixture
    def default_inline_elements() -> tuple[()]:
        """Fixture for the default inline_elements tuple."""
        return ()

    @staticmethod
    def test_default_indentation(default_options: Options, default_indentation: int) -> None:
        """Tests that the default indentation value is correctly set."""
        assert default_options.indentation == default_indentation

    @staticmethod
    def test_default_max_line_length(
        default_options: Options, default_max_line_length: int
    ) -> None:
        """Tests that the default max_line_length value is correctly set."""
        assert default_options.max_line_length == default_max_line_length

    @staticmethod
    def test_default_inline_elements(
        default_options: Options, default_inline_elements: tuple[()]
    ) -> None:
        """Tests that the default inline_elements tuple is correctly set."""
        assert default_options.inline_elements == default_inline_elements


class TestCustomOptions:
    """This class tests the custom behavior of the Options class."""

    @staticmethod
    @pytest.mark.parametrize("indentation", [2, 0, 10])
    def test_custom_indentation(indentation: int) -> None:
        """Tests that custom indentation values are accepted and correctly set."""
        options = Options(indentation=indentation)
        assert options.indentation == indentation

    @staticmethod
    @pytest.mark.parametrize("max_line_length", [50, 120, 0])
    def test_custom_max_line_length(max_line_length: int) -> None:
        """Tests that custom max_line_length values are accepted and correctly set."""
        options = Options(max_line_length=max_line_length)
        assert options.max_line_length == max_line_length

    @staticmethod
    @pytest.mark.parametrize(
        "inline_elements",
        [
            ("div", "span"),
            tuple(),
            ("a",),
        ],
        ids=["two-elements", "a-tuple", "one-element"],
    )
    def test_custom_inline_elements(inline_elements: tuple[str, ...]) -> None:
        """Tests that custom valid inline_elements tuples are accepted and correctly set."""
        options = Options(inline_elements=inline_elements)
        assert options.inline_elements == inline_elements

    @staticmethod
    @pytest.mark.parametrize(
        "invalid_input",
        [
            ["div", 42],
            (None,),
            [object()],
            (b"byte",),
            [True],
        ],
        ids=["integers", "none", "objects", "bytes", "booleans"],
    )
    def test_custom_invalid_inline_elements(invalid_input: list[str]) -> None:
        """
        Tests that custom invalid inline_elements raise a TypeError.
        """
        with pytest.raises(TypeError, match="inline_elements must contain only strings"):
            Options(inline_elements=tuple(invalid_input))
