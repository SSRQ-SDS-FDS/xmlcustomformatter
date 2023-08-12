import re as regex
from xml.dom import minidom
from xmlformattingoptions import XMLFormattingOptions


class XMLCustomFormatter:
    def __init__(self, input_file, output_file, formatting_options=None):
        self.input_file = input_file
        self.output_file = output_file
        self.formatting_options = formatting_options or XMLFormattingOptions()
        self.indentation_level = 0
        self.result = None
        self.dom = None
        self.format()

    def format(self):
        self.read_input_file_to_dom()
        self.add_xml_declaration()
        self.process(self.dom)
        self.postprocess()
        self.write_to_output_file()

    def read_input_file_to_dom(self):
        self.dom = minidom.parse(self.input_file)

    def add_xml_declaration(self):
        # This is necessary because XML DOM does process XML-declarations.
        # If there was one present in the input document, the parser would
        # just ignore it. Adding this declaration makes sure, that there
        # is one in the output document.
        self.result = ['<?xml version="1.0" encoding="UTF-8"?>\n']

    def process(self, node):
        match node.nodeType:
            case 1:
                self.process_element_node(node)
            case 2:
                self.process_attribute_node(node)
            case 3:
                self.process_text_node(node)
            case 4:
                self.process_cdata_node(node)
            case 5:
                # ToDo: Entity Reference Node
                pass
            case 6:
                # ToDo: Entity Node
                pass
            case 7:
                self.process_processing_instruction_node(node)
            case 8:
                self.process_comment_node(node)
            case 9:
                self.process_document_node(node)
            case 10:
                self.process_document_type_node(node)
            case 11:
                # ToDo: Document Fragment Node
                pass
            case 12:
                # ToDo: Notation Node
                pass

    def process_attribute_node(self, node):
        self.result.append(' ' + node.nodeName + '="' + node.nodeValue + '"')

    def process_cdata_node(self, node):
        self.result.append("\n" + self.calculate_indentation() + "<![CDATA[" + node.nodeValue + ']]>\n')

    def process_comment_node(self, node):
        node.data = self.reduce_redundant_whitespace(node.data)
        self.result.append('\n' + self.calculate_indentation() + '<!--' + node.data + '-->\n')

    def process_document_node(self, node):
        self.process_children(node)

    def process_document_type_node(self, node):
        self.result.append("<!DOCTYPE " + node.name + " ")
        self.process_document_type_external_id(node)
        self.process_document_type_internal_subset(node)
        self.result.append(">")

    def process_document_type_external_id(self, node):
        if node.publicId:
            self.result.append('PUBLIC "' + node.publicId + '" "' + node.systemId + '" ')
        elif node.systemId:
            self.result.append('SYSTEM "' + node.systemId + '" ')

    def process_document_type_internal_subset(self, node):
        if node.internalSubset:
            self.increase_indentation_level()
            subset = node.internalSubset
            subset = " ".join(subset.split())
            subset = subset.replace("<!", "\n" + self.calculate_indentation() + "<!")
            subset = subset.replace("<?", "\n" + self.calculate_indentation() + "<?")
            self.result.append('[' + subset + '\n]')
            self.decrease_indentation_level()

    def process_element_node(self, node):
        self.process_element_start_tag(node)
        if not self.is_empty_element(node):
            self.process_children(node)
            self.process_element_end_tag(node)

    def process_element_start_tag(self, node):
        if self.is_inline_element(node):
            self.process_inline_element_start_tag(node)
        else:
            self.process_container_element_start_tag(node)

    def process_container_element_start_tag(self, node):
        self.result.append('\n' + self.calculate_indentation() + '<' + node.tagName)
        self.process_element_attributes(node)
        self.close_start_tag(node)
        self.result.append('\n')
        if not self.is_empty_element(node):
            self.increase_indentation_level()

    def process_inline_element_start_tag(self, node):
        self.determine_inline_element_indentation(node)
        self.open_start_tag(node)
        self.process_element_attributes(node)
        self.close_start_tag(node)

    def determine_inline_element_indentation(self, node):
        # Depending on its context in the parent node, an inline-element has to be indented.
        previous = node.previousSibling
        # Indent if it is the first child of its parent
        if previous is None:
            self.result.append(self.calculate_indentation())
        # Indent if it follows immediately after a comment (4), processing instruction (7) or cdata (8) node
        elif previous.nodeType in (4, 7, 8):
            self.result.append(self.calculate_indentation())
        # Indent if it follows a text node (3) consisting of whitespace that follows a comment or cdata node
        elif (previous.nodeType == 3 and regex.match(r"^\s+$", previous.data)) \
                and (previous.previousSibling is not None and previous.previousSibling.nodeType in (4, 7, 8)):
            self.result.append(self.calculate_indentation())
        # Indent if it follows a whitespace text node inside a container element
        elif (previous.nodeType == 3 and regex.match(r"^\s+$", previous.data)) \
                and previous.previousSibling is None \
                and not self.is_empty_element(node.parentNode):
            self.result.append(self.calculate_indentation())

    def open_start_tag(self, node):
        self.result.append('<' + node.tagName)

    def close_start_tag(self, node):
        if self.is_empty_element(node):
            self.result.append('/>')
        else:
            self.result.append('>')

    def process_element_attributes(self, node):
        if node.hasAttributes:
            for i in range(node.attributes.length):
                self.process(node.attributes.item(i))

    def process_children(self, node):
        for child_node in node.childNodes:
            self.process(child_node)

    def process_element_end_tag(self, node):
        if self.is_inline_element(node):
            self.process_inline_element_end_tag(node)
        else:
            self.process_container_element_end_tag(node)

    def process_container_element_end_tag(self, node):
        self.decrease_indentation_level()
        self.result.append('\n' + self.calculate_indentation() + '</' + node.tagName + '>\n')

    def process_inline_element_end_tag(self, node):
        self.result.append('</' + node.tagName + '>')

    def process_processing_instruction_node(self, node):
        node.data = self.reduce_redundant_whitespace(node.data)
        node.data = node.data.strip()
        self.result.append('\n' + self.calculate_indentation() + '<?' + node.target + ' ' + node.data + '?>\n')

    def process_text_node(self, node):
        if self.is_inline_element(node.parentNode):
            self.process_inline_element_text(node)
        else:
            self.process_container_element_text(node)

    def process_container_element_text(self, node):
        node.data = self.reduce_redundant_whitespace(node.data)
        if node.data != " ":
            previous = node.previousSibling
            if previous is None or previous.nodeType in (4, 7, 8) or \
                    (previous.nodeType == 1 and not self.is_inline_element(previous)):
                node.data = self.calculate_indentation() + node.data.lstrip()
            self.result.append(node.data)

    def process_inline_element_text(self, node):
        node.data = self.reduce_redundant_whitespace(node.data)
        node.data = node.data.strip()
        self.result.append(node.data)

    def postprocess(self):
        self.postprocess_rearrange_result()
        self.postprocess_result_lines()
        self.result = self.convert_result_to_string(self.result)
        self.result = self.remove_empty_lines(self.result)
        self.result = self.remove_whitespace_before_end_of_line(self.result)
        self.result = self.result.strip()

    # Functions for postprocessing
    def postprocess_rearrange_result(self):
        self.result = "".join(self.result).split('\n')

    def postprocess_result_lines(self):
        lines = self.result
        self.result = []
        for line in lines:
            self.postprocess_line(line)

    def postprocess_line(self, line: str):
        number_of_spaces = self.get_current_indentation(line)
        if number_of_spaces > 0:
            indentation = number_of_spaces * " "
        else:
            indentation = ""
        if len(line) <= self.formatting_options.max_line_length:
            self.result.append(line)
        else:
            if " " in line:
                position = line.rfind(" ", number_of_spaces, self.formatting_options.max_line_length)
                if position == -1:
                    position = line.find(" ", self.formatting_options.max_line_length)
                    if position == -1:
                        self.result.append(line)
                    else:
                        self.result.append(line[0:position] + "\n")
                        self.postprocess_line(indentation + line[position:].lstrip())
                else:
                    self.result.append(line[0:position] + "\n")
                    self.postprocess_line(indentation + line[position:].lstrip())
            else:
                self.result.append(line)

    def get_current_indentation(self, string):
        return len(string) - len(string.lstrip())

    def write_to_output_file(self):
        with open(self.output_file, 'w') as output_file:
            output_file.write(self.result)

    # Functions for processing the indentation
    def calculate_indentation(self):
        return self.indentation_level * self.formatting_options.indentation * ' '

    def decrease_indentation_level(self):
        self.indentation_level -= 1

    def increase_indentation_level(self):
        self.indentation_level += 1

    # Functions for processing the different element types
    def is_empty_element(self, node):
        # An element is empty if it either has no child nodes at all
        # or if it has exactly one text node (constant: 3) with just
        # whitespaces as a child.
        match node.childNodes.length:
            case 0:
                return True
            case 1:
                if node.firstChild.nodeType == 3 and self.remove_whitespace(node.firstChild.data) == "":
                    return True
                else:
                    return False
            case _:
                return False

    def is_inline_element(self, node):
        if node.tagName in self.formatting_options.inline_elements:
            return True
        else:
            return False

    # Functions for processing whitespace
    @staticmethod
    def reduce_redundant_whitespace(string: str):
        return regex.sub(r"\s+", " ", string)

    @staticmethod
    def remove_whitespace(string: str):
        return regex.sub(r"\s", "", string)

    @staticmethod
    def remove_empty_lines(string: str):
        return regex.sub(r"\n+", "\n", string)

    @staticmethod
    def remove_whitespace_before_end_of_line(string: str):
        return regex.sub(r"\s+\n", "\n", string)

    # Other functions
    @staticmethod
    def convert_result_to_string(result: list):
        return "\n".join(result)
