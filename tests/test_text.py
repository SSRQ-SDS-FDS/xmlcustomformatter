"""This module tests the processing of text nodes."""

from pathlib import Path
from typing import cast
from xml.dom.minidom import Text

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
                "<root> </root>",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root> </root>""",
                Options(inline_elements=("root",)),
            ),
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
            "text consisting of just spaces",
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

    @staticmethod
    @pytest.mark.parametrize(
        "text_value, expected",
        [
            ("", True),
            ("   ", True),
            ("\n\t", True),
            ("foo", False),
            (" foo ", False),
            ("bar\n", False),
        ],
        ids=[
            "empty_string",
            "spaces_only",
            "tabs_newlines_only",
            "non_empty_string",
            "non_empty_with_spaces",
            "non_empty_with_newline",
        ],
    )
    def test_is_whitespace_only_text(text_value: str, expected: bool) -> None:
        """Tests whether a node consists of whitespace characters or not."""
        node = Text()
        node.data = text_value
        assert XMLCustomFormatter._is_whitespace_only_text(node) is expected
