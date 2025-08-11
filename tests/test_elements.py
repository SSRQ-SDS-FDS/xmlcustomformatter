"""This module tests the processing of elements."""

from xml.dom.minidom import Element
from pathlib import Path

import pytest

from xmlcustomformatter.formatter import XMLCustomFormatter


class TestXMLCustomFormatterElements:
    """This class tests the processing of elements."""

    @pytest.mark.parametrize(
        "xml_content, expected",
        [
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
    def test_is_empty_element(self, tmp_path: Path, xml_content: str, expected: bool) -> None:
        """Tests that empty and non-empty elements are classified correctly."""
        file_path = tmp_path / "input.xml"
        file_path.write_text(xml_content)
        formatter = XMLCustomFormatter(str(file_path), "output.xml")
        if isinstance(formatter._dom.documentElement, Element):
            assert formatter._is_empty_element(formatter._dom.documentElement) == expected

    # ToDo: Add tests of functionality
