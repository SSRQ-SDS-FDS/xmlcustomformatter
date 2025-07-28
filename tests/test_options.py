import pytest
from xmlcustomformatter.options import Options


class TestDefaultOptions:
    """
    Unit tests for the default behavior of the Options class.
    """

    @pytest.fixture
    def default_options(self) -> Options:
        """
        Fixture that provides an Options instance with default values.
        """
        return Options()

    @pytest.fixture
    def default_indentation(self) -> int:
        """
        Fixture for the default indentation value.
        """
        return 4

    @pytest.fixture
    def default_max_line_length(self) -> int:
        """
        Fixture for the default max_line_length value.
        """
        return 80

    @pytest.fixture
    def default_inline_elements(self) -> tuple[()]:
        """
        Fixture for the default inline_elements tuple.
        """
        return ()

    def test_default_indentation(
        self, default_options: Options, default_indentation: int
    ) -> None:
        """
        Tests that the default indentation value is correctly set.
        """
        assert default_options.indentation == default_indentation

    def test_default_max_line_length(
        self, default_options: Options, default_max_line_length: int
    ) -> None:
        """
        Tests that the default max_line_length value is correctly set.
        """
        assert default_options.max_line_length == default_max_line_length

    def test_default_inline_elements(
        self, default_options: Options, default_inline_elements
    ) -> None:
        """
        Tests that the default inline_elements tuple is correctly set.
        """
        assert default_options.inline_elements == default_inline_elements


class TestCustomOptions:
    @pytest.mark.parametrize("indentation", [2, 0, 10])
    def test_custom_indentation(self, indentation: int) -> None:
        """
        Tests that custom indentation values are accepted and correctly set.
        """
        options = Options(indentation=indentation)
        assert options.indentation == indentation

    @pytest.mark.parametrize("max_line_length", [50, 120, 0])
    def test_custom_max_line_length(self, max_line_length: int) -> None:
        """
        Tests that custom max_line_length values are accepted and correctly set.
        """
        options = Options(max_line_length=max_line_length)
        assert options.max_line_length == max_line_length

    @pytest.mark.parametrize(
        "inline_elements",
        [
            ("div", "span"),
            tuple(),
            ("a",),
        ],
    )
    def test_custom_inline_elements(self, inline_elements: tuple[str, ...]) -> None:
        """
        Tests that custom valid inline_elements tuples are accepted and correctly set.
        """
        options = Options(inline_elements=inline_elements)
        assert options.inline_elements == inline_elements

    @pytest.mark.parametrize(
        "invalid_input",
        [
            ["div", 42],  # includes integer
            (None,),  # includes None
            [object()],  # includes object
            (b"byte",),  # includes bytes
            [True],  # includes boolean
        ],
    )
    def test_custom_invalid_inline_elements(self, invalid_input: list) -> None:
        """
        Tests that custom invalid inline_elements raise a TypeError.
        """
        with pytest.raises(
            TypeError, match="inline_elements must contain only strings"
        ):
            Options(inline_elements=tuple(invalid_input))
