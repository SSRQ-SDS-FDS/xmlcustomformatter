"""This module tests the behavior of the Options class."""

from typing import cast, Any

import pytest
from pytest import FixtureRequest

from xmlcustomformatter.options import Options


class TestDefaultOptions:
    """This class tests the default behavior of the Options class."""

    @staticmethod
    @pytest.fixture
    def default_options() -> Options:
        """Fixture that provides an Options instance with default values."""
        return Options()

    @staticmethod
    @pytest.fixture
    def default_indentation() -> int:
        """Fixture for the default indentation value."""
        return 4

    @staticmethod
    @pytest.fixture
    def default_max_line_length() -> int:
        """Fixture for the default max_line_length value."""
        return 120

    @staticmethod
    @pytest.fixture
    def default_inline_elements() -> tuple[()]:
        """Fixture for the default inline_elements tuple."""
        return ()

    @staticmethod
    @pytest.fixture
    def default_semicontainer_elements() -> tuple[()]:
        """Fixture for the default semicontainer_elements tuple."""
        return ()

    @staticmethod
    def test_default_indentation(default_options: Options, default_indentation: int) -> None:
        """Tests that the default indentation value is correctly set."""
        assert default_options.indentation == default_indentation

    @staticmethod
    def test_default_max_line_length(
        default_options: Options, default_max_line_length: int
    ) -> None:
        """Tests that the default max_line_length value is correctly set."""
        assert default_options.max_line_length == default_max_line_length

    @staticmethod
    def test_default_inline_elements(
        default_options: Options, default_inline_elements: tuple[()]
    ) -> None:
        """Tests that the default inline_elements tuple is correctly set."""
        assert default_options.inline_elements == default_inline_elements

    @staticmethod
    def test_default_semicontainer_elements(
        default_options: Options, default_semicontainer_elements: tuple[()]
    ) -> None:
        """Tests that the default semicontainer_elements tuple is correctly set."""
        assert default_options.semicontainer_elements == default_semicontainer_elements


class TestCustomOptions:
    """This class tests the custom behavior of the Options class."""

    @staticmethod
    @pytest.mark.parametrize("indentation", [2, 0, 10])
    def test_custom_indentation(indentation: int) -> None:
        """Tests that custom indentation values are accepted and correctly set."""
        options = Options(indentation=indentation)
        assert options.indentation == indentation

    @staticmethod
    @pytest.mark.parametrize("max_line_length", [50, 120, 0])
    def test_custom_max_line_length(max_line_length: int) -> None:
        """Tests that custom max_line_length values are accepted and correctly set."""
        options = Options(max_line_length=max_line_length)
        assert options.max_line_length == max_line_length

    @staticmethod
    @pytest.fixture(
        params=[
            ("a",),
            (
                "div",
                "span",
            ),
        ],
        ids=[
            "one element",
            "two elements",
        ],
    )
    def valid_elements(request: FixtureRequest) -> tuple[str, ...]:
        """Valid inline_elements tuples."""
        return cast(tuple[str, ...], request.param)

    @staticmethod
    @pytest.fixture(
        params=[
            (tuple(),),
            (["div", 42]),
            ((None,)),
            ([object()]),
            ((b"byte",)),
            ([True]),
        ],
        ids=["an empty tuple", "integers", "none", "objects", "bytes", "booleans"],
    )
    def invalid_elements(request: FixtureRequest) -> tuple[Any, ...]:
        """Invalid inline_elements inputs."""
        return tuple(request.param)

    @staticmethod
    def test_custom_inline_elements(valid_elements: tuple[str, ...]) -> None:
        """Valid tuples are accepted and set correctly."""
        options = Options(inline_elements=valid_elements)
        assert options.inline_elements == valid_elements

    @staticmethod
    def test_custom_invalid_inline_elements(invalid_elements: tuple[Any, ...]) -> None:
        """Invalid tuples raise TypeError."""
        with pytest.raises(TypeError):
            Options(inline_elements=invalid_elements)

    @staticmethod
    def test_custom_semicontainer_elements(valid_elements: tuple[str, ...]) -> None:
        """Valid tuples are accepted and set correctly."""
        options = Options(semicontainer_elements=valid_elements)
        assert options.semicontainer_elements == valid_elements

    @staticmethod
    def test_custom_invalid_semicontainer_elements(invalid_elements: tuple[Any, ...]) -> None:
        """Invalid tuples raise TypeError."""
        with pytest.raises(TypeError):
            Options(semicontainer_elements=invalid_elements)
