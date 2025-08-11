"""This module tests the processing of processing instructions."""

from pathlib import Path
from typing import cast

import pytest

from pytest import FixtureRequest

from xmlcustomformatter.formatter import XMLCustomFormatter
from xmlcustomformatter.options import Options


class TestXMLCustomFormatterProcessingInstructions:
    """This class tests processing of processing instructions."""

    @pytest.fixture(
        params=[
            (
                """<?foo bar?><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<?foo bar?>\n<root/>""",
                Options(),
            ),
            (
                """<?xml version="1.0"?><?foo bar?><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<?foo bar?>\n<root/>""",
                Options(),
            ),
            (
                """<root><?foo bar?></root>""",
                """<?xml version="1.0" encoding="UTF-8"?><root>\n<?foo bar?>\n</root>""",
                Options(),
            ),
            (
                """<root/><?foo bar?>""",
                """<?xml version="1.0" encoding="UTF-8"?><root/>\n<?foo bar?>\n""",
                Options(),
            ),
            (
                """<?foo bar\n   baz\n  bat?><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<?foo bar baz bat?>\n<root/>""",
                Options(),
            ),
            (
                """<?foo  \n bar \n  ?><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<?foo bar?>\n<root/>""",
                Options(),
            ),
            (
                """<?foo bar?><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?><?foo bar?><root/>""",
                Options(processing_instructions_start_new_lines=False),
            ),
        ],
        ids=[
            "pi_before_root",
            "pi_after_declaration",
            "pi_inside_element",
            "pi_after_root",
            "pi_with_line_breaks_spaces",
            "pi_with_normalized_spaces",
            "pis_don't_start_newlines",
        ],
    )
    def pis(self, request: FixtureRequest) -> tuple[str, str, Options]:
        """Yields xml_content, expected_result"""
        return cast(tuple[str, str, Options], request.param)

    @pytest.fixture
    def xml_file(self, tmp_path: Path, pis: tuple[str, str, Options]) -> str:
        """Writes the XML content to a temp file and returns the path as a string."""
        xml_content, _, _ = pis
        file_path = tmp_path / "input.xml"
        file_path.write_text(xml_content)
        return str(file_path)

    def test_xml_pi(self, pis: tuple[str, str, Options], xml_file: str) -> None:
        """Checks that comment nodes are formatted correctly."""
        _, expected, options = pis
        formatter = XMLCustomFormatter(xml_file, "output.xml", options)
        assert "".join(formatter._result) == expected
