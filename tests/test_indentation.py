"""This module tests the indentation functionality in the XMLCustomFormatter class."""

from pathlib import Path

import pytest

from xmlcustomformatter.formatter import XMLCustomFormatter


class TestXMLCustomFormatterIndentation:
    """This class tests the indentation functionality in the XMLCustomFormatter class."""

    @staticmethod
    @pytest.fixture
    def xml_content() -> str:
        """Returns XML content as a string."""
        return """<?xml version="1.0" encoding="UTF-8"?><root/>"""

    @staticmethod
    @pytest.fixture
    def xml_files(tmp_path: Path, xml_content: str) -> tuple[str, str]:
        """Returns file paths as a tuple of strings."""
        input_path = tmp_path / "input.xml"
        output_path = tmp_path / "output.xml"
        input_path.write_text(xml_content, encoding="utf-8")
        return str(input_path), str(output_path)

    @staticmethod
    def test_increase_indentation(xml_files: tuple[str, str]) -> None:
        """Tests that the indentation is increased correctly."""
        input_file, output_file = xml_files
        formatter = XMLCustomFormatter(input_file, output_file)
        formatter._increase_indentation_level()
        assert formatter._indentation_level == 1

    @staticmethod
    def test_increase_indentation_multiple_times(xml_files: tuple[str, str]) -> None:
        """Tests that the indentation is increased correctly."""
        input_file, output_file = xml_files
        formatter = XMLCustomFormatter(input_file, output_file)
        formatter._increase_indentation_level()
        formatter._increase_indentation_level()
        assert formatter._indentation_level == 2

    @staticmethod
    def test_decrease_indentation_below_zero(xml_files: tuple[str, str]) -> None:
        """Tests that the indentation cannot decrease below zero."""
        input_file, output_file = xml_files
        formatter = XMLCustomFormatter(input_file, output_file)
        with pytest.raises(ValueError):
            formatter._decrease_indentation_level()

    @staticmethod
    def test_decrease_indentation_correctly(xml_files: tuple[str, str]) -> None:
        """Tests that the indentation is increased correctly."""
        input_file, output_file = xml_files
        formatter = XMLCustomFormatter(input_file, output_file)
        formatter._increase_indentation_level()
        formatter._decrease_indentation_level()
        assert formatter._indentation_level == 0

    @staticmethod
    def test_decrease_indentation_multiple_times(xml_files: tuple[str, str]) -> None:
        """Tests that the indentation is increased correctly."""
        input_file, output_file = xml_files
        formatter = XMLCustomFormatter(input_file, output_file)
        formatter._increase_indentation_level()
        formatter._increase_indentation_level()
        formatter._decrease_indentation_level()
        formatter._decrease_indentation_level()
        assert formatter._indentation_level == 0

    @staticmethod
    def test_calculate_indentation_at_start(xml_files: tuple[str, str]) -> None:
        """Tests that the calculation of the indentation is correct."""
        input_file, output_file = xml_files
        formatter = XMLCustomFormatter(input_file, output_file)
        assert formatter._calculate_indentation() == 0

    @staticmethod
    def test_calculate_indentation_after_increasing(xml_files: tuple[str, str]) -> None:
        """Tests that the calculation of the indentation is correct."""
        input_file, output_file = xml_files
        formatter = XMLCustomFormatter(input_file, output_file)
        formatter._increase_indentation_level()
        assert formatter._calculate_indentation() == formatter.options.indentation

    @staticmethod
    def test_calculate_indentation_after_decreasing(xml_files: tuple[str, str]) -> None:
        """Tests that the calculation of the indentation is correct."""
        input_file, output_file = xml_files
        formatter = XMLCustomFormatter(input_file, output_file)
        formatter._increase_indentation_level()
        formatter._decrease_indentation_level()
        assert formatter._calculate_indentation() == 0

    @staticmethod
    @pytest.mark.parametrize(
        "count, expected",
        [
            (0, ""),
            (4, "    "),
            (8, "        "),
        ],
        ids=["zero-indentation", "four-spaces", "eight-spaces"],
    )
    def test_indentation_(xml_files: tuple[str, str], count: int, expected: str) -> None:
        """Tests that the indentation is returned correctly."""
        input_file, output_file = xml_files
        formatter = XMLCustomFormatter(input_file, output_file)
        assert formatter._indentation(count) == expected

    @staticmethod
    def test_negative_indentation_(xml_files: tuple[str, str]) -> None:
        """Tests that negative indentation raises a ValueError."""
        input_file, output_file = xml_files
        formatter = XMLCustomFormatter(input_file, output_file)
        with pytest.raises(ValueError):
            formatter._indentation(-1)
