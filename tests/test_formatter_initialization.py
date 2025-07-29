import pytest

from pathlib import Path
from xmlcustomformatter.formatter import XMLCustomFormatter
from xmlcustomformatter.options import Options
from xml.dom.minidom import Document


class TestXMLCustomFormatterInitialization:
    """
    Unit tests for the initialization behavior of the XMLCustomFormatter class.
    """

    @pytest.fixture
    def indentation_at_start(self) -> int:
        """Returns the indentation level at the start of the formatting process."""
        return 0

    @pytest.fixture
    def result_at_start(self) -> list[str]:
        """Returns the empty result at the start of the formatting process."""
        return ['<?xml version="1.0" encoding="UTF-8"?>']

    @pytest.fixture
    def options(self) -> Options:
        """Returns an Options object"""
        return Options(2, 100, ("div", "span"))

    @pytest.fixture
    def xml_content(self) -> str:
        """Returns XML content as a string"""
        return """<?xml version="1.0" encoding="UTF-8"?><root/>"""

    @pytest.fixture
    def xml_file(self, tmp_path: Path, xml_content: str) -> str:
        """Returns a file path as a string"""
        file_path = tmp_path / "input.xml"
        file_path.write_text(xml_content, encoding="utf-8")
        return str(file_path)

    @pytest.fixture
    def default_formatter(self, xml_file: str) -> XMLCustomFormatter:
        """Returns an instance with default formatting options."""
        return XMLCustomFormatter(xml_file, "output.xml")

    @pytest.fixture
    def custom_formatter(self, options: Options, xml_file: str) -> XMLCustomFormatter:
        """Returns an instance with custom formatting options."""
        return XMLCustomFormatter(xml_file, "output.xml", options)

    def test_sets_input_file(
        self, default_formatter: XMLCustomFormatter, xml_file: str
    ) -> None:
        """Checks that the input_file attribute is set correctly upon initialization."""
        assert default_formatter.input_file == xml_file

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

    def test_dom_instance(self, default_formatter: XMLCustomFormatter) -> None:
        """
        Checks that the input file is correctly parsed to a Document object.
        """
        assert isinstance(default_formatter._dom, Document)

    def test_dom_root_element_is_not_none(
        self, default_formatter: XMLCustomFormatter
    ) -> None:
        """
        Checks that the root element is correctly parsed from the input file.
        """
        assert default_formatter._dom.documentElement is not None

    def test_dom_root_element_is_root(
        self, default_formatter: XMLCustomFormatter
    ) -> None:
        """
        Checks that the root element is correctly parsed from the input file.
        """
        if default_formatter._dom.documentElement is not None:
            assert default_formatter._dom.documentElement.tagName == "root"

    def test_file_not_found(self) -> None:
        """
        Test that initializing XMLCustomFormatter with a non-existent input file
        raises a FileNotFoundError.
        """
        non_existing_path = "does_not_exist.xml"
        with pytest.raises(FileNotFoundError):
            XMLCustomFormatter(non_existing_path, "output.xml")

    def test_indentation_level_at_start(
        self, default_formatter: XMLCustomFormatter, indentation_at_start: int
    ) -> None:
        assert default_formatter._indentation_level == indentation_at_start

    def test_result_at_start(
        self, default_formatter: XMLCustomFormatter, result_at_start: list[str]
    ) -> None:
        print(repr(default_formatter._dom.standalone))
        assert default_formatter._result == result_at_start
