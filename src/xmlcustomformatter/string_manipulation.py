import re

EMPTY_LINES: re.Pattern = re.compile(r"\n+")
WHITESPACES: re.Pattern = re.compile(r"\s+")
WHITESPACE_EOL: re.Pattern = re.compile(r"\s+\n")


def convert_list_to_string(result: list[str]):
    return "\n".join(result)


def reduce_redundant_whitespace(string: str):
    return WHITESPACES.sub(" ", string)


def remove_empty_lines(string: str):
    return EMPTY_LINES.sub("\n", string)


def remove_whitespace(string: str):
    return string.replace(" ", "")


def remove_whitespace_before_end_of_line(string: str):
    return WHITESPACE_EOL.sub("\n", string)
