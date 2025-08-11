"""This module tests the processing of attributes."""

from pathlib import Path
from typing import cast

import pytest

from pytest import FixtureRequest

from xmlcustomformatter.formatter import XMLCustomFormatter
from xmlcustomformatter.options import Options


class TestXMLCustomFormatterAttribute:
    """This class tests the processing of attributes."""

    @staticmethod
    @pytest.fixture(
        params=[
            (
                """<root a="b"/>""",
                """<?xml version="1.0" encoding="UTF-8"?><root a="b"/>""",
                Options(),
            ),
            (
                """<root a="b" b="c"/>""",
                """<?xml version="1.0" encoding="UTF-8"?><root a="b" b="c"/>""",
                Options(),
            ),
            (
                """<root a='b'/>""",
                """<?xml version="1.0" encoding="UTF-8"?><root a="b"/>""",
                Options(),
            ),
            (
                """<root a="'b'"/>""",
                """<?xml version="1.0" encoding="UTF-8"?><root a="'b'"/>""",
                Options(),
            ),
            (
                """<root a='"b"'/>""",
                """<?xml version="1.0" encoding="UTF-8"?><root a="&quot;b&quot;"/>""",
                Options(),
            ),
            (
                """<root    a="b"   />""",
                """<?xml version="1.0" encoding="UTF-8"?><root a="b"/>""",
                Options(),
            ),
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
            "one_attribute",
            "two_attributes",
            "attribute_with_single_quotes",
            "attribute_with_single_quotes_inside_double_quotes",
            "attribute_with_double_quotes_inside_single_quotes",
            "attribute_with_spaces_around",
            "two_attributes_ordered_alphabetical",
            "two_attributes_not_ordered_alphabetical",
        ],
    )
    def attributes(request: FixtureRequest) -> tuple[str, str, Options]:
        """Yields xml_content, expected result and options."""
        return cast(tuple[str, str, Options], request.param)

    @staticmethod
    @pytest.fixture
    def xml_files(tmp_path: Path, attributes: tuple[str, str, Options]) -> tuple[str, str]:
        """Writes the XML content to a temp file and returns the path as a string."""
        xml_content, _, _ = attributes
        input_path = tmp_path / "input.xml"
        output_path = tmp_path / "output.xml"
        input_path.write_text(xml_content)
        return str(input_path), str(output_path)

    @staticmethod
    def test_attributes(attributes: tuple[str, str, Options], xml_files: tuple[str, str]) -> None:
        """Tests that attributes are processed correctly, including ordering."""
        _, expected, options = attributes
        input_file, output_file = xml_files
        formatter = XMLCustomFormatter(input_file, output_file, options)
        assert formatter.get_result_as_string() == expected
