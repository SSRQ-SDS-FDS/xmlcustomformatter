# Purpose

The XMLCustomFormatter is intended to provide means to format XML-files
in a customizable way.

# Underlying technology

The xmlcustomformatter is written in Python and uses the built-in package
[xml.dom.minidom](https://docs.python.org/3/library/xml.dom.minidom.html)
for Pythons Document Object Model (DOM) API.

uv is used as a package manager and build/installation tool.

# Installation and execution

Clone the repository and execute: `uv build` to build and install the XMLCustomFormatter
or download the released wheels from GitHub and install them with: `pip install` 

After this step you can evoke the XMLCustomFormatter
with the command `xmlfmt`.

`xmlfmt --help` shows all possible flags  
`xmlfmt --version` will show the current version  
`xmlfmt input.xml output.xml` will format input.xml
and write the formatted XML into output.xml

# Main options

For all available options see `xmlfmt --help`.

The main options are as follows:

## Indentation

`xmlfmt input.xml output.xml --indentation <n>`

The XML-tree will be indented by whitespace characters only.  
You can choose how many whitespaces are used for every nesting level.  
Default value is four whitespace characters.

Examples:

`xmlfmt input.xml output.xml`  
```
<root>foo</root>
``` 
will be formatted to:  
```
<root>
    foo
</root>
```

`xmlfmt input.xml output.xml --indentation 1`  
```
<root>foo</root>
``` 
will be formatted to:  
```
<root>
 foo
</root>
``` 

`xmlfmt input.xml output.xml --indentation 8`  
```
<root>foo</root>
``` 
will be formatted to:  
```
<root>
        foo
</root>
```

## Max_line_length

Long lines will be split at the latest possible whitespace character.
If there is no suitable whitespace character, the line remains as is.
Default max_line_length is set to 120.

Examples:

`xmlfmt input.xml output.xml`  
```
<?xml-model href="https://schema.ssrq-sds-fds.ch/latest/TEI_Schema.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>
```
will be formatted to:
```
<?xml-model href="https://schema.ssrq-sds-fds.ch/latest/TEI_Schema.rng" type="application/xml" 
schematypens="http://relaxng.org/ns/structure/1.0"?>
```


`xmlfmt input.xml output.xml --max-line-length 80`  
```
<?xml-model href="https://schema.ssrq-sds-fds.ch/latest/TEI_Schema.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>
```
will be formatted to:
```
<?xml-model href="https://schema.ssrq-sds-fds.ch/latest/TEI_Schema.rng"
type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>
```

## Element behavior

There are three types of element behaviors: container elements, 
semicontainer elements and inline elements.

Every element is by default a container element and behaves as follows:

- the start tag will be placed on a new line
- the indentation is increased by `--indentation`
- content, if any exists, will start on a new line
  and will be indented
- the end tag will be placed on a new line
- the indentation is decreased by `--indentation`

A semicontainer element behaves as follows:
- the start tag will be placed on a new line
- indentation is increased by `--indentation`
- content will start directly behind the start tag
- indentation is decreased by `--indentation`
- if possible, the end tag is placed directly behind the content

An inline element behaves as follows:
- the start tag will be placed directly behind the last XML portion
- indentation is increased by `--indentation`
- content will start directly behind the start tag
- indentation is decreased by `--indentation`
- if possible, the end tag is placed directly behind the content

Examples:

Container-Elements
```xml
<container>
    <container>
        Foo 
    </container>
</container>
```
```xml
<container>
    <container>
        Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et
        dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet
        clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet,
        consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat,
        sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea
        takimata sanctus est Lorem ipsum dolor sit amet.
    </container>
</container>
```

Semicontainer-Elements
```xml
<semicontainer>
    <semicontainer>Foo</semicontainer>
</semicontainer>
```
```xml
<semicontainer>
    <semicontainer>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut
    labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum.
    Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet,
    consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed
    diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata
    sanctus est Lorem ipsum dolor sit amet.</semicontainer>
</semicontainer>
```

Inline-Elements
```xml
<inline><inline>Foo</inline></inline>
```
```xml
<inline><inline>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut
labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet
clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur
sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.
At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem
ipsum dolor sit amet.</inline></inline>
```