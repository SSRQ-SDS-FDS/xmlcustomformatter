"""This class contains various other tests."""

from xml.dom.minidom import Node
from pathlib import Path

import pytest

from xmlcustomformatter.formatter import XMLCustomFormatter


class TestXMLCustomFormatterOther:
    """This class contains various other tests."""

    @staticmethod
    @pytest.fixture
    def xml_dummy(tmp_path: Path) -> XMLCustomFormatter:
        """Yields an instance of the XMLCustomFormatter class."""
        xml = "<root/>"
        file_path = tmp_path / "input.xml"
        file_path.write_text(xml, encoding="UTF-8")
        return XMLCustomFormatter(str(file_path), "output.xml")

    @staticmethod
    def test_get_result_as_list(xml_dummy: XMLCustomFormatter) -> None:
        """Tests the result as a list of strings."""
        expected = ['<?xml version="1.0" encoding="UTF-8"?>', "<root", "/>"]
        assert xml_dummy.get_result_as_list() == expected

    @staticmethod
    def test_get_result_as_string(xml_dummy: XMLCustomFormatter) -> None:
        """Tests the result as a string."""
        expected = """<?xml version="1.0" encoding="UTF-8"?><root/>"""
        assert xml_dummy.get_result_as_string() == expected

    @staticmethod
    def test_xml_wrong_node(xml_dummy: XMLCustomFormatter) -> None:
        """Tests that an unhandled node type raises an exception."""
        with pytest.raises(TypeError):
            xml_dummy._process_node(Node())
