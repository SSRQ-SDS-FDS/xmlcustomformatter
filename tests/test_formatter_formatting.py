from typing import cast

import pytest
from pytest import FixtureRequest
from pathlib import Path
from xmlcustomformatter.formatter import XMLCustomFormatter


class TestXMLCustomFormatterFormatting:
    # Kombinierte Inhalte
    @pytest.fixture(
        params=[
            (
                "no_declaration",
                "utf-8",
                """<root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>""",
            ),
            (
                "version_1_0",
                "utf-8",
                """<?xml version="1.0"?><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>""",
            ),
            (
                "version_1_0_with_space",
                "utf-8",
                """<?xml version="1.0" ?><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>""",
            ),
            (
                "version_1_1",
                "utf-8",
                """<?xml version="1.1"?><root/>""",
                """<?xml version="1.1" encoding="UTF-8"?>""",
            ),
            (
                "encoding_utf_8",
                "utf-8",
                """<?xml version="1.0" encoding="UTF-8"?><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>""",
            ),
            (
                "encoding_iso_8859_1",
                "iso-8859-1",
                """<?xml version="1.0" encoding="ISO-8859-1"?><root/>""",
                """<?xml version="1.0" encoding="ISO-8859-1"?>""",
            ),
            (
                "standalone_yes",
                "utf-8",
                """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><root/>""",
                """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>""",
            ),
            (
                "standalone_no",
                "utf-8",
                """<?xml version="1.0" encoding="UTF-8" standalone="no"?><root/>""",
                """<?xml version="1.0" encoding="UTF-8" standalone="no"?>""",
            ),
        ]
    )
    def xml_test_case(self, request: FixtureRequest) -> tuple[str, str, str, str]:
        """Yields test_name, encoding, xml_content, expected_result"""
        return cast(tuple[str, str, str, str], request.param)

    @pytest.fixture
    def xml_file(self, tmp_path: Path, xml_test_case: tuple[str, str, str, str]) -> str:
        """Writes the XML content to a temp file and returns the path as a string."""
        _, encoding, xml_content, _ = xml_test_case
        file_path = tmp_path / "input.xml"
        file_path.write_text(xml_content, encoding=encoding)
        return str(file_path)

    def test_xml_declaration(
        self, xml_test_case: tuple[str, str, str, str], xml_file: str
    ) -> None:
        test_name, _, _, expected = xml_test_case
        formatter = XMLCustomFormatter(xml_file, "output.xml")
        assert formatter._result[0] == expected
