from xml.dom.minidom import Element

import pytest

from pathlib import Path

from xmlcustomformatter.formatter import XMLCustomFormatter


class TestXMLCustomFormatterElements:
    @pytest.mark.parametrize(
        "test_name, xml_content, expected",
        [
            (
                "element_is_empty",
                """<root/>""",
                True,
            ),
            (
                "element_with_attributes_is_empty",
                """<root foo="bar"/>""",
                True,
            ),
            (
                "element_is_empty-with-endtag",
                """<root></root>""",
                True,
            ),
            (
                "element_is_not_empty_because_of_whitespace",
                """<root> </root>""",
                False,
            ),
            (
                "element_is_not_empty_because_of_other_text",
                """<root>foo</root>""",
                False,
            ),
            (
                "element_is_not_empty_because_of_comment",
                """<root><!--foo--></root>""",
                False,
            ),
            (
                "element_is_not_empty_because_of_pi",
                """<root><?foo bar?></root>""",
                False,
            ),
            (
                "element_is_not_empty_because_of_cdata",
                """<root><![CDATA[foo]]></root>""",
                False,
            ),
            (
                "element_is_empty_because_of_empty_cdata",
                """<root><![CDATA[]]></root>""",
                True,
            ),
        ],
    )
    def test_empty_elements(
        self, tmp_path: Path, test_name: str, xml_content: str, expected: bool
    ) -> None:
        """Checks that empty and non-empty elements are classified correctly."""
        file_path = tmp_path / "input.xml"
        file_path.write_text(xml_content)
        formatter = XMLCustomFormatter(str(file_path), "output.xml")
        if isinstance(formatter._dom.documentElement, Element):
            assert formatter._is_empty_element(formatter._dom.documentElement) == expected
