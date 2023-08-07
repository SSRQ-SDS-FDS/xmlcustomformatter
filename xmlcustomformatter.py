import xml.dom.pulldom


class XMLFormattingOptions:
    def __init__(self, max_line_length=80, indentation='4', inline_elements=None):
        self.max_line_length = max_line_length
        self.indentation = indentation
        self.inline_elements = inline_elements


class XMLCustomFormatter:
    def __init__(self, input_file, output_file, formatting_options=None):
        self.input_file = input_file
        self.output_file = output_file
        self.formatting_options = formatting_options or XMLFormattingOptions()
        self.stream = None
        self.result = None
        self.format_xml()

    def format_xml(self):
        self.open_input_file_as_stream()
        self.process_stream()
        self.write_to_output_file()

    def open_input_file_as_stream(self):
        self.stream = xml.dom.pulldom.parse(self.input_file)

    def process_stream(self):
        # Here comes the implementation
        pass

    def write_to_output_file(self):
        with open(self.output_file, 'wb') as output_file:
            output_file.write(self.result)
