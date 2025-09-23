"""This module contains the XMLCustomFormatter class."""

import re
from pathlib import Path
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
        input_xml (str): Path to the input XML file to be read or an XML string.
        output_xml (str, optional): Path to the file where the formatted XML will be saved.
            If not provided, the result can be accesses via get_result_as_list or
            get_result_as_string.
        options (Options, optional): Configuration options for formatting.
            If not provided, default Options() will be used.

    Default values:
        If no information is provided in the XML to be processed, then
        XML Version 1.0, encoding UTF-8 and an empty standalone declaration are used.
    """

    default_version: str = "1.0"
    default_encoding: str = "UTF-8"
    default_standalone: str = ""

    def __init__(
        self,
        input_xml: str,
        output_xml: Optional[str] = None,
        options: Optional[Options] = None,
    ):
        """
        Initializes a XMLCustomFormatter instance.
        The input XML file is automatically parsed with the built-in
        minidom parser and formatted.
        The processing takes place in two phases:
        First: all nodes of the parsed dom are processed, such that
            the markup is written into the result, indentation levels are calculated
            and the distribution of the markup to lines is made
        Second: the result from the first step is postprocessed to
            remove empty lines and to split lines, which are too long
            into smaller lines which are less or equal than the max_line_length option.
        """

        self.input = input_xml
        self.output = output_xml
        self.options = options or Options()

        self._dom = self._parse_input(self.input)
        self._encoding = self._dom.encoding or self.default_encoding
        self._indentation_level: int = 0
        self._result: list[str] = []

        self._process_node(self._dom)
        self._postprocess()

        if self.output:
            self._write_to_output_file(self.output, self._encoding, self._result)

    def _parse_input(self, input_xml: str) -> Document:
        """
        Parses the input into a minidom Document.

        If `input_xml` is a valid file path, the file will be parsed.
        Otherwise, the string is assumed to contain XML and will be parsed.
        """
        try:
            path = Path(input_xml)
            if path.is_file():
                return self._parse_from_file(path)
        except (OSError, TypeError, ValueError):
            pass

        return self._parse_from_string(input_xml)

    @staticmethod
    def _parse_from_file(path: Path) -> Document:
        try:
            return minidom.parse(str(path))
        except Exception as e:
            raise ValueError(f"File '{path}' exists but could not be parsed as XML: {e}") from e

    @staticmethod
    def _parse_from_string(string: str) -> Document:
        try:
            return minidom.parseString(string)
        except Exception as e:
            raise ValueError(
                f"`input_xml` is neither a valid file path nor a well-formed XML-String: {e}"
            ) from e

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
            #     # Thus, it is not necessary to process this kind of node while formatting.
            #     pass

    def _process_all_child_nodes(self, node: Node) -> None:
        """
        Iterates over all existing child nodes and calls the main processing method.
        Adds indentation to child nodes depending on context.
        """
        for child in node.childNodes:
            if self._needs_indentation(child):
                self._add_indentation()
            self._process_node(child)

    def _needs_indentation(self, child: Node) -> bool:
        """Returns True if the child should be indented before processing."""
        return (
            self.needs_indent_for_first_child(child)
            and self.needs_indent_after_special_sibling(child)
            and self.needs_indent_for_text(child)
        )

    def needs_indent_for_first_child(self, child: Node) -> bool:
        """Indentation is required if the child is not the first child of a
        semicontainer or inline element."""
        return not (
            child.previousSibling is None
            and isinstance(child.parentNode, Element)
            and (
                self._is_semicontainer_element(child.parentNode)
                or self._is_inline_element(child.parentNode)
            )
        )

    def needs_indent_after_special_sibling(self, child: Node) -> bool:
        """Indentation is required unless the child follows a semicontainer or inline element."""
        return not (
            child.previousSibling is not None
            and isinstance(child.previousSibling, Element)
            and (
                self._is_semicontainer_element(child.previousSibling)
                or self._is_inline_element(child.previousSibling)
            )
        )

    def needs_indent_for_text(self, child: Node) -> bool:
        """
        Indentation is required unless the child is an inline element or text
        following another text (e.g. two CDATA nodes in sequence).
        """
        return not (
            child.previousSibling is not None
            and (
                (isinstance(child, Element) and self._is_inline_element(child))
                or isinstance(child, Text)
            )
            and isinstance(child.previousSibling, Text)
        )

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
        value = SM.escape_xml_entities(attribute.value)
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

        data = SM.escape_xml_entities(data)

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
        """Adds indentation to the result based on the current indentation level"""
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
        result_as_string = "".join(self._result)
        result_as_string = SM.remove_empty_lines(result_as_string)
        result_as_string = SM.remove_whitespace_before_eol(result_as_string)
        result_as_string = result_as_string.strip()

        lines = result_as_string.splitlines(keepends=True)
        lines = self._split_too_long_lines(lines)

        self._result = lines

    def _split_too_long_lines(self, lines: list[str]) -> list[str]:
        """
        Splits long lines safely at the last whitespace before max_line_length,
        preserving indentation. If no whitespace is found, the line remains as is.
        """
        result: list[str] = []

        for line in lines:
            indent = line[: len(line) - len(line.lstrip(" "))]

            # Split line while it is longer than max_line_length
            while len(line) > self.options.max_line_length:
                old_length = len(line)

                split_at = self._find_split_position(line)
                if split_at is None:
                    break

                current_line = line[:split_at].rstrip()

                line = indent + line[split_at + 1 :].lstrip()

                # If the line does not get shorter end the loop to prevent endless iterations
                new_length = len(line)
                if not new_length < old_length:
                    break

                result.append(current_line + "\n")

            result.append(line)

        return result

    def _find_split_position(self, line: str) -> int | None:
        """
        Returns an index, where the line should be split.

        Prefers the last whitespace before max_line_length,
        otherwise the first one after it.

        Returns None if no whitespace is found at all.
        """
        result = line.rfind(" ", 0, self.options.max_line_length)
        if result != -1:
            return result

        result = line.find(" ", self.options.max_line_length)
        if result != -1:
            return result

        return None

    @staticmethod
    def _write_to_output_file(output_file: str, encoding: str, result: list[str]) -> None:
        """Writes the collected result to the output file."""
        with open(output_file, "w", encoding=encoding) as f:
            f.writelines(result)
