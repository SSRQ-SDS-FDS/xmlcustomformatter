from xmlformattingoptions import XMLFormattingOptions
from xmlcustomformatter import XMLCustomFormatter

list_of_tags = ['inline-element']
formatting_options = XMLFormattingOptions(
    indentation=4,
    inline_elements=list_of_tags)

XMLCustomFormatter('input.xml', 'output.xml', formatting_options)
