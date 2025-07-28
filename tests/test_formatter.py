import pytest

from xmlcustomformatter.formatter import XMLCustomFormatter
from xmlcustomformatter.options import Options


@pytest.fixture
def formatter() -> XMLCustomFormatter:
    return XMLCustomFormatter("input.xml", "output.xml")


@pytest.fixture
def formatter_with_options() -> XMLCustomFormatter:
    return XMLCustomFormatter(
        "input.xml", "output.xml", Options(2, 100, ("div", "span"))
    )


def test_init_sets_input_file(formatter: XMLCustomFormatter) -> None:
    assert formatter.input_file == "input.xml"


def test_init_sets_output_file(formatter: XMLCustomFormatter) -> None:
    assert formatter.output_file == "output.xml"


def test_init_sets_default_formatting_options(formatter: XMLCustomFormatter) -> None:
    assert isinstance(formatter.options, Options)


def test_init_accepts_custom_formatting_options(
    formatter_with_options: XMLCustomFormatter,
) -> None:
    assert isinstance(formatter_with_options.options, Options)
