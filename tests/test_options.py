import pytest

from xmlcustomformatter.options import Options


@pytest.fixture
def default_options():
    return Options()


@pytest.mark.parametrize("expected_indentation", [4])
def test_default_indentation(default_options, expected_indentation):
    assert default_options.indentation == expected_indentation


@pytest.mark.parametrize("expected_max_line_length", [80])
def test_default_max_line_length(default_options, expected_max_line_length):
    assert default_options.max_line_length == expected_max_line_length


@pytest.mark.parametrize("expected_inline_elements", [()])
def test_default_inline_elements(default_options, expected_inline_elements):
    assert default_options.inline_elements == expected_inline_elements


@pytest.mark.parametrize("indentation", [2, 0, 10])
def test_custom_indentation(indentation):
    opts = Options(indentation=indentation)
    assert opts.indentation == indentation


@pytest.mark.parametrize("max_line_length", [50, 120, 0])
def test_custom_max_line_length(max_line_length):
    opts = Options(max_line_length=max_line_length)
    assert opts.max_line_length == max_line_length


@pytest.mark.parametrize(
    "inline_elements",
    [
        ("div", "span"),
        tuple(),
        ("a",),
    ],
)
def test_custom_inline_elements(inline_elements):
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
def test_custom_invalid_inline_elements(invalid_input):
    with pytest.raises(TypeError, match="inline_elements must contain only strings"):
        Options(inline_elements=tuple(invalid_input))
