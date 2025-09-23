"""This module tests the functionality of the StringManipulation class."""

import pytest

from xmlcustomformatter.stringmanipulation import StringManipulation


class TestStringManipulation:
    """This class tests the functionality of the StringManipulation class."""

    @staticmethod
    @pytest.mark.parametrize(
        "input_string, expected",
        [
            ([" a", "b c", "d"], " a\nb c\nd"),
            ([], ""),
            (["single"], "single"),
        ],
        ids=["list of strings", "empty-list", "list of string"],
    )
    def test_convert_list_to_string(input_string: list[str], expected: str) -> None:
        """Tests conversion of a list of strings into a single newline-separated string."""
        result = StringManipulation.convert_list_to_string(input_string)
        assert result == expected

    @staticmethod
    @pytest.mark.parametrize(
        "input_string, expected",
        [
            ("Hello   World", "Hello World"),
            ("Tabs\tand\nNewlines\n\n", "Tabs and Newlines "),
            (" No  extra   spaces ", " No extra spaces "),
            ("Multiple \n\n\n Lines", "Multiple Lines"),
        ],
        ids=["multiple spaces", "tags", "trailing spaces", "linebreaks"],
    )
    def test_reduce_redundant_whitespace(input_string: str, expected: str) -> None:
        """
        Tests removal of redundant whitespace by collapsing multiple spaces
        or tabs into single spaces.
        """
        result = StringManipulation.reduce_redundant_whitespace(input_string)
        assert result == expected

    @staticmethod
    @pytest.mark.parametrize(
        "input_string, expected",
        [
            ("Line1\nLine2", "Line1\nLine2"),
            ("Line1\n\nLine2", "Line1\nLine2"),
            ("One\n\n\nTwo", "One\nTwo"),
            ("NoEmptyLines", "NoEmptyLines"),
            ("\n\n\nStart with empty lines", "\nStart with empty lines"),
        ],
        ids=[
            "one line break",
            "two line breaks",
            "three line breaks",
            "no line breaks",
            "leading line breaks",
        ],
    )
    def test_remove_empty_lines(input_string: str, expected: str) -> None:
        """Tests removal of consecutive empty lines by reducing them to a single newline."""
        result = StringManipulation.remove_empty_lines(input_string)
        assert result == expected

    @staticmethod
    @pytest.mark.parametrize(
        "input_string, expected",
        [
            ("Remove spaces", "Removespaces"),
            ("  Leading and trailing  ", "Leadingandtrailing"),
            ("Tabs\tand\nNewlines\n", "Tabs\tand\nNewlines\n"),
            ("NoSpaces", "NoSpaces"),
        ],
        ids=["spaces in between", "leading and trailing spaces", "tabs and newlines", "no spaces"],
    )
    def test_remove_whitespace(input_string: str, expected: str) -> None:
        """
        Tests removal of all whitespace characters from the input string
        except tabs and newline characters.
        """
        result = StringManipulation.remove_whitespace(input_string)
        assert result == expected

    @staticmethod
    @pytest.mark.parametrize(
        "input_string, expected",
        [
            ("Text  \nNext line", "Text\nNext line"),
            ("Text  \t\nNext line", "Text\nNext line"),
            ("Text\nNext line", "Text\nNext line"),
            ("Text\n Next line", "Text\n Next line"),
        ],
        ids=["whitespace", "tabs", "no space before", "space after"],
    )
    def test_remove_whitespace_before_end_of_line(input_string: str, expected: str) -> None:
        """Tests removal of trailing whitespace that occurs just before a newline character."""
        result = StringManipulation.remove_whitespace_before_eol(input_string)
        assert result == expected

    @staticmethod
    @pytest.mark.parametrize(
        "input_string, expected",
        [
            ("Text text text", "Text text text"),
            ("Text 'text' text", "Text &apos;text&apos; text"),
            ('Text "text" text', "Text &quot;text&quot; text"),
            ("Text & text", "Text &amp; text"),
            ("Text < text", "Text &lt; text"),
            ("Text > text", "Text &gt; text"),
        ],
        ids=["no quotes", "single quotes", "double quotes", "ampersand", "lt", "gt"],
    )
    def test_escape_xml_entities(input_string: str, expected: str) -> None:
        """Tests escaping of entities."""
        result = StringManipulation.escape_xml_entities(input_string)
        assert result == expected
