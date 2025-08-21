"""This module tests the initialization behavior of the XMLCustomFormatter class."""

from pathlib import Path
from xml.dom.minidom import Document

import pytest

from xmlcustomformatter.formatter import XMLCustomFormatter
from xmlcustomformatter.options import Options


class TestXMLCustomFormatterInitialization:
    """Unit tests for the initialization behavior of the XMLCustomFormatter class."""

    @staticmethod
    @pytest.fixture
    def indentation_at_start() -> int:
        """Returns the indentation level at the start of the formatting process."""
        return 0

    @staticmethod
    @pytest.fixture
    def result_string_at_start() -> str:
        """Returns the empty result at the start of the formatting process."""
        return '<?xml version="1.0" encoding="UTF-8"?>\n<root/>'

    @staticmethod
    @pytest.fixture
    def options() -> Options:
        """Returns an Options object"""
        return Options(2, 100, ("div", "span"))

    @staticmethod
    @pytest.fixture
    def xml_content() -> str:
        """Returns XML content as a string"""
        return """<?xml version="1.0" encoding="UTF-8"?><root/>"""

    @staticmethod
    @pytest.fixture
    def xml_files(tmp_path: Path, xml_content: str) -> tuple[str, str]:
        """Returns a file path as a string"""
        input_path = tmp_path / "input.xml"
        output_path = tmp_path / "output.xml"
        input_path.write_text(xml_content, encoding="utf-8")
        return str(input_path), str(output_path)

    @staticmethod
    @pytest.fixture
    def default_formatter(xml_files: tuple[str, str]) -> XMLCustomFormatter:
        """Returns an instance with default formatting options."""
        input_file, output_file = xml_files
        return XMLCustomFormatter(input_file, output_file)

    @staticmethod
    @pytest.fixture
    def custom_formatter(options: Options, xml_files: tuple[str, str]) -> XMLCustomFormatter:
        """Returns an instance with custom formatting options."""
        input_file, output_file = xml_files
        return XMLCustomFormatter(input_file, output_file, options)

    @staticmethod
    def test_sets_input_file(
        default_formatter: XMLCustomFormatter, xml_files: tuple[str, str]
    ) -> None:
        """Checks that the input_file attribute is set correctly upon initialization."""
        input_file, _ = xml_files
        assert default_formatter.input_file == input_file

    @staticmethod
    def test_sets_output_file(
        default_formatter: XMLCustomFormatter, xml_files: tuple[str, str]
    ) -> None:
        """Checks that the output_file attribute is set correctly upon initialization."""
        _, output_file = xml_files
        assert default_formatter.output_file == output_file

    @staticmethod
    def test_sets_default_formatting_options(default_formatter: XMLCustomFormatter) -> None:
        """Verifies that the default Options object is used if no custom options are provided."""
        assert isinstance(default_formatter.options, Options)

    @staticmethod
    def test_custom_formatter_is_instance(custom_formatter: XMLCustomFormatter) -> None:
        """Ensures that a custom Options object is correctly assigned to the formatter."""
        assert isinstance(custom_formatter.options, Options)

    @staticmethod
    def test_custom_formatter_indentation(
        custom_formatter: XMLCustomFormatter, options: Options
    ) -> None:
        """
        Validates that the indentation value from the custom Options is
        preserved in the formatter.
        """
        assert custom_formatter.options.indentation == options.indentation

    @staticmethod
    def test_custom_formatter_max_line_length(
        custom_formatter: XMLCustomFormatter, options: Options
    ) -> None:
        """
        Checks that the max_line_length from the custom Options is correctly
        assigned in the formatter.
        """
        assert custom_formatter.options.max_line_length == options.max_line_length

    @staticmethod
    def test_custom_formatter_inline_elements(
        custom_formatter: XMLCustomFormatter, options: Options
    ) -> None:
        """Checks that the inline_elements attribute is set correctly upon initialization."""
        assert custom_formatter.options.inline_elements == options.inline_elements

    @staticmethod
    def test_dom_instance(default_formatter: XMLCustomFormatter) -> None:
        """Checks that the input file is correctly parsed to a Document object."""
        assert isinstance(default_formatter._dom, Document)

    @staticmethod
    def test_dom_root_element_is_not_none(default_formatter: XMLCustomFormatter) -> None:
        """Checks that the root element is correctly parsed from the input file."""
        assert default_formatter._dom.documentElement is not None

    @staticmethod
    def test_dom_root_element_is_root(default_formatter: XMLCustomFormatter) -> None:
        """Checks that the root element is correctly parsed from the input file."""
        if default_formatter._dom.documentElement is not None:
            assert default_formatter._dom.documentElement.tagName == "root"

    @staticmethod
    def test_file_not_found() -> None:
        """
        Test that initializing XMLCustomFormatter with a non-existent input file
        raises a FileNotFoundError.
        """
        non_existing_path = "does_not_exist.xml"
        with pytest.raises(FileNotFoundError):
            XMLCustomFormatter(non_existing_path, "output.xml")

    @staticmethod
    def test_indentation_level_at_start(
        default_formatter: XMLCustomFormatter, indentation_at_start: int
    ) -> None:
        """Tests that the indentation level is correctly set at start."""
        assert default_formatter._indentation_level == indentation_at_start

    @staticmethod
    def test_result_at_start(
        default_formatter: XMLCustomFormatter, result_string_at_start: str
    ) -> None:
        """Tests that the result is correctly set at start."""
        assert default_formatter.get_result_as_string() == result_string_at_start
