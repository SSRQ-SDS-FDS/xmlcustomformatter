from pathlib import Path

from xmlcustomformatter.formatter import XMLCustomFormatter

import pytest


class TestXMLCustomFormatterIndentation:
    """Unit tests for the indentation functionality in the XMLCustomFormatter class."""

    @pytest.fixture
    def xml_content(self) -> str:
        """Returns XML content as a string"""
        return """<?xml version="1.0" encoding="UTF-8"?><root/>"""

    @pytest.fixture
    def xml_file(self, tmp_path: Path, xml_content: str) -> str:
        """Returns a file path as a string"""
        file_path = tmp_path / "input.xml"
        file_path.write_text(xml_content, encoding="utf-8")
        return str(file_path)

    def test_increase_indentation(self, xml_file: str) -> None:
        """Tests that the indentation is increased correctly."""
        formatter = XMLCustomFormatter(xml_file, "output.xml")
        formatter._increase_indentation_level()
        assert formatter._indentation_level == 1

    def test_increase_indentation_multiple_times(self, xml_file: str) -> None:
        """Tests that the indentation is increased correctly."""
        formatter = XMLCustomFormatter(xml_file, "output.xml")
        formatter._increase_indentation_level()
        formatter._increase_indentation_level()
        assert formatter._indentation_level == 2

    def test_decrease_indentation_below_zero(self, xml_file: str) -> None:
        """Tests that the indentation cannot decrease below zero."""
        formatter = XMLCustomFormatter(xml_file, "output.xml")
        with pytest.raises(ValueError):
            formatter._decrease_indentation_level()

    def test_decrease_indentation_correctly(self, xml_file: str) -> None:
        """Tests that the indentation is increased correctly."""
        formatter = XMLCustomFormatter(xml_file, "output.xml")
        formatter._increase_indentation_level()
        formatter._decrease_indentation_level()
        assert formatter._indentation_level == 0

    def test_decrease_indentation_multiple_times(self, xml_file: str) -> None:
        """Tests that the indentation is increased correctly."""
        formatter = XMLCustomFormatter(xml_file, "output.xml")
        formatter._increase_indentation_level()
        formatter._increase_indentation_level()
        formatter._decrease_indentation_level()
        formatter._decrease_indentation_level()
        assert formatter._indentation_level == 0

    def test_calculate_indentation_at_start(self, xml_file: str) -> None:
        """Tests that the calculation of the indentation is correct."""
        formatter = XMLCustomFormatter(xml_file, "output.xml")
        assert formatter._calculate_indentation() == 0

    def test_calculate_indentation_after_increasing(self, xml_file: str) -> None:
        """Tests that the calculation of the indentation is correct."""
        formatter = XMLCustomFormatter(xml_file, "output.xml")
        formatter._increase_indentation_level()
        assert formatter._calculate_indentation() == formatter.options.indentation

    def test_calculate_indentation_after_decreasing(self, xml_file: str) -> None:
        """Tests that the calculation of the indentation is correct."""
        formatter = XMLCustomFormatter(xml_file, "output.xml")
        formatter._increase_indentation_level()
        formatter._decrease_indentation_level()
        assert formatter._calculate_indentation() == 0

    @pytest.mark.parametrize(
        "count, expected",
        [
            (0, ""),
            (4, "    "),
            (8, "        "),
        ],
    )
    def test_indentation_(self, xml_file: str, count: int, expected: str) -> None:
        """Tests that the indentation is returned correctly."""
        formatter = XMLCustomFormatter(xml_file, "output.xml")
        assert formatter._indentation(count) == expected

    def test_negative_indentation_(self, xml_file: str) -> None:
        """Tests that negative indentation raises a ValueError."""
        formatter = XMLCustomFormatter(xml_file, "output.xml")
        with pytest.raises(ValueError):
            formatter._indentation(-1)
