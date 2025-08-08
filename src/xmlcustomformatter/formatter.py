from typing import Optional, cast
from xml.dom import minidom
from xml.dom.minidom import (
    Node,
    Element,
    Attr,
    Text,
    CDATASection,
    ProcessingInstruction,
    Comment,
    Document,
    DocumentType,
)

from xmlcustomformatter.options import Options
from xmlcustomformatter.stringmanipulation import StringManipulation as SM


class XMLCustomFormatter:
    """
    Formatter for XML files applying custom formatting options.

    Args:
        input_file (str): Path to the input XML file to be read.
        output_file (str): Path to the output XML file where the formatted XML will be saved.
        options (Options, optional): Configuration options for formatting.
            If not provided, default Options() will be used.

    Default values:
        If no information is provided in the XML file to be processed, then
        XML Version 1.0, encoding UTF-8 and an empty standalone declaration are used.
    """

    default_version: str = "1.0"
    default_encoding: str = "UTF-8"
    default_standalone: str = ""

    def __init__(
        self,
        input_file: str,
        output_file: str,
        options: Optional[Options] = None,
    ):
        """
        Initializes a XMLCustomFormatter instance.
        The input XML file is automatically parsed with the built-in
        minidom parser and formatted.
        """
        self.input_file = input_file
        self.output_file = output_file
        self.options = options or Options()
        self._dom = minidom.parse(self.input_file)
        self._indentation_level: int = 0
        self._result: list[str] = []
        self._process_xml_declaration()
        self._process_node(self._dom)
        #     self.postprocess()
        #     self.write_to_output_file()

    def _process_xml_declaration(self) -> None:
        """
        Processes the XML declaration. If version, encoding or standalone are not
        set, then default values will be used. The declaration is appended to the result.
        """
        self._result.append(self._construct_xml_declaration())

    def _construct_xml_declaration(self) -> str:
        """Constructs the XML declaration."""
        version = self._set_version()
        encoding = self._set_encoding()
        standalone = self._set_standalone()
        return f"<?xml{version}{encoding}{standalone}?>"

    def _set_encoding(self) -> str:
        """Sets the encoding part of the XML declaration."""
        if self._dom.encoding is None:
            return f' encoding="{self.default_encoding}"'
        return f' encoding="{self._dom.encoding}"'

    def _set_standalone(self) -> str:
        """Sets the standalone part of the XML declaration."""
        if self._dom.standalone is None:
            return self.default_standalone
        elif self._dom.standalone:
            return ' standalone="yes"'
        else:
            return ' standalone="no"'

    def _set_version(self) -> str:
        """Sets the version part of the XML declaration."""
        if self._dom.version is None:
            return f' version="{self.default_version}"'
        return f' version="{self._dom.version}"'

    def _process_node(self, node: Node) -> None:
        """Delegates the processing of nodes to specialized methods."""
        match node:
            case Attr():
                self._process_attribute_node(node)
            case Comment():
                self._process_comment_node(node)
            case Document():
                self._process_document_node(node)
            case DocumentType():
                self._process_document_type_node(node)
            case Element():
                self._process_element_node(node)
            case ProcessingInstruction():
                self._process_processing_instruction_node(node)
            case Text():
                # CDATASection() shares the same interface as Text().
                # Therefore CDATASection() will be treated as an instance
                # of Text() by minidom. So you have to distinguish by the
                # nodeType property. These two cases are exhaustive.
                if node.nodeType == Node.TEXT_NODE:
                    self._process_text_node(node)
                else:
                    self._process_cdata_section_node(node)
            case _:
                raise TypeError(f"Wrong node type: {repr(node)}")
            #
            # The following cases are commented out because of different reasons:
            #
            # case CDATASection():
            #     # This case cannot be reached as CDATASection is a child class
            #     # of Text. Every CDATASection in the XML will be parsed into
            #     # a Text object. Therefore cf. case Text() for processing of
            #     # CDATASections.
            #     self._process_cdatasection_node(node)
            #
            # case DocumentFragment():
            #     # The following case is commented out, because xml.dom.miniom
            #     # DocumentFragment as a helper class when constructing
            #     # structures to be added to an existing Document object.
            #     # This node type cannot be found in a parsed XML file.
            #     self._process_document_fragment_node(node)
            #
            # case Entity():
            #     # This case is commented out, because xml.dom.minidom
            #     # uses the class Entity as a helper class, if one wants to
            #     # manually create such nodes.
            #     # This node type may be found in the DocumentType.entities node map,
            #     # but because it is part of the document type declaration,
            #     # it will also be part of the DocumentType.internalSubset property.
            #     # Thus it is not necessary to process this kind of node while formatting.
            #     self._process_entity_node(node)
            #
            # case EntityReference():
            #     # This case cannot be reaches as xml.dom.minidom uses an expat-based
            #     # parser, which will resolve all entity references. Thus, EntityReference
            #     # is not implemented in xml.dom.minidom.
            #     self._process_entity_reference_node(node)
            #
            # case Notation():
            #     # The following case is commented out, because xml.dom.minidom
            #     # uses the class Notation as a helper class, if one wants to
            #     # manually create such nodes.
            #     # This node type may be found in the DocumentType.notations node map,
            #     # but because it is part of the document type declaration,
            #     # it will also be part of DocumentType.internalSubset property.
            #     # Thus it is not necessary to process this kind of node while formatting.
            #     self._process_notation_node(node)

    def _process_element_node(self, element: Element) -> None:
        """Processes all element nodes depending on emptyness."""
        if self._is_empty_element(element):
            self._process_empty_element(element)
        else:
            self._process_non_empty_element(element)

    def _process_non_empty_element(self, element: Element) -> None:
        self._process_element_start_tag(element)
        self._process_all_child_nodes(element)
        self._process_element_end_tag(element)

    def _process_element_start_tag(self, element: Element) -> None:
        self._open_start_tag(element)
        self._process_attributes(element)
        self._close_start_tag()

    def _process_element_end_tag(self, element: Element) -> None:
        self._result.append("</" + element.tagName + ">")

    def _process_empty_element(self, element: Element) -> None:
        self._open_start_tag(element)
        self._process_attributes(element)
        self._close_empty_tag()

    def _open_start_tag(self, element: Element) -> None:
        self._result.append("<" + element.tagName)

    def _close_start_tag(self) -> None:
        self._result.append(">")

    def _close_empty_tag(self) -> None:
        self._result.append("/>")

    def _process_attributes(self, element: Element) -> None:
        if element.hasAttributes():
            if self.options.ordered_attributes:
                attributes = self._sorted_attributes(element)
                for attribute in attributes.values():
                    self._process_node(attribute)
            else:
                for i in range(element.attributes.length):
                    attribute = cast(Attr, element.attributes.item(i))
                    self._process_node(attribute)

    @staticmethod
    def _sorted_attributes(element: Element) -> dict[str, Attr]:
        attributes = {}
        for i in range(element.attributes.length):
            attribute = cast(Attr, element.attributes.item(i))
            if attribute is not None:
                attributes[attribute.name] = attribute
        return dict(sorted(attributes.items()))

    def _process_attribute_node(self, attribute: Attr) -> None:
        value = SM.escape_double_quotes(attribute.value)
        self._result.append(" " + attribute.name + '="' + value + '"')

    def _process_text_node(self, text: Text) -> None:
        self._result.append(text.data)

    def _process_cdata_section_node(self, cdata: CDATASection) -> None:
        self._result.append("<![CDATA[" + cdata.data + "]]>")

    def _process_processing_instruction_node(self, pi: ProcessingInstruction) -> None:
        """Processes processing instruction nodes."""
        newline = self._set_processing_instruction_newline()
        indentation = self._indentation(self._calculate_indentation())
        start = "<?"
        target = pi.target
        data = self._normalize_processing_instruction_data(pi)
        end = "?>"
        self._result.append(newline + indentation + start + target + data + end + newline)

    @staticmethod
    def _normalize_processing_instruction_data(pi: ProcessingInstruction) -> str:
        return " " + SM.reduce_redundant_whitespace(pi.data).strip()

    def _set_processing_instruction_newline(self) -> str:
        return "\n" if self.options.processing_instructions_start_new_lines else ""

    def _process_comment_node(self, comment: Comment) -> None:
        """Processes comment nodes."""
        newline = self._set_comment_newline()
        indentation = self._indentation(self._calculate_indentation())
        start = self._set_comment_start()
        data = self._normalize_comment_data(comment)
        end = self._set_comment_end()
        self._result.append(newline + indentation + start + data + end + newline)

    @staticmethod
    def _normalize_comment_data(comment: Comment) -> str:
        return SM.reduce_redundant_whitespace(comment.data).strip()

    def _set_comment_newline(self) -> str:
        return "\n" if self.options.comments_start_new_lines else ""

    def _set_comment_start(self) -> str:
        return "<!-- " if self.options.comments_have_trailing_spaces else "<!--"

    def _set_comment_end(self) -> str:
        return " -->" if self.options.comments_have_trailing_spaces else "-->"

    def _process_document_node(self, node: Document) -> None:
        self._process_all_child_nodes(node)

    def _process_document_type_node(self, doc_type: DocumentType) -> None:
        self._result.append(self._set_doctype_content(doc_type))

    def _set_doctype_content(self, doc_type: DocumentType) -> str:
        newline = self._set_doctype_newline()
        public_id = doc_type.publicId
        system_id = doc_type.systemId
        internal_subset = doc_type.internalSubset
        start = f"<!DOCTYPE {doc_type.name}"
        content = ""
        end = ">"

        if public_id is not None:
            content += f' PUBLIC "{public_id}" "{system_id}"'

        elif system_id is not None:
            content += f' SYSTEM "{system_id}"'

        if internal_subset is not None:
            content += f" [{internal_subset}]"

        return f"{newline}{start}{content}{end}{newline}"

    def _set_doctype_newline(self) -> str:
        return "\n" if self.options.doctype_declaration_starts_new_line else ""

    def _process_all_child_nodes(self, node: Node) -> None:
        if node.hasChildNodes():
            for child in node.childNodes:
                self._process_node(child)

    @staticmethod
    def _indentation(count: int) -> str:
        """Returns a string consisting of count space characters."""
        if count < 0:
            raise ValueError("Indentation may not be negative.")
        return count * " "

    def _calculate_indentation(self) -> int:
        """Calculates the indentation depending on the indentation level and the Options."""
        return self._indentation_level * self.options.indentation

    def _decrease_indentation_level(self) -> None:
        """Decreases the indentation level by 1 as long as the indentation level is >= 0."""
        if self._indentation_level == 0:
            raise ValueError(
                f"Indentation level cannot be lower then zero {self._indentation_level}"
            )
        self._indentation_level -= 1

    def _increase_indentation_level(self) -> None:
        """Increases the indentation level by 1"""
        self._indentation_level += 1

    @staticmethod
    def _is_empty_element(element: Element) -> bool:
        return not element.hasChildNodes()

    # def postprocess(self) -> None:
    #     self.postprocess_rearrange_result()
    #     self.postprocess_result_lines()
    #     self.postprocess_result_as_string()
    #
    # # Functions for postprocessing
    # def postprocess_rearrange_result(self) -> None:
    #     self._result = "".join(self._result).split("\n")
    #
    # def postprocess_result_lines(self) -> None:
    #     lines = self._result
    #     self._result = []
    #     for line in lines:
    #         self.postprocess_line(line)
    #
    # def postprocess_result_as_string(self) -> None:
    #     self._result = sm.convert_list_to_string(self._result)
    #     self._result = sm.remove_empty_lines(self._result)
    #     self._result = sm.remove_whitespace_before_eol(self._result)
    #     self._result = self._result.strip()
    #
    # def postprocess_line(self, line: str) -> None:
    #     # Todo: split this function up to make it more readable
    #     number_of_spaces = self.get_current_indentation(line)
    #     if number_of_spaces > 0:
    #         indentation = number_of_spaces * " "
    #     else:
    #         indentation = ""
    #     if len(line) <= self.options.max_line_length:
    #         self._result.append(line)
    #     else:
    #         if " " in line:
    #             position = line.rfind(
    #                 " ", number_of_spaces, self.options.max_line_length
    #             )
    #             if position == -1:
    #                 position = line.find(" ", self.options.max_line_length)
    #                 if position == -1:
    #                     self._result.append(line)
    #                 else:
    #                     self._result.append(line[0:position] + "\n")
    #                     self.postprocess_line(indentation + line[position:].lstrip())
    #             else:
    #                 self._result.append(line[0:position] + "\n")
    #                 self.postprocess_line(indentation + line[position:].lstrip())
    #         else:
    #             self._result.append(line)
    #
    # @staticmethod
    # def get_current_indentation(string) -> int:
    #     return len(string) - len(string.lstrip())
    #
    # def write_to_output_file(self) -> None:
    #     with open(self.output_file, "w") as output_file:
    #         output_file.write(self._result)
    #
    # def is_inline_element(self, node: minidom.Element) -> bool:
    #     if (
    #         self.options.inline_elements is not None
    #         and node.tagName in self.options.inline_elements
    #     ):
    #         return True
    #
    #     return False
