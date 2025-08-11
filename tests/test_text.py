"""This module tests the processing of text nodes."""

from pathlib import Path
from typing import cast

import pytest

from pytest import FixtureRequest

from xmlcustomformatter.formatter import XMLCustomFormatter


class TestCustomXMLFormatterText:
    """This class tests the processing of text nodes."""

    @staticmethod
    @pytest.fixture(
        params=[
            (
                "<root>foo</root>",
                """<?xml version="1.0" encoding="UTF-8"?><root>foo</root>""",
            ),
            (
                "<root>foo bar</root>",
                """<?xml version="1.0" encoding="UTF-8"?><root>foo bar</root>""",
            ),
            (
                "<root>foo \tbar</root>",
                """<?xml version="1.0" encoding="UTF-8"?><root>foo bar</root>""",
            ),
            (
                "<root>foo \nbar</root>",
                """<?xml version="1.0" encoding="UTF-8"?><root>foo bar</root>""",
            ),
            (
                "<root>foo \n\nbar</root>",
                """<?xml version="1.0" encoding="UTF-8"?><root>foo bar</root>""",
            ),
            (
                "<root>foo \t       \n\nbar</root>",
                """<?xml version="1.0" encoding="UTF-8"?><root>foo bar</root>""",
            ),
            (
                "<root>   foo bar    </root>",
                """<?xml version="1.0" encoding="UTF-8"?><root> foo bar </root>""",
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
    def textnodes(request: FixtureRequest) -> tuple[str, str]:
        """Yields xml_content, expected result."""
        return cast(tuple[str, str], request.param)

    @staticmethod
    @pytest.fixture
    def xml_file(tmp_path: Path, textnodes: tuple[str, str]) -> str:
        """Writes the XML content to a temp file and returns the path as a string."""
        xml_content, _ = textnodes
        file_path = tmp_path / "input.xml"
        file_path.write_text(xml_content)
        return str(file_path)

    @staticmethod
    def test_textnodes(textnodes: tuple[str, str], xml_file: str) -> None:
        """Tests that textnodes are processed correctly."""
        _, expected = textnodes
        formatter = XMLCustomFormatter(xml_file, "output.xml")
        assert formatter.get_result_as_string() == expected
