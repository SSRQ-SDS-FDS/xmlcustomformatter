from typing import cast
from xml.dom.minidom import (
    Element,
    Attr,
    CDATASection,
    Comment,
    Document,
    DocumentFragment,
    DocumentType,
    Entity,
    Notation,
    ProcessingInstruction,
    Text,
)

import pytest
from pytest import FixtureRequest
from pathlib import Path
from xmlcustomformatter.formatter import XMLCustomFormatter


class TestXMLCustomFormatterFormatting:
    # Kombinierte Inhalte
    @pytest.fixture(
        params=[
            (
                "no_declaration",
                "utf-8",
                """<root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>""",
            ),
            (
                "version_1_0",
                "utf-8",
                """<?xml version="1.0"?><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>""",
            ),
            (
                "version_1_0_with_space",
                "utf-8",
                """<?xml version="1.0" ?><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>""",
            ),
            (
                "version_1_1",
                "utf-8",
                """<?xml version="1.1"?><root/>""",
                """<?xml version="1.1" encoding="UTF-8"?>""",
            ),
            (
                "encoding_utf_8",
                "utf-8",
                """<?xml version="1.0" encoding="UTF-8"?><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>""",
            ),
            (
                "encoding_iso_8859_1",
                "iso-8859-1",
                """<?xml version="1.0" encoding="ISO-8859-1"?><root/>""",
                """<?xml version="1.0" encoding="ISO-8859-1"?>""",
            ),
            (
                "standalone_yes",
                "utf-8",
                """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><root/>""",
                """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>""",
            ),
            (
                "standalone_no",
                "utf-8",
                """<?xml version="1.0" encoding="UTF-8" standalone="no"?><root/>""",
                """<?xml version="1.0" encoding="UTF-8" standalone="no"?>""",
            ),
        ]
    )
    def xml_declarations(self, request: FixtureRequest) -> tuple[str, str, str, str]:
        """Yields test_name, encoding, XML declaration, expected_result"""
        return cast(tuple[str, str, str, str], request.param)

    @pytest.fixture
    def xml_file(self, tmp_path: Path, xml_declarations: tuple[str, str, str, str]) -> str:
        """Writes the XML content to a temp file and returns the path as a string."""
        _, encoding, xml_content, _ = xml_declarations
        file_path = tmp_path / "input.xml"
        file_path.write_text(xml_content, encoding=encoding)
        return str(file_path)

    def test_xml_declaration(
        self, xml_declarations: tuple[str, str, str, str], xml_file: str
    ) -> None:
        test_name, _, _, expected = xml_declarations
        formatter = XMLCustomFormatter(xml_file, "output.xml")
        assert formatter._result[0] == expected

    @pytest.fixture
    def xml_dummy(self, tmp_path: Path) -> XMLCustomFormatter:
        xml = "<root/>"
        file_path = tmp_path / "input.xml"
        file_path.write_text(xml, encoding="UTF-8")
        return XMLCustomFormatter(str(file_path), "output.xml")

    def test_xml_attribute(self, xml_dummy: XMLCustomFormatter) -> None:
        with pytest.raises(NotImplementedError):
            xml_dummy._process_node(Attr("foo"))

    def test_xml_cdata_section(self, xml_dummy: XMLCustomFormatter) -> None:
        with pytest.raises(NotImplementedError):
            xml_dummy._process_node(CDATASection())

    def test_xml_comment(self, xml_dummy: XMLCustomFormatter) -> None:
        with pytest.raises(NotImplementedError):
            xml_dummy._process_node(Comment(""))

    def test_xml_document(self, xml_dummy: XMLCustomFormatter) -> None:
        xml_dummy._process_node(Document())

    def test_xml_document_fragment(self, xml_dummy: XMLCustomFormatter) -> None:
        with pytest.raises(NotImplementedError):
            xml_dummy._process_node(DocumentFragment())

    def test_xml_document_type(self, xml_dummy: XMLCustomFormatter) -> None:
        with pytest.raises(NotImplementedError):
            xml_dummy._process_node(DocumentType("foo"))

    def test_xml_element(self, xml_dummy: XMLCustomFormatter) -> None:
        with pytest.raises(NotImplementedError):
            xml_dummy._process_node(Element("tag"))

    def test_xml_entity(self, xml_dummy: XMLCustomFormatter) -> None:
        with pytest.raises(NotImplementedError):
            xml_dummy._process_node(Entity("name", "foo", "bar", "baz"))

    def test_xml_notation(self, xml_dummy: XMLCustomFormatter) -> None:
        with pytest.raises(NotImplementedError):
            xml_dummy._process_node(Notation("name", "foo", "bar"))

    def test_xml_processing_instruction(self, xml_dummy: XMLCustomFormatter) -> None:
        with pytest.raises(NotImplementedError):
            xml_dummy._process_node(ProcessingInstruction("target", "data"))

    def test_xml_text(self, xml_dummy: XMLCustomFormatter) -> None:
        with pytest.raises(NotImplementedError):
            xml_dummy._process_node(Text())
