"""This module tests the formatting of a complete example file."""

from pathlib import Path

import pytest

from xmlcustomformatter.formatter import XMLCustomFormatter
from xmlcustomformatter.options import Options


class TestXMLCustomFormatterExampleFile:
    """This class tests the formatting of a complete example file."""

    @staticmethod
    @pytest.mark.parametrize(
        "options, file_name",
        [
            (
                Options(),
                "tests/example_files/SSRQ-SG-III_4-24_all_container.xml",
            ),
            (
                Options(
                    semicontainer_elements=(
                        "add",
                        "author",
                        "cell",
                        "corr",
                        "custEvent",
                        "date",
                        "del",
                        "expan",
                        "head",
                        "height",
                        "idno",
                        "item",
                        "lb",
                        "lem",
                        "material",
                        "measure",
                        "note",
                        "origDate",
                        "origPlace",
                        "publisher",
                        "pubPlace",
                        "q",
                        "quote",
                        "rdg",
                        "repository",
                        "resp",
                        "settlement",
                        "title",
                        "width",
                    ),
                    inline_elements=(
                        "abbr",
                        "addSpan",
                        "anchor",
                        "bibl",
                        "damage",
                        "damageSpan",
                        "delSpan",
                        "foreign",
                        "fw",
                        "gap",
                        "handShift",
                        "hi",
                        "label",
                        "num",
                        "orgName",
                        "orig",
                        "pc",
                        "persName",
                        "placeName",
                        "precision",
                        "ref",
                        "sic",
                        "space",
                        "supplied",
                        "term",
                        "time",
                        "unclear",
                    ),
                ),
                "tests/example_files/SSRQ-SG-III_4-24_custom.xml",
            ),
        ],
        ids=["all_container", "custom"],
    )
    def test_example_file(tmp_path: Path, options: Options, file_name: str) -> None:
        """Tests whether the formatted file equals the expected file."""
        input_file = "tests/example_files/SSRQ-SG-III_4-24_unformatiert.xml"
        output_file = str(tmp_path / "output.xml")
        expected = Path(file_name).read_text(encoding="UTF-8")
        XMLCustomFormatter(input_file, output_file, options)
        result = Path(output_file).read_text(encoding="UTF-8")
        assert result == expected
