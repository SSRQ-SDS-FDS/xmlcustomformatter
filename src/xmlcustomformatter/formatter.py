from typing import Optional
from xml.dom import minidom
from xml.dom.minidom import (
    Node,
    Element,
    Attr,
    Text,
    CDATASection,
    Entity,
    ProcessingInstruction,
    Comment,
    Document,
    DocumentType,
    DocumentFragment,
    Notation,
)

from xmlcustomformatter.options import Options


class XMLCustomFormatter:
    """
    Formatter for XML files applying custom formatting options.

    Args:
        input_file (str): Path to the input XML file to be read.
        output_file (str): Path to the output XML file where the formatted XML will be saved.
        formatting_options (Options, optional): Configuration options for formatting.
            If not provided, default Options() will be used.

    Attributes:
        input_file (str): Input XML file path.
        output_file (str): Output file path.
        options (Options): Formatting options object.

    Default values:
        If no information is provided in the XML file which is to be processed
        XML Version 1.0 and encoding UTF-8 are used.
    """

    default_version: str = "1.0"
    default_encoding: str = "UTF-8"

    def __init__(
        self,
        input_file: str,
        output_file: str,
        formatting_options: Optional[Options] = None,
    ):
        """
        Initializes a XMLCustomFormatter instance.
        The input XML file is automatically parsed with the built-in
        minidom parser and formatted.
        """
        self.input_file = input_file
        self.output_file = output_file
        self.options = formatting_options or Options()
        self._dom = minidom.parse(self.input_file)
        self._indentation_level = 0
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
        version = self._normalize_version()
        encoding = self._normalize_encoding()
        standalone = self._normalize_standalone()
        xml_declaration = self._construct_xml_declaration(version, encoding, standalone)
        self._result.append(xml_declaration)

    def _construct_xml_declaration(self, version: str, encoding: str, standalone: str) -> str:
        """Constructs the XML declaration."""
        return f"<?xml{version}{encoding}{standalone}?>"

    def _normalize_encoding(self) -> str:
        """Normalizes the encoding part of the XML declaration."""
        if self._dom.encoding is None:
            self._dom.encoding = self.default_encoding
        return f' encoding="{self._dom.encoding}"'

    def _normalize_standalone(self) -> str:
        """
        Normalizes the standalone part of the XML declaration.
        If there is none, no default value will be used, because standalone is optional.
        """
        if self._dom.standalone is None:
            return ""
        elif self._dom.standalone:
            return ' standalone="yes"'
        else:
            return ' standalone="no"'

    def _normalize_version(self) -> str:
        """Normalizes the version part of the XML declaration."""
        if self._dom.version is None:
            self._dom.version = self.default_version
        return f' version="{self._dom.version}"'

    def _process_node(self, node: Node) -> None:
        """Delegates the processing of nodes to specialized methods."""
        match node:
            case Element():
                self._process_element_node(node)
            case Attr():
                self._process_attribute_node(node)
            case Text():
                # CDATASection() shares the same interface as Text()
                # as CDATASection is a child class of Text().
                # Therefore CDATASection() will be treated as an instance
                # of Text() by minidom. So you have to distinguish by
                # nodeType. These two cases are exhaustive.
                if node.nodeType == Node.TEXT_NODE:
                    self._process_text_node(node)
                else:
                    self._process_cdata_section_node(node)
            # The following case is commented out, because xml.dom.minidom
            # uses an expat-based parser, which will resolve all
            # entity references. Thus, EntityReference is not
            # implemented in xml.dom.minidom - added for completeness.
            # case EntityReference():
            #    self._process_entity_reference_node(node)
            case Entity():
                self._process_entity_node(node)
            case ProcessingInstruction():
                self._process_processing_instruction_node(node)
            case Comment():
                self._process_comment_node(node)
            case Document():
                self._process_document_node(node)
            case DocumentType():
                self._process_document_type_node(node)
            case DocumentFragment():
                self._process_document_fragment_node(node)
            case Notation():
                self._process_notation_node(node)
            case _:
                raise TypeError(f"Wrong node type: {repr(node)}")

    def _process_element_node(self, node: Element) -> None:
        raise NotImplementedError("_process_element_node is not implemented")

    def _process_attribute_node(self, node: Attr) -> None:
        raise NotImplementedError("_process_attribute_node is not implemented")

    def _process_text_node(self, node: Text) -> None:
        raise NotImplementedError("_process_text_node is not implemented")

    def _process_cdata_section_node(self, node: CDATASection) -> None:
        raise NotImplementedError("_process_cdata_section_node is not implemented")

    def _process_entity_node(self, node: Entity) -> None:
        raise NotImplementedError("_process_entity_node is not implemented")

    def _process_processing_instruction_node(self, node: ProcessingInstruction) -> None:
        raise NotImplementedError("_process_processing_instruction_node is not implemented")

    def _process_comment_node(self, node: Comment) -> None:
        raise NotImplementedError("_process_comment_node is not implemented")

    def _process_document_node(self, node: Document) -> None:
        pass

    def _process_document_type_node(self, node: DocumentType) -> None:
        raise NotImplementedError("_process_document_type_node is not implemented")

    def _process_document_fragment_node(self, node: DocumentFragment) -> None:
        raise NotImplementedError("_process_document_fragment_node is not implemented")

    def _process_notation_node(self, node: Notation) -> None:
        raise NotImplementedError("_process_notation_node is not implemented")

    # def process_element_node(self, node) -> None:
    #     self.process_element_start_tag(node)
    #     self.process_all_child_nodes(node)
    #     self.process_element_end_tag(node)
    #
    # def process_element_start_tag(self, node) -> None:
    #     if self.is_inline_element(node):
    #         self.process_inline_element_start_tag(node)
    #     else:
    #         self.process_container_element_start_tag(node)
    #
    # def process_inline_element_start_tag(self, node) -> None:
    #     self.determine_inline_element_indentation(node)
    #     self.open_start_tag(node)
    #     self.process_element_attributes(node)
    #     self.close_start_tag(node)
    #
    # def process_container_element_start_tag(self, node) -> None:
    #     self._result.append("\n" + self.calculate_indentation())
    #     self.open_start_tag(node)
    #     self.process_element_attributes(node)
    #     self.close_start_tag(node)
    #     self._result.append("\n")
    #     if not self.is_empty_element(node):
    #         self.increase_indentation_level()
    #
    # def determine_inline_element_indentation(self, node) -> None:
    #     # ToDO: split this function up to make it more readable
    #     # Depending on its context in the parent node, an inline-element has
    #     # to be indented.
    #     previous = node.previousSibling
    #     # Indent if it is the first child of its parent
    #     if previous is None:
    #         self._result.append(self.calculate_indentation())
    #     # Indent if it follows immediately after a comment (4),
    #     # processing instruction (7) or cdata (8) node
    #     elif previous.nodeType in (4, 7, 8):
    #         self._result.append(self.calculate_indentation())
    #     # Indent if it follows a text node (3) consisting of whitespace that
    #     # follows a comment or cdata node
    #     elif (previous.nodeType == 3 and re.match(r"^\s+$", previous.data)) and (
    #         previous.previousSibling is not None
    #         and previous.previousSibling.nodeType in (4, 7, 8)
    #     ):
    #         self._result.append(self.calculate_indentation())
    #     # Indent if it follows a whitespace text node inside a container element
    #     elif (
    #         (previous.nodeType == 3 and re.match(r"^\s+$", previous.data))
    #         and previous.previousSibling is None
    #         and not self.is_empty_element(node.parentNode)
    #     ):
    #         self._result.append(self.calculate_indentation())
    #
    # def open_start_tag(self, node) -> None:
    #     self._result.append("<" + node.tagName)
    #
    # def process_element_attributes(self, node) -> None:
    #     if node.hasAttributes:
    #         for i in range(node.attributes.length):
    #             self.process(node.attributes.item(i))
    #
    # def close_start_tag(self, node) -> None:
    #     if self.is_empty_element(node):
    #         self._result.append("/>")
    #     else:
    #         self._result.append(">")
    #
    # def process_element_end_tag(self, node) -> None:
    #     if not self.is_empty_element(node):
    #         if self.is_inline_element(node):
    #             self.process_inline_element_end_tag(node)
    #         else:
    #             self.process_container_element_end_tag(node)
    #
    # def process_inline_element_end_tag(self, node) -> None:
    #     self._result.append("</" + node.tagName + ">")
    #
    # def process_container_element_end_tag(self, node) -> None:
    #     self.decrease_indentation_level()
    #     self._result.append(
    #         "\n" + self.calculate_indentation() + "</" + node.tagName + ">\n"
    #     )
    #
    # def process_all_child_nodes(self, node) -> None:
    #     if not self.is_empty_element(node):
    #         for child_node in node.childNodes:
    #             self.process(child_node)
    #
    # def process_attribute_node(self, node) -> None:
    #     self._result.append(" " + node.nodeName + '="' + node.nodeValue + '"')
    #
    # def process_text_node(self, node) -> None:
    #     if self.is_inline_element(node.parentNode):
    #         self.process_text_node_inside_inline_element(node)
    #     else:
    #         self.process_text_node_inside_container_element(node)
    #
    # def process_text_node_inside_inline_element(self, node) -> None:
    #     node.data = sm.reduce_redundant_whitespace(node.data)
    #     node.data = node.data.strip()
    #     self._result.append(node.data)
    #
    # def process_text_node_inside_container_element(self, node) -> None:
    #     node.data = sm.reduce_redundant_whitespace(node.data)
    #     if node.data != " ":
    #         self.process_text_node_depending_on_context(node)
    #     else:
    #         pass
    #
    # def process_text_node_depending_on_context(self, node) -> None:
    #     if self.is_indentation_needed(node.previousSibling):
    #         node.data = self.calculate_indentation() + node.data.lstrip()
    #     self._result.append(node.data)
    #
    # def is_indentation_needed(self, context) -> bool:
    #     # A text node inside a container element should be indented when one of
    #     # these context requirements is met:
    #     # 1) It is the first child node of its parent
    #     # 2) The previous node is a CDATA (4), processing instruction (7) or
    #     #    comment (8) node,
    #     # 3) The previous node is a container element (1)
    #     if (
    #         context is None
    #         or context.nodeType in (4, 7, 8)
    #         or (context.nodeType == 1 and not self.is_inline_element(context))
    #     ):
    #         return True
    #     else:
    #         return False
    #
    # def process_cdata_node(self, node) -> None:
    #     self._result.append(
    #         "\n" + self.calculate_indentation() + "<![CDATA[" + node.nodeValue + "]]>\n"
    #     )
    #
    # def process_entity_reference_node(self, node) -> None:
    #     # ToDo: Implement this to support entity reference nodes
    #     pass
    #
    # def process_entity_node(self, node) -> None:
    #     # ToDo: Implement this to support entity nodes
    #     pass
    #
    # def process_processing_instruction_node(self, node) -> None:
    #     node.data = sm.reduce_redundant_whitespace(node.data)
    #     node.data = node.data.strip()
    #     self._result.append(
    #         "\n"
    #         + self.calculate_indentation()
    #         + "<?"
    #         + node.target
    #         + " "
    #         + node.data
    #         + "?>\n"
    #     )
    #
    # def process_comment_node(self, node) -> None:
    #     node.data = sm.reduce_redundant_whitespace(node.data)
    #     self._result.append(
    #         "\n" + self.calculate_indentation() + "<!--" + node.data + "-->\n"
    #     )
    #
    # def process_document_node(self, node) -> None:
    #     self.process_all_child_nodes(node)
    #
    # def process_document_type_node(self, node) -> None:
    #     self._result.append("<!DOCTYPE " + node.name + " ")
    #     self.process_document_type_external_id(node)
    #     self.process_document_type_internal_subset(node)
    #     self._result.append(">")
    #
    # def process_document_type_external_id(self, node) -> None:
    #     if node.publicId:
    #         self.process_document_type_public_id(node)
    #     elif node.systemId:
    #         self.process_document_type_system_id(node)
    #
    # def process_document_type_public_id(self, node) -> None:
    #     self._result.append('PUBLIC "' + node.publicId + '" "' + node.systemId + '" ')
    #
    # def process_document_type_system_id(self, node) -> None:
    #     self._result.append('SYSTEM "' + node.systemId + '" ')
    #
    # def process_document_type_internal_subset(self, node) -> None:
    #     # ToDO: split this function up to make it more readable
    #     if node.internalSubset:
    #         self.increase_indentation_level()
    #         subset = node.internalSubset
    #         subset = " ".join(subset.split())
    #         subset = subset.replace("<!", "\n" + self.calculate_indentation() + "<!")
    #         subset = subset.replace("<?", "\n" + self.calculate_indentation() + "<?")
    #         self._result.append("[" + subset + "\n]")
    #         self.decrease_indentation_level()
    #
    # def process_document_fragment_node(self, node) -> None:
    #     # ToDo: Implement this to support document fragment nodes
    #     pass
    #
    # def process_notation_node(self, node) -> None:
    #     # ToDo: Implement this to support notation nodes
    #     pass
    #
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
    # # Functions for processing the indentation
    # def calculate_indentation(self) -> int:
    #     return self._indentation_level * self.options.indentation * " "
    #
    # def decrease_indentation_level(self) -> None:
    #     self._indentation_level -= 1
    #
    # def increase_indentation_level(self) -> None:
    #     self._indentation_level += 1
    #
    # # Functions for processing the different element types
    # def is_empty_element(self, node) -> bool:
    #     # An element is empty if one of these requirements is met:
    #     # 1) it has no child nodes at all
    #     # 2) it has exactly one child node, that is a text (3) node consisting
    #     #    of whitespace only
    #     match node.childNodes.length:
    #         case 0:
    #             return True
    #         case 1:
    #             if self.check_if_node_is_whitespace_only(node):
    #                 return True
    #             else:
    #                 return False
    #         case _:
    #             return False
    #
    # @staticmethod
    # def check_if_node_is_whitespace_only(node) -> bool:
    #     if (
    #         node.firstChild.nodeType == 3
    #         and sm.remove_whitespace(node.firstChild.data) == ""
    #     ):
    #         return True
    #     else:
    #         return False
    #
    # def is_inline_element(self, node: minidom.Element) -> bool:
    #     if (
    #         self.options.inline_elements is not None
    #         and node.tagName in self.options.inline_elements
    #     ):
    #         return True
    #
    #     return False
