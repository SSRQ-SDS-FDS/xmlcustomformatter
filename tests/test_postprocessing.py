"""This module tests the postprocessing."""

from pathlib import Path
from typing import cast

import pytest

from pytest import FixtureRequest

from xmlcustomformatter.formatter import XMLCustomFormatter
from xmlcustomformatter.options import Options


class TestCustomXMLFormatterPostprocessing:
    """This class tests the postprocessing."""

    @staticmethod
    @pytest.fixture(
        params=[
            (
                "<root>12345678901234567890123456789012345678901234567890</root>",
                '<?xml version="1.0" encoding="UTF-8"?>\n'
                "<root>12345678901234567890123456789012345678901234567890</root>",
                Options(inline_elements=("root",), max_line_length=40),
            ),
            (
                "<root>1234567890 1234567890123456789012345678901234567890</root>",
                '<?xml version="1.0" encoding="UTF-8"?>\n'
                "<root>1234567890\n"
                "1234567890123456789012345678901234567890</root>",
                Options(inline_elements=("root",), max_line_length=40),
            ),
            (
                "<root>12345678901234567890123456789012345678901234 567890</root>",
                '<?xml version="1.0" encoding="UTF-8"?>\n'
                "<root>12345678901234567890123456789012345678901234\n"
                "567890</root>",
                Options(inline_elements=("root",), max_line_length=40),
            ),
        ],
        ids=[
            "text with no whitespace",
            "text with whitespace before max_line_length",
            "text with whitespace after max_line_length",
        ],
    )
    def long_lines(request: FixtureRequest) -> tuple[str, str, Options]:
        """Yields xml_content, expected result."""
        return cast(tuple[str, str, Options], request.param)

    @staticmethod
    @pytest.fixture
    def xml_files(tmp_path: Path, long_lines: tuple[str, str, Options]) -> tuple[str, str]:
        """Writes the XML content to a temp file and returns the path as a string."""
        xml_content, _, _ = long_lines
        input_path = tmp_path / "input.xml"
        output_path = tmp_path / "output.xml"
        input_path.write_text(xml_content)
        return str(input_path), str(output_path)

    @staticmethod
    def test_textnodes(long_lines: tuple[str, str, Options], xml_files: tuple[str, str]) -> None:
        """Tests that textnodes are processed correctly."""
        _, expected, options = long_lines
        input_file, output_file = xml_files
        formatter = XMLCustomFormatter(input_file, output_file, options)
        assert formatter.get_result_as_string() == expected
