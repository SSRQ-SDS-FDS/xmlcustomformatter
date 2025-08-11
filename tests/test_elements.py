"""This module tests the processing of elements."""

from pathlib import Path
from typing import cast
from xml.dom.minidom import Element

import pytest
from pytest import FixtureRequest

from xmlcustomformatter.formatter import XMLCustomFormatter


class TestXMLCustomFormatterElements:
    """This class tests the processing of elements."""

    @staticmethod
    @pytest.fixture(
        params=[
            (
                """<root/>""",
                True,
            ),
            (
                """<root foo="bar"/>""",
                True,
            ),
            (
                """<root></root>""",
                True,
            ),
            (
                """<root> </root>""",
                False,
            ),
            (
                """<root>foo</root>""",
                False,
            ),
            (
                """<root><!--foo--></root>""",
                False,
            ),
            (
                """<root><?foo bar?></root>""",
                False,
            ),
            (
                """<root><![CDATA[foo]]></root>""",
                False,
            ),
            (
                """<root><![CDATA[]]></root>""",
                True,
            ),
        ],
        ids=[
            "element_is_empty",
            "element_with_attributes_is_empty",
            "element_is_empty-with-endtag",
            "element_is_not_empty_because_of_whitespace",
            "element_is_not_empty_because_of_other_text",
            "element_is_not_empty_because_of_comment",
            "element_is_not_empty_because_of_pi",
            "element_is_not_empty_because_of_cdata",
            "element_is_empty_because_of_empty_cdata",
        ],
    )
    def elements(request: FixtureRequest) -> tuple[str, bool]:
        """Yields xml_content, expected_result and an Options object"""
        return cast(tuple[str, bool], request.param)

    @staticmethod
    @pytest.fixture
    def xml_file(tmp_path: Path, elements: tuple[str, bool]) -> str:
        """Writes the XML content to a temp file and returns the path as a string."""
        xml_content, _ = elements
        file_path = tmp_path / "input.xml"
        file_path.write_text(xml_content)
        return str(file_path)

    @staticmethod
    def test_is_empty_element(xml_file: str, elements: tuple[str, bool]) -> None:
        """Tests that empty and non-empty elements are classified correctly."""
        _, expected = elements
        formatter = XMLCustomFormatter(xml_file, "output.xml")
        if isinstance(formatter._dom.documentElement, Element):
            assert formatter._is_empty_element(formatter._dom.documentElement) == expected

    # ToDo: Add tests of functionality
