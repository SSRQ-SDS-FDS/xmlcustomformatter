"""This module contains tests for the XML parsing."""

from pathlib import Path

import pytest

from xmlcustomformatter.formatter import XMLCustomFormatter


class TestXMLCustomFormatterParsing:
    """This class tests the parsing behaviour of the XMLCustomFormatter"""

    @staticmethod
    def test_parsing_from_wellformed_string() -> None:
        """Tests that a wellformed input string is parsed correctly."""
        input_xml = "<root/>"
        assert isinstance(XMLCustomFormatter(input_xml), XMLCustomFormatter)

    @staticmethod
    def test_parsing_from_not_wellformed_string() -> None:
        """Tests that a not wellformed input string raises an exception."""
        input_xml = "<root>"
        with pytest.raises(ValueError):
            XMLCustomFormatter(input_xml)

    @staticmethod
    def test_parsing_from_very_large_input_string() -> None:
        """Tests that a very large input string is parsed correctly."""
        input_xml = Path("tests/example_files/SSRQ-SG-III_4-24_unformatiert.xml").read_text(
            encoding="utf-8"
        )
        assert isinstance(XMLCustomFormatter(input_xml), XMLCustomFormatter)

    @staticmethod
    def test_parsing_from_wellformed_file(tmp_path: Path) -> None:
        """Tests that a wellformed input file is parsed correctly."""
        file = tmp_path / "test.xml"
        file.write_text("<root/>", encoding="utf-8")
        assert isinstance(XMLCustomFormatter(str(file)), XMLCustomFormatter)

    @staticmethod
    def test_parsing_from_not_wellformed_file(tmp_path: Path) -> None:
        """Tests that a not wellformed input file raises an exception."""
        file = tmp_path / "test.xml"
        file.write_text("<root>", encoding="utf-8")
        with pytest.raises(ValueError):
            XMLCustomFormatter(str(file))
