import pytest

from xmlcustomformatter.options import Options


@pytest.fixture
def default_options() -> Options:
    return Options()


@pytest.fixture
def default_indentation() -> int:
    return 4


@pytest.fixture
def default_max_line_length() -> int:
    return 80


@pytest.fixture
def empty_inline_elements() -> tuple[()]:
    return ()


def test_default_indentation(
    default_options: Options, default_indentation: int
) -> None:
    assert default_options.indentation == default_indentation


def test_default_max_line_length(
    default_options: Options, default_max_line_length: int
) -> None:
    assert default_options.max_line_length == default_max_line_length


def test_default_inline_elements(
    default_options: Options, empty_inline_elements: tuple[()]
) -> None:
    assert default_options.inline_elements == empty_inline_elements


@pytest.mark.parametrize("indentation", [2, 0, 10])
def test_custom_indentation(indentation: int) -> None:
    options = Options(indentation=indentation)
    assert options.indentation == indentation


@pytest.mark.parametrize("max_line_length", [50, 120, 0])
def test_custom_max_line_length(max_line_length: int) -> None:
    options = Options(max_line_length=max_line_length)
    assert options.max_line_length == max_line_length


@pytest.mark.parametrize(
    "inline_elements",
    [
        ("div", "span"),
        tuple(),
        ("a",),
    ],
)
def test_custom_inline_elements(inline_elements: tuple[str, str]) -> None:
    options = Options(inline_elements=inline_elements)
    assert options.inline_elements == inline_elements


@pytest.mark.parametrize(
    "invalid_input",
    [
        ["div", 42],  # integers
        (None,),  # None
        [object()],  # arbitrary objects
        (b"byte",),  # bytes
        [True],  # booleans
    ],
)
def test_custom_invalid_inline_elements(invalid_input: tuple[str, str]) -> None:
    with pytest.raises(TypeError, match="inline_elements must contain only strings"):
        Options(inline_elements=tuple(invalid_input))
