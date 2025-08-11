"""This module tests the processing of processing instructions."""

from pathlib import Path
from typing import cast

import pytest

from pytest import FixtureRequest

from xmlcustomformatter.formatter import XMLCustomFormatter
from xmlcustomformatter.options import Options


class TestXMLCustomFormatterProcessingInstructions:
    """This class tests processing of processing instructions."""

    @staticmethod
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
    def pis(request: FixtureRequest) -> tuple[str, str, Options]:
        """Yields xml_content, expected_result"""
        return cast(tuple[str, str, Options], request.param)

    @staticmethod
    @pytest.fixture
    def xml_files(tmp_path: Path, pis: tuple[str, str, Options]) -> tuple[str, str]:
        """Writes the XML content to a temp file and returns the path as a string."""
        xml_content, _, _ = pis
        input_path = tmp_path / "input.xml"
        output_path = tmp_path / "output.xml"
        input_path.write_text(xml_content)
        return str(input_path), str(output_path)

    @staticmethod
    def test_xml_pi(pis: tuple[str, str, Options], xml_files: tuple[str, str]) -> None:
        """Checks that comment nodes are formatted correctly."""
        _, expected, options = pis
        input_file, output_file = xml_files
        formatter = XMLCustomFormatter(input_file, output_file, options)
        assert "".join(formatter._result) == expected
