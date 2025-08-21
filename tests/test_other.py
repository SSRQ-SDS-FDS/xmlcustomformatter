"""This class contains various other tests."""

from xml.dom.minidom import Node
from pathlib import Path

import pytest

from xmlcustomformatter.formatter import XMLCustomFormatter
from xmlcustomformatter.options import Options


class TestXMLCustomFormatterOther:
    """This class contains various other tests."""

    @staticmethod
    @pytest.fixture
    def xml_dummy(tmp_path: Path) -> XMLCustomFormatter:
        """Yields an instance of the XMLCustomFormatter class."""
        xml = "<root/>"
        input_path = tmp_path / "input.xml"
        output_path = tmp_path / "output.xml"
        input_path.write_text(xml, encoding="UTF-8")
        options = Options(inline_elements=("root",))
        return XMLCustomFormatter(str(input_path), str(output_path), options)

    @staticmethod
    def test_get_result_as_list(xml_dummy: XMLCustomFormatter) -> None:
        """Tests the result as a list of strings."""
        expected = ['<?xml version="1.0" encoding="UTF-8"?>\n', "<root/>"]
        assert xml_dummy.get_result_as_list() == expected

    @staticmethod
    def test_get_result_as_string(xml_dummy: XMLCustomFormatter) -> None:
        """Tests the result as a string."""
        expected = """<?xml version="1.0" encoding="UTF-8"?>\n<root/>"""
        assert xml_dummy.get_result_as_string() == expected

    @staticmethod
    def test_xml_wrong_node(xml_dummy: XMLCustomFormatter) -> None:
        """Tests that an unhandled node type raises an exception."""
        with pytest.raises(TypeError):
            xml_dummy._process_node(Node())

    @staticmethod
    def test_output_file_is_created(xml_dummy: XMLCustomFormatter) -> None:
        """Checks that the output file is created."""
        assert Path(xml_dummy.output_file).exists()

    @staticmethod
    def test_output_file_has_correct_content(xml_dummy: XMLCustomFormatter) -> None:
        """Checks that the output file has the correct content."""
        expected = """<?xml version="1.0" encoding="UTF-8"?>\n<root/>"""
        result = Path(xml_dummy.output_file).read_text(encoding="UTF-8")
        assert result == expected

    @staticmethod
    def test_really_long_input_line(tmp_path: Path) -> None:
        """Tests too long lines without breaking point are not split up."""
        xml = "<root>Donaudampfschifffahrtsgesellschaftskapitänsversicherungsanspruchs"
        xml += "prüfungskommissionsteilnehmervergütungsgesetzinkraftsetzungsverordnung</root>"
        expected = '<?xml version="1.0" encoding="UTF-8"?>\n<root>\n'
        expected += "    Donaudampfschifffahrtsgesellschaftskapitänsversicherungsanspruchs"
        expected += "prüfungskommissionsteilnehmervergütungsgesetzinkraftsetzungsverordnung\n"
        expected += "</root>"
        input_path = tmp_path / "input.xml"
        output_path = tmp_path / "output.xml"
        input_path.write_text(xml, encoding="UTF-8")
        options = Options()
        XMLCustomFormatter(str(input_path), str(output_path), options)
        result = output_path.read_text(encoding="UTF-8")
        assert result == expected

    @staticmethod
    def test_really_long_input_line_inline(tmp_path: Path) -> None:
        """Tests too long lines without breaking point are not split up."""
        xml = "<root>Donaudampfschifffahrtsgesellschaftskapitänsversicherungsanspruchs"
        xml += "prüfungskommissionsteilnehmervergütungsgesetzinkraftsetzungsverordnung</root>"
        expected = '<?xml version="1.0" encoding="UTF-8"?>\n<root>'
        expected += "Donaudampfschifffahrtsgesellschaftskapitänsversicherungsanspruchs"
        expected += "prüfungskommissionsteilnehmervergütungsgesetzinkraftsetzungsverordnung"
        expected += "</root>"
        input_path = tmp_path / "input.xml"
        output_path = tmp_path / "output.xml"
        input_path.write_text(xml, encoding="UTF-8")
        options = Options(inline_elements=("root",))
        XMLCustomFormatter(str(input_path), str(output_path), options)
        result = output_path.read_text(encoding="UTF-8")
        assert result == expected
