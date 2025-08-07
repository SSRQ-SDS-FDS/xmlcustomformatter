from xml.dom.minidom import (
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

    def test_xml_wrong_node(self, xml_dummy: XMLCustomFormatter) -> None:
        """Tests that an unhandled node type raises an exception."""
        with pytest.raises(TypeError):
            xml_dummy._process_node(Node())
