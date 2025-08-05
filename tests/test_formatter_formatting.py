from xml.dom.minidom import (
    Attr,
    CDATASection,
    Document,
    DocumentFragment,
    DocumentType,
    Entity,
    Notation,
    ProcessingInstruction,
    Text,
    Node,
)

import pytest
from pathlib import Path
from xmlcustomformatter.formatter import XMLCustomFormatter


class TestXMLCustomFormatterFormatting:
    @pytest.fixture
    def xml_dummy(self, tmp_path: Path) -> XMLCustomFormatter:
        """Yields an instance of the XMLCustomFormatter class."""
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

    def test_xml_document(self, xml_dummy: XMLCustomFormatter) -> None:
        xml_dummy._process_node(Document())

    def test_xml_document_fragment(self, xml_dummy: XMLCustomFormatter) -> None:
        with pytest.raises(NotImplementedError):
            xml_dummy._process_node(DocumentFragment())

    def test_xml_document_type(self, xml_dummy: XMLCustomFormatter) -> None:
        with pytest.raises(NotImplementedError):
            xml_dummy._process_node(DocumentType("foo"))

    def test_xml_element(self, xml_dummy: XMLCustomFormatter) -> None:
        # ToDo: Fill with life
        assert True

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

    def test_xml_wrong_node(self, xml_dummy: XMLCustomFormatter) -> None:
        """Tests that an unhandled node type raises an exception."""
        with pytest.raises(TypeError):
            xml_dummy._process_node(Node())
