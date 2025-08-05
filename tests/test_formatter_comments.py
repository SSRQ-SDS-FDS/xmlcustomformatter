from typing import cast

import pytest

from pytest import FixtureRequest
from pathlib import Path

from xmlcustomformatter.formatter import XMLCustomFormatter
from xmlcustomformatter.options import Options


class TestXMLCustomFormatterComments:
    @pytest.fixture(
        params=[
            (
                "comment_before_root",
                """<!--Foo--><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!-- Foo -->""",
                Options(),
            ),
            (
                "comment_after_declaration",
                """<?xml version="1.0"?><!--Foo--><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!-- Foo -->""",
                Options(),
            ),
            (  # ToDo: Yet to implement when elements are being processes
                "comment_inside_element",
                """<root><!--Foo--></root>""",
                """<?xml version="1.0" encoding="UTF-8"?>""",
                Options(),
            ),
            (
                "comment_after_root",
                """<root/><!--Foo-->""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!-- Foo -->""",
                Options(),
            ),
            (
                "comment_with_trailing_spaces",
                """<!--  Foo  --><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!-- Foo -->""",
                Options(),
            ),
            (
                "comment_with_line_breaks_spaces",
                """<!--\nFoo\n--><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!-- Foo -->""",
                Options(),
            ),
            (
                "comment_with_normalized_spaces",
                """<!--  Foo  \n Bar  --><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!-- Foo Bar -->""",
                Options(),
            ),
            (
                "comment_with_normalized_spaces_no_trailing_spaces",
                """<!--  Foo  \n Bar  --><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!--Foo Bar-->""",
                Options(comments_have_trailing_spaces=False),
            ),
            (
                "comments_don't_start_newlines",
                """<!--  Foo  Bar  --><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?><!--Foo Bar-->""",
                Options(comments_have_trailing_spaces=False, comments_start_new_lines=False),
            ),
        ]
    )
    def comments(self, request: FixtureRequest) -> tuple[str, str, str, Options]:
        """Yields tets_name, xml_content, expected_result"""
        return cast(tuple[str, str, str, Options], request.param)

    @pytest.fixture
    def xml_file(self, tmp_path: Path, comments: tuple[str, str, str, Options]) -> str:
        """Writes the XML content to a temp file and returns the path as a string."""
        _, xml_content, _, _ = comments
        file_path = tmp_path / "input.xml"
        file_path.write_text(xml_content)
        return str(file_path)

    def test_xml_comment(self, comments: tuple[str, str, str, Options], xml_file: str) -> None:
        """Tests Comment nodes are formatted correctly."""
        test_name, _, expected, options = comments
        formatter = XMLCustomFormatter(xml_file, "output.xml", options)
        assert "".join(formatter._result) == expected
