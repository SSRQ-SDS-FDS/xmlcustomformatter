"""This module tests the processing of doctype declarations."""

from pathlib import Path

import pytest

from xmlcustomformatter.formatter import XMLCustomFormatter
from xmlcustomformatter.options import Options


class TestXMLCustomFormatterDocumentTypes:
    """This class tests the processing of doctype declarations."""

    @pytest.mark.parametrize(
        "xml_content, expected, options",
        [
            (
                """<!DOCTYPE root><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE root>\n<root/>""",
                Options(),
            ),
            (
                """<!DOCTYPE root SYSTEM "foo"><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE root SYSTEM "foo">\n<root/>""",
                Options(),
            ),
            (
                """<!DOCTYPE root PUBLIC "foo" "bar"><root/>""",
                '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE root PUBLIC "foo" "bar">'
                "\n<root/>",
                Options(),
            ),
            (
                """<!DOCTYPE root []><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE root>\n<root/>""",
                Options(),
            ),
            (
                """<!DOCTYPE root [%foo;]><root/>""",
                '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE root [\n    %foo;\n]>\n<root/>',
                Options(),
            ),
            (
                """<!DOCTYPE root [<?foo bar?>]><root/>""",
                '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE root ['
                "\n    <?foo bar?>\n]>\n<root/>",
                Options(),
            ),
            (
                """<!DOCTYPE root [<!--foo-->]><root/>""",
                '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE root ['
                "\n    <!--foo-->\n]>\n<root/>",
                Options(),
            ),
            (
                """<!DOCTYPE root [<!NOTATION foo SYSTEM "foo">]><root/>""",
                '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE root ['
                '\n    <!NOTATION foo SYSTEM "foo">\n]>\n<root/>',
                Options(),
            ),
            (
                """<!DOCTYPE root [<!ENTITY foo "foo">]><root/>""",
                '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE root ['
                '\n    <!ENTITY foo "foo">\n]>\n<root/>',
                Options(),
            ),
            (
                """<!DOCTYPE root [<!ELEMENT root EMPTY>]><root/>""",
                '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE root ['
                "\n    <!ELEMENT root EMPTY>\n]>\n<root/>",
                Options(),
            ),
            (
                """<!DOCTYPE root [<!ATTLIST root>]><root/>""",
                '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE root ['
                "\n    <!ATTLIST root>\n]>\n<root/>",
                Options(),
            ),
            (
                '<!DOCTYPE root PUBLIC "foo" "bar" ['
                "<!ELEMENT root EMPTY>"
                "<!ATTLIST root>"
                "<!--Test-->"
                "<?foo bar?>"
                '<!NOTATION foo SYSTEM "foo">'
                '<!ENTITY foo "foo">'
                "%foo;"
                "]><root/>",
                '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE root PUBLIC "foo" "bar" ['
                "\n    <!ELEMENT root EMPTY>"
                "\n    <!ATTLIST root>"
                "\n    <!--Test-->"
                "\n    <?foo bar?>"
                '\n    <!NOTATION foo SYSTEM "foo">'
                '\n    <!ENTITY foo "foo">'
                "\n    %foo;\n]>\n<root/>",
                Options(),
            ),
            (
                '<!DOCTYPE root PUBLIC "foo" "bar" ['
                "<!ELEMENT root EMPTY>"
                "<!ATTLIST root>"
                "<!--Test-->"
                "<?foo bar?>"
                '<!NOTATION foo SYSTEM "foo">'
                '<!ENTITY foo "foo">'
                "%foo;"
                "]><root/>",
                '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root PUBLIC "foo" "bar" ['
                "<!ELEMENT root EMPTY>"
                "<!ATTLIST root>"
                "<!--Test-->"
                "<?foo bar?>"
                '<!NOTATION foo SYSTEM "foo">'
                '<!ENTITY foo "foo">'
                "%foo;]><root/>",
                Options(
                    doctype_declaration_starts_new_line=False,
                    doctype_subset_parts_start_new_lines=False,
                ),
            ),
        ],
        ids=[
            "minimal_doctype",
            "doctype_with_external_id_system",
            "doctype_with_external_id_public",
            "doctype_with_empty_internal_subset",
            "doctype_with_internal_subset_with_pereference",
            "doctype_with_internal_subset_with_pi",
            "doctype_with_internal_subset_with_comment",
            "doctype_with_internal_subset_with_notation",
            "doctype_with_internal_subset_with_entity",
            "doctype_with_internal_subset_with_element",
            "doctype_with_internal_subset_with_attlist",
            "doctype_with_all_kinds_of_content",
            "doctype_with_all_kinds_of_content",
        ],
    )
    def test_document_types(
        self, tmp_path: Path, xml_content: str, expected: str, options: Options
    ) -> None:
        """Tests the processing of doctype declarations."""
        file_path = tmp_path / "input.xml"
        file_path.write_text(xml_content)
        formatter = XMLCustomFormatter(str(file_path), "output.xml", options)
        assert "".join(formatter._result) == expected
