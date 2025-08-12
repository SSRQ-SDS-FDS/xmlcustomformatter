"""This module tests the processing/construction of XML declarations."""

from pathlib import Path
from typing import cast
import pytest

from pytest import FixtureRequest
from xmlcustomformatter.formatter import XMLCustomFormatter
from xmlcustomformatter.options import Options


class TestXMLCustomFormatterXMLDeclarations:
    """This class tests the processing/construction of XML declarations."""

    @staticmethod
    @pytest.fixture(
        params=[
            (
                "utf-8",
                """<root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root/>""",
                Options(inline_elements=("root",)),
            ),
            (
                "utf-8",
                """<?xml version="1.0"?><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root/>""",
                Options(inline_elements=("root",)),
            ),
            (
                "utf-8",
                """<?xml version="1.0" ?><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root/>""",
                Options(inline_elements=("root",)),
            ),
            (
                "utf-8",
                """<?xml version="1.1"?><root/>""",
                """<?xml version="1.1" encoding="UTF-8"?>\n<root/>""",
                Options(inline_elements=("root",)),
            ),
            (
                "utf-8",
                """<?xml version="1.0" encoding="UTF-8"?><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root/>""",
                Options(inline_elements=("root",)),
            ),
            (
                "iso-8859-1",
                """<?xml version="1.0" encoding="ISO-8859-1"?><root/>""",
                """<?xml version="1.0" encoding="ISO-8859-1"?>\n<root/>""",
                Options(inline_elements=("root",)),
            ),
            (
                "utf-8",
                """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><root/>""",
                """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<root/>""",
                Options(inline_elements=("root",)),
            ),
            (
                "utf-8",
                """<?xml version="1.0" encoding="UTF-8" standalone="no"?><root/>""",
                """<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<root/>""",
                Options(inline_elements=("root",)),
            ),
        ],
        ids=[
            "no_declaration",
            "version_1_0",
            "version_1_0_with_space",
            "version_1_1",
            "encoding_utf_8",
            "encoding_iso_8859_1",
            "standalone_yes",
            "standalone_no",
        ],
    )
    def xml_declarations(request: FixtureRequest) -> tuple[str, str, str, Options]:
        """Yields test_name, encoding, XML declaration, expected_result"""
        return cast(tuple[str, str, str, Options], request.param)

    @staticmethod
    @pytest.fixture
    def xml_files(
        tmp_path: Path, xml_declarations: tuple[str, str, str, Options]
    ) -> tuple[str, str]:
        """Writes the XML content to a temp file and returns the path as a string."""
        encoding, xml_content, _, _ = xml_declarations
        input_path = tmp_path / "input.xml"
        output_path = tmp_path / "output.xml"
        input_path.write_text(xml_content, encoding=encoding)
        return str(input_path), str(output_path)

    @staticmethod
    def test_xml_declaration(
        xml_declarations: tuple[str, str, str, Options], xml_files: tuple[str, str]
    ) -> None:
        """Tests the XML declaration is being constructed correctly."""
        _, _, expected, options = xml_declarations
        input_file, output_file = xml_files
        formatter = XMLCustomFormatter(input_file, output_file, options)
        assert formatter.get_result_as_string() == expected
