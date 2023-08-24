import re as regex


def convert_list_to_string(result: list):
    return "\n".join(result)


def reduce_redundant_whitespace(string: str):
    return regex.sub(r"\s+", " ", string)


def remove_empty_lines(string: str):
    return regex.sub(r"\n+", "\n", string)


def remove_whitespace(string: str):
    return regex.sub(r"\s", "", string)


def remove_whitespace_before_end_of_line(string: str):
    return regex.sub(r"\s+\n", "\n", string)
