import re


class StringManipulation:
    EMPTY_LINES: re.Pattern[str] = re.compile(r"\n+")
    WHITESPACES: re.Pattern[str] = re.compile(r"\s+")
    WHITESPACE_EOL: re.Pattern[str] = re.compile(r"\s+\n")

    @classmethod
    def convert_list_to_string(cls, result: list[str]) -> str:
        return "\n".join(result)

    @classmethod
    def reduce_redundant_whitespace(cls, string: str) -> str:
        return cls.WHITESPACES.sub(" ", string)

    @classmethod
    def remove_empty_lines(cls, string: str) -> str:
        return cls.EMPTY_LINES.sub("\n", string)

    @classmethod
    def remove_whitespace(cls, string: str) -> str:
        return string.replace(" ", "")

    @classmethod
    def remove_whitespace_before_end_of_line(cls, string: str) -> str:
        return cls.WHITESPACE_EOL.sub("\n", string)
