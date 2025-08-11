"""This module tests the processing of comments."""

from pathlib import Path
from typing import cast

import pytest

from pytest import FixtureRequest

from xmlcustomformatter.formatter import XMLCustomFormatter
from xmlcustomformatter.options import Options


class TestXMLCustomFormatterComments:
    """This class tests the processing of comments."""

    @staticmethod
    @pytest.fixture(
        params=[
            (
                """<!--Foo--><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!-- Foo -->\n<root/>""",
                Options(),
            ),
            (
                """<?xml version="1.0"?><!--Foo--><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!-- Foo -->\n<root/>""",
                Options(),
            ),
            (
                """<root><!--Foo--></root>""",
                """<?xml version="1.0" encoding="UTF-8"?><root>\n<!-- Foo -->\n</root>""",
                Options(),
            ),
            (
                """<root/><!--Foo-->""",
                """<?xml version="1.0" encoding="UTF-8"?><root/>\n<!-- Foo -->\n""",
                Options(),
            ),
            (
                """<!--  Foo  --><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!-- Foo -->\n<root/>""",
                Options(),
            ),
            (
                """<!--\nFoo\n--><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!-- Foo -->\n<root/>""",
                Options(),
            ),
            (
                """<!--  Foo  \n Bar  --><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!-- Foo Bar -->\n<root/>""",
                Options(),
            ),
            (
                """<!--  Foo  \n Bar  --><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!--Foo Bar-->\n<root/>""",
                Options(comments_have_trailing_spaces=False),
            ),
            (
                """<!--  Foo  Bar  --><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?><!--Foo Bar--><root/>""",
                Options(comments_have_trailing_spaces=False, comments_start_new_lines=False),
            ),
        ],
        ids=[
            "comment_before_root",
            "comment_after_declaration",
            "comment_inside_element",
            "comment_after_root",
            "comment_with_trailing_spaces",
            "comment_with_line_breaks_spaces",
            "comment_with_normalized_spaces",
            "comment_with_normalized_spaces_no_trailing_spaces",
            "comments_don't_start_newlines",
        ],
    )
    def comments(request: FixtureRequest) -> tuple[str, str, Options]:
        """Yields xml_content, expected_result and an Options object"""
        return cast(tuple[str, str, Options], request.param)

    @staticmethod
    @pytest.fixture
    def xml_file(tmp_path: Path, comments: tuple[str, str, Options]) -> str:
        """Writes the XML content to a temp file and returns the path as a string."""
        xml_content, _, _ = comments
        file_path = tmp_path / "input.xml"
        file_path.write_text(xml_content)
        return str(file_path)

    @staticmethod
    def test_xml_comment(comments: tuple[str, str, Options], xml_file: str) -> None:
        """Checks that comment nodes are formatted correctly."""
        _, expected, options = comments
        formatter = XMLCustomFormatter(xml_file, "output.xml", options)
        assert formatter.get_result_as_string() == expected
