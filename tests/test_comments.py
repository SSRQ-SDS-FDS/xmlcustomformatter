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
                Options(inline_elements=("root",)),
            ),
            (
                """<?xml version="1.0"?><!--Foo--><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!-- Foo -->\n<root/>""",
                Options(inline_elements=("root",)),
            ),
            (
                """<root><!--Foo--></root>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root>\n<!-- Foo -->\n</root>""",
                Options(inline_elements=("root",)),
            ),
            (
                """<root/><!--Foo-->""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<root/>\n<!-- Foo -->\n""",
                Options(inline_elements=("root",)),
            ),
            (
                """<!--  Foo  --><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!-- Foo -->\n<root/>""",
                Options(inline_elements=("root",)),
            ),
            (
                """<!--\nFoo\n--><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!-- Foo -->\n<root/>""",
                Options(inline_elements=("root",)),
            ),
            (
                """<!--  Foo  \n Bar  --><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!-- Foo Bar -->\n<root/>""",
                Options(inline_elements=("root",)),
            ),
            (
                """<!--  Foo  \n Bar  --><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!--Foo Bar-->\n<root/>""",
                Options(comments_have_trailing_spaces=False, inline_elements=("root",)),
            ),
            (
                """<!--  Foo  Bar  --><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!--Foo Bar--><root/>""",
                Options(
                    comments_have_trailing_spaces=False,
                    comments_start_new_lines=False,
                    inline_elements=("root",),
                ),
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
    def xml_files(tmp_path: Path, comments: tuple[str, str, Options]) -> tuple[str, str]:
        """Writes the XML content to a temp file and returns the path as a string."""
        xml_content, _, _ = comments
        input_path = tmp_path / "input.xml"
        output_path = tmp_path / "output.xml"
        input_path.write_text(xml_content)
        return str(input_path), str(output_path)

    @staticmethod
    def test_xml_comment(comments: tuple[str, str, Options], xml_files: tuple[str, str]) -> None:
        """Checks that comment nodes are formatted correctly."""
        _, expected, options = comments
        input_file, output_file = xml_files
        formatter = XMLCustomFormatter(input_file, output_file, options)
        assert formatter.get_result_as_string() == expected
