"""This module contains the entry point."""

import argparse
from pathlib import Path
from importlib.metadata import version

from .formatter import XMLCustomFormatter
from .options import Options

__version__ = version("xmlcustomformatter")


def build_options_from_args(args: argparse.Namespace) -> Options:
    """
    Builds an options object from cli arguments.
    """
    return Options(
        indentation=args.indentation,
        max_line_length=args.max_line_length,
        inline_elements=tuple(args.inline_elements or []),
        semicontainer_elements=tuple(args.semicontainer_elements or []),
        sorted_attributes=args.sorted_attributes,
        comments_have_trailing_spaces=args.comments_have_trailing_spaces,
        comments_start_new_lines=args.comments_start_new_lines,
        doctype_declaration_starts_new_line=args.doctype_declaration_starts_new_line,
        doctype_subset_parts_start_new_lines=args.doctype_subset_parts_start_new_lines,
        processing_instructions_start_new_lines=args.processing_instructions_start_new_lines,
    )


def main() -> None:
    """The entry point."""

    parser = argparse.ArgumentParser(
        prog="xmlfmt",
        description="Custom XML formatter with configurable indentation, wrapping and rules.",
    )

    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    parser.add_argument("input", type=Path, help="Path to input XML file")
    parser.add_argument("output", type=Path, help="Path to output XML file")

    parser.add_argument(
        "--indentation", type=int, default=4, help="Number of whitespaces for indentation"
    )
    parser.add_argument(
        "--max-line-length", type=int, default=120, help="Maximum number of chars per line"
    )

    parser.add_argument("--inline-elements", nargs="*", help="Elements to be treated inline")
    parser.add_argument(
        "--semicontainer-elements", nargs="*", help="Elements to be treated as semi-container"
    )

    parser.add_argument(
        "--no-sorted-attributes",
        dest="sorted_attributes",
        action="store_false",
        help="Attributes will not be sorted",
    )
    parser.set_defaults(sorted_attributes=True)

    parser.add_argument(
        "--no-comments-trailing-spaces",
        dest="comments_have_trailing_spaces",
        action="store_false",
        help="Comments will not have trailing spaces",
    )
    parser.set_defaults(comments_have_trailing_spaces=True)

    parser.add_argument(
        "--no-comments-newline",
        dest="comments_start_new_lines",
        action="store_false",
        help="Comments don't start a new line",
    )
    parser.set_defaults(comments_start_new_lines=True)

    parser.add_argument(
        "--no-doctype-newline",
        dest="doctype_declaration_starts_new_line",
        action="store_false",
        help="Doctype declarations don't start a new line",
    )
    parser.set_defaults(doctype_declaration_starts_new_line=True)

    parser.add_argument(
        "--no-doctype-subset-newlines",
        dest="doctype_subset_parts_start_new_lines",
        action="store_false",
        help="Doctype subsets don't start a new line ",
    )
    parser.set_defaults(doctype_subset_parts_start_new_lines=True)

    parser.add_argument(
        "--no-pi-newline",
        dest="processing_instructions_start_new_lines",
        action="store_false",
        help="Processing instructions don't start a new line",
    )
    parser.set_defaults(processing_instructions_start_new_lines=True)

    args = parser.parse_args()

    XMLCustomFormatter(str(args.input), str(args.output), build_options_from_args(args))


if __name__ == "__main__":  # pragma: no cover
    main()
