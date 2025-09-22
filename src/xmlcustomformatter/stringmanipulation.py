"""This module contains the utility class StringManipulation."""

import re


class StringManipulation:
    """
    A utility class for common string manipulation tasks such as
    whitespace cleanup, line formatting, and list-to-string conversion.
    """

    EMPTY_LINES: re.Pattern[str] = re.compile(r"\n+")
    WHITESPACES: re.Pattern[str] = re.compile(r"\s+")
    WHITESPACE_EOL: re.Pattern[str] = re.compile(r"\s+\n")

    @classmethod
    def convert_list_to_string(cls, result: list[str]) -> str:
        """
        Joins a list of strings into a single string separated by newlines.

        Args:
            result (list[str]): The list of strings to join.

        Returns:
            str: A single string with elements joined by newline characters.
        """
        return "\n".join(result)

    @classmethod
    def reduce_redundant_whitespace(cls, string: str) -> str:
        """
        Replaces consecutive whitespace characters with a single space.

        Args:
            string (str): The input string containing redundant whitespace.

        Returns:
            str: A string with all whitespace sequences reduced to single spaces.
        """
        return cls.WHITESPACES.sub(" ", string)

    @classmethod
    def remove_empty_lines(cls, string: str) -> str:
        """
        Removes consecutive empty lines by collapsing multiple newlines into one.

        Args:
            string (str): The input string potentially containing empty lines.

        Returns:
            str: A string with redundant empty lines removed.
        """
        return cls.EMPTY_LINES.sub("\n", string)

    @classmethod
    def remove_whitespace(cls, string: str) -> str:
        """
        Removes all space characters from the input string.

        Note:
            This does not remove tabs or newline characters, only spaces.

        Args:
            string (str): The input string from which to remove spaces.

        Returns:
            str: A string with all space characters removed.
        """
        return string.replace(" ", "")

    @classmethod
    def remove_whitespace_before_eol(cls, string: str) -> str:
        """
        Removes whitespace that appears immediately before a newline character.

        Args:
            string (str): The input string that may contain trailing whitespace.

        Returns:
            str: A string where whitespace before line breaks is removed.
        """
        return cls.WHITESPACE_EOL.sub("\n", string)

    @classmethod
    def escape_xml_entities(cls, string: str) -> str:
        """
        Escapes XML entities.

        Args:
            string (str): The input string that may contain resolved entities.

        Returns:
            str: A string where entities are escaped.
        """
        result = string

        if "&" in result:
            result = result.replace("&", "&amp;")
        if "<" in result:
            result = result.replace("<", "&lt;")
        if ">" in result:
            result = result.replace(">", "&gt;")
        if '"' in result:
            result = result.replace('"', "&quot;")
        if "'" in result:
            result = result.replace("'", "&apos;")

        return result
