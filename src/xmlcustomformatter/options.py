from dataclasses import dataclass, field


@dataclass(frozen=True)
class Options:
    """
    Configuration options for the XML formatter.

    Attributes:
        indentation: Number of spaces used for indentation.
        max_line_length: Maximum allowed line length before wrapping occurs.
        inline_elements: A tuple of element tag names that should be treated as inline
            during formatting. All elements must be strings.
    """

    # Main options
    indentation: int = field(default=4)
    max_line_length: int = field(default=80)

    # Options for elements
    inline_elements: tuple[str, ...] = field(default_factory=tuple)

    # Options for comments
    comments_have_trailing_spaces: bool = field(default=True)
    comments_start_new_lines: bool = field(default=True)

    def __post_init__(self) -> None:
        """
        Validates that all elements in `inline_elements` are of type `str`.

        Raises:
            TypeError: If one or more elements in `inline_elements` are not strings.
        """
        invalid = [el for el in self.inline_elements if not isinstance(el, str)]
        if invalid:
            raise TypeError(f"inline_elements must contain only strings. Invalid: {invalid}")
