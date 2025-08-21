"""This module contains the XMLCustomFormatter class."""

import re
from typing import Optional, cast
from xml.dom import minidom
from xml.dom.minidom import (
    Node,
    Element,
    Attr,
    Text,
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
        self._encoding = self._dom.encoding or self.default_encoding
        self._indentation_level: int = 0
        self._result: list[str] = []
        self._process_node(self._dom)
        self._postprocess()
        self._write_to_output_file()

    def get_result_as_list(self) -> list[str]:
        """Returns the result as a list of strings."""
        return self._result

    def get_result_as_string(self) -> str:
        """Returns the result as a concatenated string."""
        return "".join(self._result)

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
                self._process_text_node(node)
            case _:
                raise TypeError(f"Wrong node type: {repr(node)}")
            #
            # The following cases are commented out because of different reasons:
            #
            # case CDATASection():
            #     # This case cannot be reached as CDATASection is a child class
            #     # of Text sharing the same interface as Text. Thus, every CDATASection
            #     # in the XML will be parsed into a Text object. Therefore, cf.
            #     # case Text() for processing of CDATASections.
            #     pass
            #
            # case DocumentFragment():
            #     # The following case is commented out, because xml.dom.minidom
            #     # uses DocumentFragment as a helper class when constructing
            #     # structures to be added to an existing Document object.
            #     # This node type cannot be found in a parsed XML file.
            #     pass
            #
            # case Entity():
            #     # This case is commented out, because xml.dom.minidom
            #     # uses the class Entity as a helper class, if one wants to
            #     # manually create such nodes.
            #     # This node type may be found in the DocumentType.entities node map,
            #     # but because it is also part of the document type declaration,
            #     # it will be part of the DocumentType.internalSubset property.
            #     # Thus it is not necessary to process this kind of node while formatting.
            #     pass
            #
            # case EntityReference():
            #     # This case cannot be reached as xml.dom.minidom uses an expat-based
            #     # parser, which will resolve all entity references. Thus, EntityReference
            #     # is not implemented in xml.dom.minidom.
            #     pass
            #
            # case Notation():
            #     # The following case is commented out, because xml.dom.minidom
            #     # uses the class Notation as a helper class, if one wants to
            #     # manually create such nodes.
            #     # This node type may be found in the DocumentType.notations node map,
            #     # but because it is also part of the document type declaration,
            #     # it will be part of DocumentType.internalSubset property.
            #     # Thus it is not necessary to process this kind of node while formatting.
            #     pass

    def _process_all_child_nodes(self, node: Node) -> None:
        """
        Iterates over all existing child nodes and calls the main processing method.
        Adds indentation to all child nodes depending on context.
        """
        for child in node.childNodes:
            # No indentation for first child in semicontainer or inline element
            if (
                child.previousSibling is None
                and isinstance(child.parentNode, Element)
                and (
                    self._is_semicontainer_element(child.parentNode)
                    or self._is_inline_element(child.parentNode)
                )
            ):
                self._process_node(child)
                continue

            # No indentation for any child after semicontainer or inline element
            if (
                child.previousSibling is not None
                and isinstance(child.previousSibling, Element)
                and (
                    self._is_semicontainer_element(child.previousSibling)
                    or self._is_inline_element(child.previousSibling)
                )
            ):
                self._process_node(child)
                continue

            # No indentation for inline-elements or text after text (e. g. two CDATA nodes
            if (
                child.previousSibling is not None
                and (
                    (isinstance(child, Element) and self._is_inline_element(child))
                    or isinstance(child, Text)
                )
                and isinstance(child.previousSibling, Text)
            ):
                self._process_node(child)
                continue

            self._add_indentation()
            self._process_node(child)

    def _process_element_node(self, element: Element) -> None:
        """Processes all element nodes depending on emptiness and element group."""
        empty = self._is_empty_element(element)

        if self._is_inline_element(element):
            group = "inline"
        elif self._is_semicontainer_element(element):
            group = "semicontainer"
        else:
            group = "container"

        method_map = {
            ("inline", True): self._process_empty_inline_element,
            ("inline", False): self._process_nonempty_inline_element,
            ("semicontainer", True): self._process_empty_semicontainer_element,
            ("semicontainer", False): self._process_nonempty_semicontainer_element,
            ("container", True): self._process_empty_container_element,
            ("container", False): self._process_nonempty_container_element,
        }

        method = method_map[(group, empty)]
        method(element)

    def _process_empty_inline_element(self, element: Element) -> None:
        """Processes inline elements which are empty."""
        self._open_start_tag(element)
        self._process_attributes(element)
        self._close_empty_tag()

    def _process_nonempty_inline_element(self, element: Element) -> None:
        """Processes inline elements which have child nodes."""
        self._open_start_tag(element)
        self._process_attributes(element)
        self._close_start_tag()
        self._increase_indentation_level()
        self._process_all_child_nodes(element)
        # If the content of the element ends with a linebreak
        # then the end tag has to be indented
        if self._result_endswith_linebreak():
            self._add_indentation()
        self._decrease_indentation_level()
        self._process_element_end_tag(element)

    def _process_empty_container_element(self, element: Element) -> None:
        """Processes container elements which are empty."""
        self._add_linebreak()
        self._add_indentation()
        self._open_start_tag(element)
        self._process_attributes(element)
        self._close_empty_tag()
        self._add_linebreak()

    def _process_nonempty_container_element(self, element: Element) -> None:
        """Processes container elements which have child nodes."""
        self._add_linebreak()
        self._add_indentation()
        self._open_start_tag(element)
        self._process_attributes(element)
        self._close_start_tag()
        self._increase_indentation_level()
        self._add_linebreak()
        self._process_all_child_nodes(element)
        self._decrease_indentation_level()
        self._add_linebreak()
        self._add_indentation()
        self._process_element_end_tag(element)
        self._add_linebreak()

    def _process_empty_semicontainer_element(self, element: Element) -> None:
        """Processes semi container elements which are empty."""
        self._add_linebreak()
        self._add_indentation()
        self._open_start_tag(element)
        self._process_attributes(element)
        self._close_empty_tag()

    def _process_nonempty_semicontainer_element(self, element: Element) -> None:
        """Processes semi container elements which have child nodes."""
        self._add_linebreak()
        self._add_indentation()
        self._open_start_tag(element)
        self._process_attributes(element)
        self._close_start_tag()
        self._increase_indentation_level()
        self._process_all_child_nodes(element)
        # If the content of the element ends with a linebreak
        # then the end tag has to be indented
        if self._result_endswith_linebreak():
            self._add_indentation()
        self._decrease_indentation_level()
        self._process_element_end_tag(element)

    def _is_inline_element(self, element: Element) -> bool:
        """Determines whether an element is an inline element."""
        if (
            self.options.inline_elements is not None
            and element.tagName in self.options.inline_elements
        ):
            return True
        return False

    def _is_semicontainer_element(self, element: Element) -> bool:
        """Determines whether an element is a semi container element."""
        if (
            self.options.semicontainer_elements is not None
            and element.tagName in self.options.semicontainer_elements
        ):
            return True
        return False

    def _process_element_end_tag(self, element: Element) -> None:
        """Processes the end tag of a non-empty element."""
        self._result.append(f"</{element.tagName}>")

    def _open_start_tag(self, element: Element) -> None:
        """Opens the start tag of a non-empty element or the empty tag of an empty element."""
        self._result.append(f"<{element.tagName}")

    def _close_start_tag(self) -> None:
        """Closes the start tag of a non-empty element."""
        self._result.append(">")

    def _close_empty_tag(self) -> None:
        """Closes the empty tag of an empty element."""
        self._result.append("/>")

    def _process_attributes(self, element: Element) -> None:
        """Processes attributes of the given element, optionally sorted by name."""
        if element.hasAttributes():
            attributes = []
            for i in range(element.attributes.length):
                attribute = element.attributes.item(i)
                if attribute is not None:
                    attributes.append(cast(Attr, attribute))

            if self.options.sorted_attributes:
                attributes.sort(key=lambda attr: attr.name)

            for attribute in attributes:
                self._process_node(attribute)

    def _process_attribute_node(self, attribute: Attr) -> None:
        """Processes an attribute node and escapes double quotes inside the attribute value."""
        name = attribute.name
        value = SM.escape_double_quotes(attribute.value)
        self._result.append(f' {name}="{value}"')

    def _process_text_node(self, text: Text) -> None:
        """
        Delegates the processing of a text to specialized methods for
        text nodes and cdata nodes.
        """
        # CDATASection shares the same interface as Text.
        # Therefore, CDATASection will be treated as an instance
        # of Text by minidom. So you have to disambiguate any Text
        # object by its nodeType property.
        # These two cases are exhaustive.
        if text.nodeType == Node.TEXT_NODE:
            self._process_text(text)
        else:
            self._process_cdata_section(text)

    def _process_text(self, text: Text) -> None:
        """Processes a text node by reducing redundant whitespace."""
        data = SM.reduce_redundant_whitespace(text.data)

        if self._result_endswith_whitespace():
            data = data.lstrip()

        self._result.append(data)

    def _result_endswith_linebreak(self) -> bool:
        return self._result[-1].endswith("\n")

    def _result_endswith_whitespace(self) -> bool:
        return self._result[-1].endswith(("\n", " ", "\t", "\r"))

    def _process_cdata_section(self, cdata: Text) -> None:
        """
        Processes a CDATASection by reducing redundant whitespace
        and stripping leading and trailing whitespace.
        """
        data = SM.reduce_redundant_whitespace(cdata.data)
        data = data.strip()
        self._result.append(f"<![CDATA[{data}]]>")

    def _process_processing_instruction_node(self, pi: ProcessingInstruction) -> None:
        """Processes processing instruction nodes."""
        newline = self._set_processing_instruction_newline()
        indentation = self._indentation(self._calculate_indentation())
        target = pi.target
        data = self._normalize_processing_instruction_data(pi)
        self._result.append(f"{newline}{indentation}<?{target}{data}?>{newline}")

    @staticmethod
    def _normalize_processing_instruction_data(pi: ProcessingInstruction) -> str:
        """Normalizes the data part of a processing instruction by reducing redundant whitespace."""
        return " " + SM.reduce_redundant_whitespace(pi.data).strip()

    def _set_processing_instruction_newline(self) -> str:
        """
        Determines whether processing instructions start on new lines
        and returns a linebreak or empty string.
        """
        return "\n" if self.options.processing_instructions_start_new_lines else ""

    def _process_comment_node(self, comment: Comment) -> None:
        """Processes comment nodes."""
        newline = self._set_comment_newline()
        indentation = self._indentation(self._calculate_indentation())
        start = self._set_comment_start()
        data = self._normalize_comment_data(comment)
        end = self._set_comment_end()
        self._result.append(f"{newline}{indentation}{start}{data}{end}{newline}")

    @staticmethod
    def _normalize_comment_data(comment: Comment) -> str:
        """
        Normalizes the data of an XML comment by reducing redundant whitespace
        and stripping leading and trailing whitespaces.
        """
        data = SM.reduce_redundant_whitespace(comment.data)
        data = data.strip()
        return data

    def _set_comment_newline(self) -> str:
        """
        Determines whether comments start on new lines
        and returns a linebreak or empty string.
        """
        return "\n" if self.options.comments_start_new_lines else ""

    def _set_comment_start(self) -> str:
        """
        Determines whether comments should have leading whitespace and
        returns the start with or without leading whitespace.
        """
        return "<!-- " if self.options.comments_have_trailing_spaces else "<!--"

    def _set_comment_end(self) -> str:
        """
        Determines whether comments should have trailing whitespace and
        returns the end with or without trailing whitespace.
        """
        return " -->" if self.options.comments_have_trailing_spaces else "-->"

    def _process_document_node(self, node: Document) -> None:
        """
        Processes the complete document by constructing the XML declaration,
        which is not a node itself and recursively iterating all child nodes.
        """
        self._process_xml_declaration()
        self._process_all_child_nodes(node)

    def _process_xml_declaration(self) -> None:
        """
        Processes the XML declaration. If version, encoding or standalone are not
        set, then default values will be used. The declaration is appended to the result.
        """
        version = self._set_version()
        encoding = self._set_encoding()
        standalone = self._set_standalone()
        self._result.append(f"<?xml{version}{encoding}{standalone}?>\n")

    def _set_encoding(self) -> str:
        """Sets the encoding part of the XML declaration."""
        if self._dom.encoding is None:
            return f' encoding="{self.default_encoding}"'
        return f' encoding="{self._dom.encoding}"'

    def _set_standalone(self) -> str:
        """Sets the standalone part of the XML declaration."""
        if self._dom.standalone is None:
            return self.default_standalone

        if self._dom.standalone:
            return ' standalone="yes"'

        return ' standalone="no"'

    def _set_version(self) -> str:
        """Sets the version part of the XML declaration."""
        if self._dom.version is None:
            return f' version="{self.default_version}"'
        return f' version="{self._dom.version}"'

    def _process_document_type_node(self, doc_type: DocumentType) -> None:
        """Processes document type nodes."""
        newline = self._set_doctype_newline()
        external_id = self._construct_external_id(doc_type.publicId, doc_type.systemId)
        subset = self._construct_internal_subset(doc_type.internalSubset)
        self._result.append(f"{newline}<!DOCTYPE {doc_type.name}{external_id}{subset}>{newline}")

    def _set_doctype_newline(self) -> str:
        """
        Determines whether doctype declarations start on new lines
        and returns a linebreak or empty string.
        """
        return "\n" if self.options.doctype_declaration_starts_new_line else ""

    @staticmethod
    def _construct_external_id(public_id: str | None, system_id: str | None) -> str:
        """
        Constructs the external id depending on the existence of the
        public id part and the system id part.
        """
        if public_id is not None:
            return f' PUBLIC "{public_id}" "{system_id}"'

        if system_id is not None:
            return f' SYSTEM "{system_id}"'

        return ""

    def _construct_internal_subset(self, subset: str | None) -> str:
        """
        Determines whether an internal subset exists and returns either an empty string
        or the complete formatted subset.
        """
        if subset is None or subset == "":
            return ""

        if not self.options.doctype_subset_parts_start_new_lines:
            return f" [{subset}]"

        self._increase_indentation_level()
        indentation = self._indentation(self._calculate_indentation())
        self._decrease_indentation_level()

        # These are all valid constituents of a doctype declaration
        # according to the XML version 1.0 specification
        patterns = [
            r"<!ELEMENT[^>]*?>",  # element declarations
            r"<!ENTITY[^>]*?>",  # entity declarations
            r"<!ATTLIST[^>]*?>",  # attlist declarations
            r"<!NOTATION[^>]*?>",  # notation declarations
            r"<!--.*?-->",  # comments
            r"<\?.*?\?>",  # processing instructions
            r"%\w+;",  # pe-references
        ]
        combined_pattern = f"({'|'.join(patterns)})"
        parts = re.findall(combined_pattern, subset, re.DOTALL)
        formatted_lines = []
        for part in parts:
            formatted_lines.append(indentation + part.strip())
        return f" [\n{'\n'.join(formatted_lines)}\n]"

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
            raise ValueError("Indentation level cannot be lower than zero")
        self._indentation_level -= 1

    def _increase_indentation_level(self) -> None:
        """Increases the indentation level by 1"""
        self._indentation_level += 1

    def _add_indentation(self) -> None:
        """Adds indentation to the result based on the currend indentation level"""
        self._result.append(self._indentation(self._calculate_indentation()))

    def _add_linebreak(self) -> None:
        """Adds a linebreak to the result"""
        self._result.append("\n")

    @staticmethod
    def _is_empty_element(element: Element) -> bool:
        """
        Determines whether an element is empty or not. An element is said to be empty
        if it has no child nodes.
        """
        return not element.hasChildNodes()

    @staticmethod
    def _is_whitespace_only_text(text: Text) -> bool:
        """
        Determines whether a text node consist of whitespace only.
        """
        data = text.data
        return data.strip() == ""

    def _postprocess(self) -> None:
        """Delegates postprocessing of result to specialized methods."""
        self._postprocess_rearrange_result()
        #     self.postprocess_result_lines()
        #     self.postprocess_result_as_string()

    def _postprocess_rearrange_result(self) -> None:
        """Splits the result at newline and removes empty lines."""
        result = "".join(self._result)
        result = SM.remove_empty_lines(result)
        result = SM.remove_whitespace_before_eol(result)
        self._result = result.splitlines(keepends=True)

    def _write_to_output_file(self) -> None:
        """Writes the collected result to the output file."""
        with open(self.output_file, "w", encoding=self._encoding) as f:
            f.writelines(self._result)

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
