import dataclasses
import pytest
from xmldomformatter import options


def test_default_options():
    """Test that the default options are set correctly."""
    default_options = options.Options()
    assert default_options.indentation == 4
    assert default_options.inline_elements is None
    assert default_options.max_line_length == 80


def test_options_is_immutable():
    """Test that the options object is immutable."""
    default_options = options.Options()
    with pytest.raises(dataclasses.FrozenInstanceError):
        default_options.indentation = 2  # type: ignore
    with pytest.raises(dataclasses.FrozenInstanceError):
        default_options.inline_elements = ["a", "b", "c"]  # type: ignore
    with pytest.raises(dataclasses.FrozenInstanceError):
        default_options.max_line_length = 100  # type: ignore


def test_options_defaults_can_be_overwritten():
    """Test that the default options can be overwritten."""
    default_options = options.Options(indentation=2, max_line_length=100)
    assert default_options.indentation == 2
    assert default_options.inline_elements is None
    assert default_options.max_line_length == 100
