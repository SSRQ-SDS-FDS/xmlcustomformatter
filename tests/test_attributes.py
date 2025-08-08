from pathlib import Path

import pytest

from xmlcustomformatter.formatter import XMLCustomFormatter
from xmlcustomformatter.options import Options


class TestXMLCustomFormatterAttribute:
    @pytest.mark.parametrize(
        "test_name, xml_content, expected, options",
        [
            (
                "one_attribute",
                """<root a="b"/>""",
                """<?xml version="1.0" encoding="UTF-8"?><root a="b"/>""",
                Options(),
            ),
            (
                "two_attributes",
                """<root a="b" b="c"/>""",
                """<?xml version="1.0" encoding="UTF-8"?><root a="b" b="c"/>""",
                Options(),
            ),
            (
                "two_attributes_ordered_alphabetical",
                """<root b="c" a="b"/>""",
                """<?xml version="1.0" encoding="UTF-8"?><root a="b" b="c"/>""",
                Options(),
            ),
            (
                "two_attributes_not_ordered_alphabetical",
                """<root b="c" a="b"/>""",
                """<?xml version="1.0" encoding="UTF-8"?><root b="c" a="b"/>""",
                Options(sorted_attributes=False),
            ),
            (
                "attribute_with_single_quotes",
                """<root a='b'/>""",
                """<?xml version="1.0" encoding="UTF-8"?><root a="b"/>""",
                Options(),
            ),
            (
                "attribute_with_single_quotes_inside_double_quotes",
                """<root a="'b'"/>""",
                """<?xml version="1.0" encoding="UTF-8"?><root a="'b'"/>""",
                Options(),
            ),
            (
                "attribute_with_double_quotes_inside_single_quotes",
                """<root a='"b"'/>""",
                """<?xml version="1.0" encoding="UTF-8"?><root a="&quot;b&quot;"/>""",
                Options(),
            ),
        ],
    )
    def test_attributes(
        self, tmp_path: Path, test_name: str, xml_content: str, expected: str, options: Options
    ) -> None:
        file_path = tmp_path / "input.xml"
        file_path.write_text(xml_content)
        formatter = XMLCustomFormatter(str(file_path), "output.xml", options)
        print(formatter._result)
        assert "".join(formatter._result) == expected
