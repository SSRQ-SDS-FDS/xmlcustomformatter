from pathlib import Path

import pytest

from xmlcustomformatter.formatter import XMLCustomFormatter


class TestXMLCustomFormatterDocumentTypes:
    @pytest.mark.parametrize(
        "test_name, xml_content, expected",
        [
            (
                "minimal_doctype",
                """<!DOCTYPE root><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE root>\n<root/>""",
            ),
            (
                "doctype_with_external_id_system",
                """<!DOCTYPE root SYSTEM "foo"><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE root SYSTEM "foo">\n<root/>""",
            ),
            (
                "doctype_with_external_id_public",
                """<!DOCTYPE root PUBLIC "foo" "bar"><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE root PUBLIC "foo" "bar">\n<root/>""",
            ),
            (
                "doctype_with_empty_internal_subset",
                """<!DOCTYPE root []><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE root []>\n<root/>""",
            ),
            (
                "doctype_with_internal_subset_with_pereference",
                """<!DOCTYPE root [%foo;]><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE root [%foo;]>\n<root/>""",
            ),
            (
                "doctype_with_internal_subset_with_pi",
                """<!DOCTYPE root [<?foo bar?>]><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE root [<?foo bar?>]>\n<root/>""",
            ),
            (
                "doctype_with_internal_subset_with_comment",
                """<!DOCTYPE root [<!--foo-->]><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE root [<!--foo-->]>\n<root/>""",
            ),
            (
                "doctype_with_internal_subset_with_notation",
                """<!DOCTYPE root [<!NOTATION foo SYSTEM "foo">]><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE root [<!NOTATION foo SYSTEM "foo">]>\n<root/>""",
            ),
            (
                "doctype_with_internal_subset_with_entity",
                """<!DOCTYPE root [<!ENTITY foo "foo">]><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE root [<!ENTITY foo "foo">]>\n<root/>""",
            ),
            (
                "doctype_with_internal_subset_with_element",
                """<!DOCTYPE root [<!ELEMENT root EMPTY>]><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE root [<!ELEMENT root EMPTY>]>\n<root/>""",
            ),
            (
                "doctype_with_internal_subset_with_attlist",
                """<!DOCTYPE root [<!ATTLIST root>]><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE root [<!ATTLIST root>]>\n<root/>""",
            ),
            (
                "doctype_with_all_kinds_of_content",
                """<!DOCTYPE root PUBLIC "foo" "bar" [
                <!ELEMENT root EMPTY>
                <!ATTLIST root>
                <!--Test-->
                <?foo bar?>
                <!NOTATION foo SYSTEM "foo">
                <!ENTITY foo "foo">
                %foo;
                ]><root/>""",
                """<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE root PUBLIC "foo" "bar" [
                <!ELEMENT root EMPTY>
                <!ATTLIST root>
                <!--Test-->
                <?foo bar?>
                <!NOTATION foo SYSTEM "foo">
                <!ENTITY foo "foo">
                %foo;
                ]>\n<root/>""",
            ),
        ],
    )
    def test_document_types(
        self, tmp_path: Path, test_name: str, xml_content: str, expected: str
    ) -> None:
        file_path = tmp_path / "input.xml"
        file_path.write_text(xml_content)
        formatter = XMLCustomFormatter(str(file_path), "output.xml")
        print(formatter._result)
        assert "".join(formatter._result) == expected
