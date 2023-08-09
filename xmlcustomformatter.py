from xml.dom import minidom
from xmlformattingoptions import XMLFormattingOptions
import re as regex


class XMLCustomFormatter:
    def __init__(self, input_file, output_file, formatting_options=None):
        self.input_file = input_file
        self.output_file = output_file
        self.formatting_options = formatting_options or XMLFormattingOptions()
        self.indentation_level = 0
        self.result = []
        self.dom = None
        self.format()

    def format(self):
        self.read_input_file_to_dom()
        self.process(self.dom)
        self.postprocess()
        self.write_to_output_file()

    def read_input_file_to_dom(self):
        self.dom = minidom.parse(self.input_file)

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
                self.process_entity_reference_node(node)
            case 6:
                self.process_entity_node(node)
            case 7:
                self.process_processing_instruction_node(node)
            case 8:
                self.process_comment_node(node)
            case 9:
                self.process_document_node(node)
            case 10:
                self.process_document_type_node(node)
            case 11:
                self.process_document_fragment_node(node)
            case 12:
                self.process_notation_node(node)

    def process_attribute_node(self, node):
        self.result.append(' ' + node.nodeName + '="' + node.nodeValue + '"')

    def process_cdata_node(self, node):
        self.append_indentation()
        self.result.append("\n" + self.calculate_indentation() + "<![CDATA[" + node.nodeValue + ']]>\n')

    def process_comment_node(self, node):
        comment = node.data
        comment = comment.replace('\n', ' ')
        comment = regex.sub(r'\s+', ' ', comment)
        self.result.append('\n' + self.calculate_indentation() + '<!--' + comment + '-->\n')

    def process_document_node(self, node):
        for child in node.childNodes:
            self.process(child)

    def process_document_fragment_node(self, node):
        # Todo: Document Fragments
        pass

    def process_document_type_node(self, node):
        self.result.append("<!DOCTYPE " + node.nodeName + " ")
        self.process_document_type_internal_subset(node)
        self.result.append(">")

    def process_document_type_internal_subset(self, node):
        self.indentation_level += 1
        if node.internalSubset:
            subset = node.internalSubset
            indentation = self.calculate_indentation()
            self.result.append('[')
            subset = " ".join(subset.split())
            subset = subset.replace("<!", "\n" + indentation + "<!")
            self.result.append(subset)
            self.result.append(']')
        self.indentation_level -= 1

    def process_element_node(self, node):
        self.process_element_start_tag(node)
        for child in node.childNodes:
            self.process(child)
        if node.childNodes.length != 0:
            self.process_element_end_tag(node)

    def process_element_attributes(self, node):
        if node.hasAttributes:
            number_of_attributes = node.attributes.length
            for i in range(number_of_attributes):
                self.process(node.attributes.item(i))

    def process_element_end_tag(self, node):
        if self.is_inline_element(node):
            self.result.append('</' + node.tagName + '>')
        else:
            self.indentation_level -= 1
            self.result.append('\n')
            self.append_indentation()
            self.result.append('</' + node.tagName + '>\n')

    def process_element_start_tag(self, node):
        if self.is_inline_element(node):
            self.result.append('<' + node.tagName)
            self.process_element_attributes(node)
            if node.childNodes.length == 0:
                self.result.append('/>')
            else:
                self.result.append('>')
        else:
            self.result.append('\n')
            self.append_indentation()
            self.result.append('<' + node.tagName)
            self.process_element_attributes(node)
            if node.childNodes.length == 0:
                self.result.append('/>\n')
            else:
                self.result.append('>\n')
                self.indentation_level += 1

    def process_entity_node(self, node):
        # ToDo: Entities
        pass

    def process_entity_reference_node(self, node):
        # ToDo: Entity References
        pass

    def process_notation_node(self, node):
        # ToDo: Notations
        pass

    def process_processing_instruction_node(self, node):
        self.result.append('<?' + node.target + ' ' + node.data + '?>\n')

    def process_text_node(self, node):
        text = node.data
        text = regex.sub(r"\s+", " ", text)
        if text != " ":
            if self.is_inline_element(node.parentNode):
                text = text.strip()
            else:
                previous = node.previousSibling
                if previous is None or previous.nodeType in (4, 8) or \
                        (previous.nodeType == 1 and not self.is_inline_element(previous)):
                    text = text.lstrip()
                    text = self.calculate_indentation() + text
            self.result.append(text)

    def postprocess(self):
        self.result = ''.join(self.result)
        self.result = self.result.replace("\n\n", "\n")
        self.result = regex.sub(r"\s+\n", "\n", self.result)
        self.result = self.result.strip()

    def write_to_output_file(self):
        with open(self.output_file, 'w') as output_file:
            output_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            output_file.write("".join(self.result))

    def is_inline_element(self, node):
        if node.tagName in self.formatting_options.inline_elements:
            return True
        else:
            return False

    def append_indentation(self):
        self.result.append(self.calculate_indentation())

    def calculate_indentation(self):
        number_of_spaces = self.indentation_level * self.formatting_options.indentation
        return number_of_spaces * ' '


inline_elements = ['inline-element', 'empty-element']
inline_elements = XMLFormattingOptions(
    indentation=6,
    inline_elements=inline_elements)
XMLCustomFormatter('input.xml', 'output.xml', inline_elements)
