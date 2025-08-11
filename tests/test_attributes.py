"""This module tests the processing of attributes."""

from pathlib import Path

import pytest

from xmlcustomformatter.formatter import XMLCustomFormatter
from xmlcustomformatter.options import Options


class TestXMLCustomFormatterAttribute:
    """This class tests the processing of attributes."""

    @pytest.mark.parametrize(
        "xml_content, expected",
        [
            (
                """<root a="b"/>""",
                """<?xml version="1.0" encoding="UTF-8"?><root a="b"/>""",
            ),
            (
                """<root a="b" b="c"/>""",
                """<?xml version="1.0" encoding="UTF-8"?><root a="b" b="c"/>""",
            ),
            (
                """<root a='b'/>""",
                """<?xml version="1.0" encoding="UTF-8"?><root a="b"/>""",
            ),
            (
                """<root a="'b'"/>""",
                """<?xml version="1.0" encoding="UTF-8"?><root a="'b'"/>""",
            ),
            (
                """<root a='"b"'/>""",
                """<?xml version="1.0" encoding="UTF-8"?><root a="&quot;b&quot;"/>""",
            ),
        ],
        ids=[
            "one_attribute",
            "two_attributes",
            "attribute_with_single_quotes",
            "attribute_with_single_quotes_inside_double_quotes",
            "attribute_with_double_quotes_inside_single_quotes",
        ],
    )
    def test_attributes(self, tmp_path: Path, xml_content: str, expected: str) -> None:
        """Tests that attributes are processed correctly."""
        file_path = tmp_path / "input.xml"
        file_path.write_text(xml_content)
        formatter = XMLCustomFormatter(str(file_path), "output.xml")
        assert "".join(formatter._result) == expected

    @pytest.mark.parametrize(
        "xml_content, expected, options",
        [
            (
                """<root b="c" a="b"/>""",
                """<?xml version="1.0" encoding="UTF-8"?><root a="b" b="c"/>""",
                Options(sorted_attributes=True),
            ),
            (
                """<root b="c" a="b"/>""",
                """<?xml version="1.0" encoding="UTF-8"?><root b="c" a="b"/>""",
                Options(sorted_attributes=False),
            ),
        ],
        ids=[
            "two_attributes_ordered_alphabetical",
            "two_attributes_not_ordered_alphabetical",
        ],
    )
    def test_attribute_ordering(
        self, tmp_path: Path, xml_content: str, expected: str, options: Options
    ) -> None:
        """Tests the ordering of attributes"""
        file_path = tmp_path / "input.xml"
        file_path.write_text(xml_content)
        formatter = XMLCustomFormatter(str(file_path), "output.xml", options)
        assert "".join(formatter._result) == expected
