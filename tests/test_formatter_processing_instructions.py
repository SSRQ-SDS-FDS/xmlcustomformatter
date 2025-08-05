from typing import cast

import pytest

from pytest import FixtureRequest
from pathlib import Path

from xmlcustomformatter.formatter import XMLCustomFormatter
from xmlcustomformatter.options import Options


class TestXMLCustomFormatterProcessingInstructions:
    @pytest.fixture(
        params=[
            (
                "pi_before_root",
                """<?foo bar?><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<?foo bar?>\n""",
                Options(),
            ),
            (
                "pi_after_declaration",
                """<?xml version="1.0"?><?foo bar?><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<?foo bar?>\n""",
                Options(),
            ),
            (  # ToDo: Yet to implement when elements are being processes
                "pi_inside_element",
                """<root><?foo bar?></root>""",
                """<?xml version="1.0" encoding="UTF-8"?>""",
                Options(),
            ),
            (
                "pi_after_root",
                """<root/><?foo bar?>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<?foo bar?>\n""",
                Options(),
            ),
            (
                "pi_with_line_breaks_spaces",
                """<?foo bar\n   baz\n  bat?><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<?foo bar baz bat?>\n""",
                Options(),
            ),
            (
                "pi_with_normalized_spaces",
                """<?foo  \n bar \n  ?><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<?foo bar?>\n""",
                Options(),
            ),
            (
                "pis_don't_start_newlines",
                """<?foo bar?><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?><?foo bar?>""",
                Options(processing_instructions_start_new_lines=False),
            ),
        ]
    )
    def pis(self, request: FixtureRequest) -> tuple[str, str, str, Options]:
        """Yields tets_name, xml_content, expected_result"""
        return cast(tuple[str, str, str, Options], request.param)

    @pytest.fixture
    def xml_file(self, tmp_path: Path, pis: tuple[str, str, str, Options]) -> str:
        """Writes the XML content to a temp file and returns the path as a string."""
        _, xml_content, _, _ = pis
        file_path = tmp_path / "input.xml"
        file_path.write_text(xml_content)
        return str(file_path)

    def test_xml_pi(self, pis: tuple[str, str, str, Options], xml_file: str) -> None:
        """Checks that comment nodes are formatted correctly."""
        test_name, _, expected, options = pis
        formatter = XMLCustomFormatter(xml_file, "output.xml", options)
        assert "".join(formatter._result) == expected
