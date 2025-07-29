import pytest

from xmlcustomformatter.stringmanipulation import StringManipulation


class TestStringManipulation:
    """
    Unit tests for the StringManipulation class.
    """

    @pytest.mark.parametrize(
        "input, expected",
        [
            ([" a", "b c", "d"], " a\nb c\nd"),
            ([], ""),
            (["single"], "single"),
        ],
    )
    def test_convert_list_to_string(self, input: list[str], expected: str) -> None:
        """
        Tests conversion of a list of strings into a single newline-separated string.
        """
        result = StringManipulation.convert_list_to_string(input)
        assert result == expected

    @pytest.mark.parametrize(
        "input, expected",
        [
            ("Hello   World", "Hello World"),
            ("Tabs\tand\nNewlines\n\n", "Tabs and Newlines "),
            (" No  extra   spaces ", " No extra spaces "),
            ("Multiple \n\n\n Lines", "Multiple Lines"),
        ],
    )
    def test_reduce_redundant_whitespace(self, input: str, expected: str) -> None:
        """
        Tests removal of redundant whitespace by collapsing multiple spaces
        or tabs into single spaces.
        """
        result = StringManipulation.reduce_redundant_whitespace(input)
        assert result == expected

    @pytest.mark.parametrize(
        "input, expected",
        [
            ("Line1\nLine2", "Line1\nLine2"),
            ("Line1\n\nLine2", "Line1\nLine2"),
            ("One\n\n\nTwo", "One\nTwo"),
            ("NoEmptyLines", "NoEmptyLines"),
            ("\n\n\nStart with empty lines", "\nStart with empty lines"),
        ],
    )
    def test_remove_empty_lines(self, input: str, expected: str) -> None:
        """
        Tests removal of consecutive empty lines by reducing them to a single newline.
        """
        result = StringManipulation.remove_empty_lines(input)
        assert result == expected

    @pytest.mark.parametrize(
        "input, expected",
        [
            ("Remove spaces", "Removespaces"),
            ("  Leading and trailing  ", "Leadingandtrailing"),
            ("Tabs\tand\nNewlines\n", "Tabs\tand\nNewlines\n"),
            ("NoSpaces", "NoSpaces"),
        ],
    )
    def test_remove_whitespace(self, input: str, expected: str) -> None:
        """
        Tests removal of all whitespace characters from the input string
        except tabs and newline characters.
        """
        result = StringManipulation.remove_whitespace(input)
        assert result == expected

    @pytest.mark.parametrize(
        "input, expected",
        [
            ("Text  \nNext line", "Text\nNext line"),
            ("Text  \t\nNext line", "Text\nNext line"),
            ("Text\nNext line", "Text\nNext line"),
            ("Text\n Next line", "Text\n Next line"),
        ],
    )
    def test_remove_whitespace_before_end_of_line(self, input: str, expected: str) -> None:
        """
        Tests removal of trailing whitespace that occurs just before a newline character.
        """
        result = StringManipulation.remove_whitespace_before_eol(input)
        assert result == expected
