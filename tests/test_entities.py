"""This module tests the processing of entities."""

from pathlib import Path
from typing import cast

import pytest
from pytest import FixtureRequest

from xmlcustomformatter.options import Options
from xmlcustomformatter.formatter import XMLCustomFormatter


class TestXMLCustomFormatterEntities:
    """This class tests the processing of elements."""

    @staticmethod
    @pytest.fixture(
        params=[
            (
                """<root>&amp;</root>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root>&amp;</root>""",
            ),
            (
                """<root>&gt;</root>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root>&gt;</root>""",
            ),
            (
                """<root>></root>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root>&gt;</root>""",
            ),
            (
                """<root>&lt;</root>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root>&lt;</root>""",
            ),
            (
                """<root>&apos;</root>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root>&apos;</root>""",
            ),
            (
                """<root>'</root>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root>&apos;</root>""",
            ),
            (
                """<root>&quot;</root>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root>&quot;</root>""",
            ),
            (
                """<root>"</root>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root>&quot;</root>""",
            ),
            (
                """<root a="&amp;"/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root a="&amp;"/>""",
            ),
            (
                """<root a="&gt;"/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root a="&gt;"/>""",
            ),
            (
                """<root a="&lt;"/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root a="&lt;"/>""",
            ),
            (
                """<root a="&apos;"/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root a="&apos;"/>""",
            ),
            (
                """<root a="&quot;"/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root a="&quot;"/>""",
            ),
        ],
        ids=[
            "ampersand_in_text_node",
            "gt_in_text_node",
            "closing_bracket_in_text_node",
            "lt_in_text_node",
            "apos_in_text_node",
            "apostrophe_in_text_node",
            "quot_in_text_node",
            "quotes_in_text_node",
            "ampersand_in_attribute",
            "gt_in_attribute",
            "lt_in_attribute",
            "quot_in_attribute",
            "apos_in_attribute",
        ],
    )
    def entities(request: FixtureRequest) -> tuple[str, str]:
        """Yields xml_content and expected_result."""
        return cast(tuple[str, str], request.param)

    @staticmethod
    @pytest.fixture
    def xml_files(tmp_path: Path, entities: tuple[str, str]) -> tuple[str, str]:
        """Writes the XML content to a temp file and returns the path as a string."""
        xml_content, _ = entities
        input_path = tmp_path / "input.xml"
        output_path = tmp_path / "output.xml"
        input_path.write_text(xml_content)
        return str(input_path), str(output_path)

    @staticmethod
    def test_is_empty_element(xml_files: tuple[str, str], entities: tuple[str, str]) -> None:
        """Tests that entities are resolved correctly."""
        _, expected = entities
        input_file, output_file = xml_files
        options = Options(inline_elements=("root",))
        XMLCustomFormatter(input_file, output_file, options)
        result = Path(output_file).read_text(encoding="UTF-8")
        assert result == expected
