import pytest

from xmlcustomformatter.formatter import XMLCustomFormatter
from xmlcustomformatter.options import Options


class TestXMLCustomFormatterInitialization:
    """
    Unit tests for the initialization behavior of the XMLCustomFormatter class.
    """

    @pytest.fixture
    def options(self) -> Options:
        """Return an Options object"""
        return Options(2, 100, ("div", "span"))

    @pytest.fixture
    def default_formatter(self) -> XMLCustomFormatter:
        """Returns an instance with default formatting options."""
        return XMLCustomFormatter("input.xml", "output.xml")

    @pytest.fixture
    def custom_formatter(self, options: Options) -> XMLCustomFormatter:
        """Returns an instance with custom formatting options."""
        return XMLCustomFormatter("input.xml", "output.xml", options)

    def test_sets_input_file(self, default_formatter: XMLCustomFormatter) -> None:
        """Checks that the input_file attribute is set correctly upon initialization."""
        assert default_formatter.input_file == "input.xml"

    def test_sets_output_file(self, default_formatter: XMLCustomFormatter) -> None:
        """Checks that the output_file attribute is set correctly upon initialization."""
        assert default_formatter.output_file == "output.xml"

    def test_sets_default_formatting_options(
        self, default_formatter: XMLCustomFormatter
    ) -> None:
        """Verifies that the default Options object is used if no custom options are provided."""
        assert isinstance(default_formatter.options, Options)

    def test_custom_formatter_is_instance(
        self, custom_formatter: XMLCustomFormatter
    ) -> None:
        """Ensures that a custom Options object is correctly assigned to the formatter."""
        assert isinstance(custom_formatter.options, Options)

    def test_custom_formatter_indentation(
        self, custom_formatter: XMLCustomFormatter, options: Options
    ) -> None:
        """
        Validates that the indentation value from the custom Options is
        preserved in the formatter.
        """
        assert custom_formatter.options.indentation == options.indentation

    def test_custom_formatter_max_line_length(
        self, custom_formatter: XMLCustomFormatter, options: Options
    ) -> None:
        """
        Checks that the max_line_length from the custom Options is correctly
        assigned in the formatter.
        """
        assert custom_formatter.options.max_line_length == options.max_line_length

    def test_custom_formatter_inline_elements(
        self, custom_formatter: XMLCustomFormatter, options: Options
    ) -> None:
        """Checks that the inline_elements attribute is set correctly upon initialization."""
        assert custom_formatter.options.inline_elements == options.inline_elements
