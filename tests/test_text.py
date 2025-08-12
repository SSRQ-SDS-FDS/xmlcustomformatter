"""This module tests the processing of text nodes."""

from pathlib import Path
from typing import cast

import pytest

from pytest import FixtureRequest

from xmlcustomformatter.formatter import XMLCustomFormatter
from xmlcustomformatter.options import Options


class TestCustomXMLFormatterText:
    """This class tests the processing of text nodes."""

    @staticmethod
    @pytest.fixture(
        params=[
            (
                "<root>foo</root>",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root>foo</root>""",
                Options(inline_elements=("root",)),
            ),
            (
                "<root>foo bar</root>",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root>foo bar</root>""",
                Options(inline_elements=("root",)),
            ),
            (
                "<root>foo \tbar</root>",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root>foo bar</root>""",
                Options(inline_elements=("root",)),
            ),
            (
                "<root>foo \nbar</root>",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root>foo bar</root>""",
                Options(inline_elements=("root",)),
            ),
            (
                "<root>foo \n\nbar</root>",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root>foo bar</root>""",
                Options(inline_elements=("root",)),
            ),
            (
                "<root>foo \t       \n\nbar</root>",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root>foo bar</root>""",
                Options(inline_elements=("root",)),
            ),
            (
                "<root>   foo bar    </root>",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root> foo bar </root>""",
                Options(inline_elements=("root",)),
            ),
        ],
        ids=[
            "text without spaces",
            "text with space",
            "text with tab",
            "text with newline",
            "text with multiple newlines",
            "text with various whitespaces",
            "test with leading and trailing whitespace",
        ],
    )
    def textnodes(request: FixtureRequest) -> tuple[str, str, Options]:
        """Yields xml_content, expected result."""
        return cast(tuple[str, str, Options], request.param)

    @staticmethod
    @pytest.fixture
    def xml_files(tmp_path: Path, textnodes: tuple[str, str, Options]) -> tuple[str, str]:
        """Writes the XML content to a temp file and returns the path as a string."""
        xml_content, _, _ = textnodes
        input_path = tmp_path / "input.xml"
        output_path = tmp_path / "output.xml"
        input_path.write_text(xml_content)
        return str(input_path), str(output_path)

    @staticmethod
    def test_textnodes(textnodes: tuple[str, str, Options], xml_files: tuple[str, str]) -> None:
        """Tests that textnodes are processed correctly."""
        _, expected, options = textnodes
        input_file, output_file = xml_files
        formatter = XMLCustomFormatter(input_file, output_file, options)
        assert formatter.get_result_as_string() == expected
