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
        # This is necessary because the XML DOM does not contain
        # an XML-declaration. If there was one present in the
        # input document, the parser would ignore it.
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
        self.result.append(self.calculate_indentation())
        self.result.append("\n" + self.calculate_indentation() + "<![CDATA[" + node.nodeValue + ']]>\n')

    def process_comment_node(self, node):
        comment = node.data
        comment = comment.replace('\n', ' ')
        comment = regex.sub(r'\s+', ' ', comment)
        self.result.append('\n' + self.calculate_indentation() + '<!--' + comment + '-->\n')

    def process_document_node(self, node):
        for childNode in node.childNodes:
            self.process(childNode)

    def process_document_type_node(self, node):
        self.result.append("<!DOCTYPE " + node.name + " ")
        self.process_document_type_internal_subset(node)
        self.result.append(">")

    def process_document_type_internal_subset(self, node):
        if node.internalSubset:
            self.increase_indentation_level()
            subset = node.internalSubset
            subset = " ".join(subset.split())
            subset = subset.replace("<!", "\n" + self.calculate_indentation() + "<!")
            subset = subset.replace("<?", "\n" + self.calculate_indentation() + "<?")
            self.result.append('[' + subset + '\n]')
            self.decrease_indentation_level()

    def decrease_indentation_level(self):
        self.indentation_level -= 1

    def increase_indentation_level(self):
        self.indentation_level += 1

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
            self.decrease_indentation_level()
            self.result.append('\n')
            self.result.append(self.calculate_indentation())
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
            self.result.append(self.calculate_indentation())
            self.result.append('<' + node.tagName)
            self.process_element_attributes(node)
            if node.childNodes.length == 0:
                self.result.append('/>\n')
            else:
                self.result.append('>\n')
                self.increase_indentation_level()

    def process_processing_instruction_node(self, node):
        text = node.data
        text = regex.sub(r"\s+", " ", text)
        self.result.append('<?' + node.target + ' ' + text + '?>\n')

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
        self.result = "".join(self.result)
        self.result = self.result.replace("\n\n", "\n")
        self.result = regex.sub(r"\s+\n", "\n", self.result)
        self.result = self.result.strip()

    def write_to_output_file(self):
        with open(self.output_file, 'w') as output_file:
            output_file.write(self.result)

    def is_inline_element(self, node):
        if node.tagName in self.formatting_options.inline_elements:
            return True
        else:
            return False

    def calculate_indentation(self):
        return self.indentation_level * self.formatting_options.indentation * ' '
