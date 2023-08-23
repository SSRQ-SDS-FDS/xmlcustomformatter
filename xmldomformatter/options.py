class XMLFormattingOptions:
    def __init__(self,
            max_line_length: int = 80,
            indentation: int = 4,
            inline_elements = list | None):
        self.max_line_length = max_line_length
        self.indentation = indentation
        self.inline_elements = inline_elements
