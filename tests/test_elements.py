"""This module tests the processing of elements."""

from pathlib import Path
from typing import cast
from xml.dom.minidom import Element

import pytest
from pytest import FixtureRequest

from xmlcustomformatter.formatter import XMLCustomFormatter
from xmlcustomformatter.options import Options


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
    def xml_files(tmp_path: Path, elements: tuple[str, bool]) -> tuple[str, str]:
        """Writes the XML content to a temp file and returns the path as a string."""
        xml_content, _ = elements
        input_path = tmp_path / "input.xml"
        output_path = tmp_path / "output.xml"
        input_path.write_text(xml_content)
        return str(input_path), str(output_path)

    @staticmethod
    def test_is_empty_element(xml_files: tuple[str, str], elements: tuple[str, bool]) -> None:
        """Tests that empty and non-empty elements are classified correctly."""
        _, expected = elements
        input_file, output_file = xml_files
        formatter = XMLCustomFormatter(input_file, output_file)
        if isinstance(formatter._dom.documentElement, Element):
            assert formatter._is_empty_element(formatter._dom.documentElement) == expected

    @staticmethod
    def test_is_inline_element(xml_files: tuple[str, str]) -> None:
        """Tests that a certain element is inline."""
        input_file, output_file = xml_files
        element = Element("foo")
        options = Options(inline_elements=("foo",))
        formatter = XMLCustomFormatter(input_file, output_file, options)
        assert formatter._is_inline_element(element)

    @staticmethod
    def test_is_not_inline_element(xml_files: tuple[str, str]) -> None:
        """Tests that a certain element is not inline"""
        input_file, output_file = xml_files
        element = Element("foo")
        options = Options(inline_elements=("bar",))
        formatter = XMLCustomFormatter(input_file, output_file, options)
        assert not formatter._is_inline_element(element)

    @staticmethod
    def test_inline_element(tmp_path: Path) -> None:
        """Tests the formatting of a certain inline element."""
        xml_content = "<root>foo</root>"
        expected = """<?xml version="1.0" encoding="UTF-8"?>\n<root>foo</root>"""
        options = Options(inline_elements=("root",))
        input_path = tmp_path / "input.xml"
        output_path = tmp_path / "output.xml"
        input_path.write_text(xml_content)
        formatter = XMLCustomFormatter(str(input_path), str(output_path), options)
        result = Path(formatter.output_file).read_text(encoding="UTF-8")
        assert result == expected

    @staticmethod
    def test_semicontainer_element(tmp_path: Path) -> None:
        """Tests the formatting of a semicontainer element."""
        xml_content = "<root>foo</root>"
        options = Options(semicontainer_elements=("root",))
        input_path = tmp_path / "input.xml"
        output_path = tmp_path / "output.xml"
        input_path.write_text(xml_content)
        with pytest.raises(NotImplementedError):
            XMLCustomFormatter(str(input_path), str(output_path), options)

    @staticmethod
    def test_empty_semicontainer_element(tmp_path: Path) -> None:
        """Tests the formatting of a semicontainer element."""
        xml_content = "<root/>"
        options = Options(semicontainer_elements=("root",))
        input_path = tmp_path / "input.xml"
        output_path = tmp_path / "output.xml"
        input_path.write_text(xml_content)
        with pytest.raises(NotImplementedError):
            XMLCustomFormatter(str(input_path), str(output_path), options)

    @staticmethod
    def test_default_element(tmp_path: Path) -> None:
        """Tests the formatting of a default element."""
        xml_content = "<root>foo</root>"
        expected = """<?xml version="1.0" encoding="UTF-8"?>\n<root>\n    foo\n</root>\n"""
        input_path = tmp_path / "input.xml"
        output_path = tmp_path / "output.xml"
        input_path.write_text(xml_content)
        formatter = XMLCustomFormatter(str(input_path), str(output_path))
        result = Path(formatter.output_file).read_text(encoding="UTF-8")
        assert result == expected
