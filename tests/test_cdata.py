"""This module tests the processing of CDATASections."""

from pathlib import Path
from typing import cast

import pytest

from pytest import FixtureRequest

from xmlcustomformatter.formatter import XMLCustomFormatter
from xmlcustomformatter.options import Options


class TestCustomXMLFormatterCDATA:
    """This class tests the processing of CDATASections."""

    @staticmethod
    @pytest.fixture(
        params=[
            (
                "<root><![CDATA[foo]]></root>",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root><![CDATA[foo]]></root>""",
                Options(inline_elements=("root",)),
            ),
            (
                "<root><![CDATA[foo bar]]></root>",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root><![CDATA[foo bar]]></root>""",
                Options(inline_elements=("root",)),
            ),
            (
                "<root><![CDATA[foo \tbar]]></root>",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root><![CDATA[foo bar]]></root>""",
                Options(inline_elements=("root",)),
            ),
            (
                "<root><![CDATA[foo \nbar]]></root>",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root><![CDATA[foo bar]]></root>""",
                Options(inline_elements=("root",)),
            ),
            (
                "<root><![CDATA[foo \n\nbar]]></root>",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root><![CDATA[foo bar]]></root>""",
                Options(inline_elements=("root",)),
            ),
            (
                "<root><![CDATA[foo \t       \n\nbar]]></root>",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root><![CDATA[foo bar]]></root>""",
                Options(inline_elements=("root",)),
            ),
            (
                "<root><![CDATA[   foo bar    ]]></root>",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root><![CDATA[foo bar]]></root>""",
                Options(inline_elements=("root",)),
            ),
            (
                "<root><![CDATA[ foo ]]><![CDATA[ bar ]]></root>",
                '<?xml version="1.0" encoding="UTF-8"?>\n'
                "<root><![CDATA[foo]]><![CDATA[bar]]></root>",
                Options(inline_elements=("root",)),
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
    def cdatanodes(request: FixtureRequest) -> tuple[str, str, Options]:
        """Yields xml_content, expected result."""
        return cast(tuple[str, str, Options], request.param)

    @staticmethod
    @pytest.fixture
    def xml_files(tmp_path: Path, cdatanodes: tuple[str, str, Options]) -> tuple[str, str]:
        """Writes the XML content to a temp file and returns the path as a string."""
        xml_content, _, _ = cdatanodes
        input_path = tmp_path / "input.xml"
        output_path = tmp_path / "output.xml"
        input_path.write_text(xml_content)
        return str(input_path), str(output_path)

    @staticmethod
    def test_cdata_notes(cdatanodes: tuple[str, str, Options], xml_files: tuple[str, str]) -> None:
        """Tests that CDATASections are processed correctly."""
        _, expected, options = cdatanodes
        input_file, output_file = xml_files
        formatter = XMLCustomFormatter(input_file, output_file, options)
        assert formatter.get_result_as_string() == expected
