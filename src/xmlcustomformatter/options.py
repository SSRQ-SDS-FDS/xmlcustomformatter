from dataclasses import dataclass, field


@dataclass(frozen=True)
class Options:
    """Options for the XML formatter."""

    indentation: int = field(default=4)
    inline_elements: list[str] | None = field(default=None)
    max_line_length: int = field(default=80)
