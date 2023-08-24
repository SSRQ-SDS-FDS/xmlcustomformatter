import argparse

from xmldomformatter.options import XMLFormattingOptions
from xmldomformatter.formatter import XMLCustomFormatter


def main():
    parser = argparse.ArgumentParser(description="Process some files.")
    parser.add_argument("input_file", type=str, help="The name of the file to format")
    parser.add_argument(
        "output_file",
        type=str,
        nargs="?",
        help="The name of the output file. If not provided, defaults to the input file name.",
    )
    parser.add_argument(
        "--inline_tags", nargs="+", type=str, help="list of inline tags"
    )
    args = parser.parse_args()

    output_file = args.input_file if args.output_file is None else args.output_file

    list_of_tags = args.inline_tags or []
    formatting_options = XMLFormattingOptions(
        max_line_length=80, indentation=4, inline_elements=list_of_tags
    )

    print(f"Formatting input file: {args.input_file}")
    print(f"Saving output to: {output_file}")
    print(f"Inline tags: {list_of_tags}")

    XMLCustomFormatter(
        input_file=args.input_file,
        output_file=output_file,
        formatting_options=formatting_options,
    )

    print("Done!")


if __name__ == "__main__":
    main()
