"""This module tests the processing of CDATASections."""

from pathlib import Path
from typing import cast

import pytest

from pytest import FixtureRequest

from xmlcustomformatter.formatter import XMLCustomFormatter


class TestCustomXMLFormatterCDATA:
    """This class tests the processing of CDATASections."""

    @staticmethod
    @pytest.fixture(
        params=[
            (
                "<root><![CDATA[foo]]></root>",
                """<?xml version="1.0" encoding="UTF-8"?><root><![CDATA[foo]]></root>""",
            ),
            (
                "<root><![CDATA[foo bar]]></root>",
                """<?xml version="1.0" encoding="UTF-8"?><root><![CDATA[foo bar]]></root>""",
            ),
            (
                "<root><![CDATA[foo \tbar]]></root>",
                """<?xml version="1.0" encoding="UTF-8"?><root><![CDATA[foo bar]]></root>""",
            ),
            (
                "<root><![CDATA[foo \nbar]]></root>",
                """<?xml version="1.0" encoding="UTF-8"?><root><![CDATA[foo bar]]></root>""",
            ),
            (
                "<root><![CDATA[foo \n\nbar]]></root>",
                """<?xml version="1.0" encoding="UTF-8"?><root><![CDATA[foo bar]]></root>""",
            ),
            (
                "<root><![CDATA[foo \t       \n\nbar]]></root>",
                """<?xml version="1.0" encoding="UTF-8"?><root><![CDATA[foo bar]]></root>""",
            ),
            (
                "<root><![CDATA[   foo bar    ]]></root>",
                """<?xml version="1.0" encoding="UTF-8"?><root><![CDATA[foo bar]]></root>""",
            ),
            (
                "<root><![CDATA[ foo ]]><![CDATA[ bar ]]></root>",
                '<?xml version="1.0" encoding="UTF-8"?><root><![CDATA[foo]]><![CDATA[bar]]></root>',
            ),
        ],
        ids=[
            "cdata without spaces",
            "cdata with space",
            "cdata with tab",
            "cdata with newline",
            "cdata with multiple newlines",
            "cdata with various whitespaces",
            "cdata with leading and trailing whitespace",
            "two cdata sections",
        ],
    )
    def cdatanodes(request: FixtureRequest) -> tuple[str, str]:
        """Yields xml_content, expected result."""
        return cast(tuple[str, str], request.param)

    @staticmethod
    @pytest.fixture
    def xml_file(tmp_path: Path, cdatanodes: tuple[str, str]) -> str:
        """Writes the XML content to a temp file and returns the path as a string."""
        xml_content, _ = cdatanodes
        file_path = tmp_path / "input.xml"
        file_path.write_text(xml_content)
        return str(file_path)

    @staticmethod
    def test_cdata_noted(cdatanodes: tuple[str, str], xml_file: str) -> None:
        """Tests that CDATASections are processed correctly."""
        _, expected = cdatanodes
        formatter = XMLCustomFormatter(xml_file, "output.xml")
        assert formatter.get_result_as_string() == expected
