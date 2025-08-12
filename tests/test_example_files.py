"""This module tests the formatting of a complete example file."""

from pathlib import Path

from xmlcustomformatter.formatter import XMLCustomFormatter
from xmlcustomformatter.options import Options


class TestXMLCustomFormatterExampleFile:
    """This class tests the formatting of a complete example file."""

    @staticmethod
    def test_example_file(tmp_path: Path) -> None:
        """Tests whether the formatted file equals the expected file."""
        input_file = "tests/example_files/SSRQ-SG-III_4-24_unformatiert.xml"
        output_file = str(tmp_path / "output.xml")
        expected = Path("tests/example_files/SSRQ-SG-III_4-24_formatted.xml").read_text(
            encoding="UTF-8"
        )
        options = Options()
        XMLCustomFormatter(input_file, output_file, options)
        result = Path(output_file).read_text(encoding="UTF-8")
        assert result == expected
