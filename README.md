# pandoc-include

[![PyPI](https://img.shields.io/pypi/v/pandoc-include)](https://pypi.org/project/pandoc-include/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pandoc-include)](https://pypi.org/project/pandoc-include/)
[![GitHub](https://img.shields.io/github/license/DCsunset/pandoc-include?color=blue)](https://github.com/DCsunset/pandoc-include)

Pandoc filter to allow file and header includes.

The filter script is based on
[User Guide for Panflute](http://scorreia.com/software/panflute/guide.html#using-the-included-batteries).
This repository is to provide a simple way to install and use it.

## Features

* Partial include (since v1.0.0): Allow including only parts of the file using options
* Code include (since v0.8.5): Allow using `!include` in code blocks
* Unix style pathname (since v0.8.2)
* Recursive include (since v0.4.0): It depends on `include-entry` header to work
* Yaml header Merging (since v0.5.0):
When an included file has its header, it will be merged into the current header.
If there's a conflict, the original header of the current file remains.
* Header include (since v0.6.0): Use `!include-header file.yaml` to include Yaml header from file.


## Installation

pandoc-include requires [python](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/installing/).

Then, use pip to install:

```
pip install --user pandoc-include
```

After installation,
make sure that the `pandoc-include` executable is put in the directory which is in **the PATH environment**.

To install the current (development) version hosted on the repository, use

```
pip install --upgrade --force --no-cache git+https://github.com/DCsunset/pandoc-include
```

You can use

```
pip show pandoc-include
```

to check the version currently installed.

## Usage

### Command

To use this filter, add to pandoc command

```
pandoc input.md --filter pandoc-include -o output.pdf
```

### Syntax

Each include statement has its own line and has the syntax:

```
!include somefolder/somefile

!include-header file.yaml
```

Or

```
$include somefolder/somefile

$include-header file.yaml
```

Each include statement must be in its own paragraph. That is, in its own line
and separated by blank lines.


For code include, use `!include` statement in a code block:

````markdown
```cpp
!include filename.cpp
```
````

The path can be either absolute or relative to the **current** file's directory.
Besides, [unix-style](https://en.wikipedia.org/wiki/Glob_(programming)) pathname can used.
(If the include statement is used in an included file,
then the path is absolute or relative to the included file itself.)

If there are special characters in the filename, use quotes:

```
!include "filename with space"
!include 'filename"with"quotes'
```

The second syntax may lead to wrong highlighting when using a markdown editor.
If it happens, use the first syntax.
Also make sure that there are no circular includes.


The `!include` command also supports options:

```
!include`<key1>=<value1>, <key2>=<value2>` some_file
```

For example, to specify line ranges in options:

```
!include`startLine=1, endLine=10` some_file
```

Or to include snippets with enclosed delimiters:

```
!include`snippetStart="<!-- Start -->", snippetEnd="<!-- End -->"` some_file
```

where `<!-- Start -->` and `<!-- End -->` are two strings occuring in `some_file`.

If multiple occurences of `<!-- Start -->` or `<!-- End -->` are in `some_file`, then pandoc-include will include all the blocks between the delimiters.
If `snippetEnd` or `snippetStart` is not found or specified, it will include till the end or from the start.

Supported options:

| Key | Value | Description |
| --- | ----- | ----------- |
| startLine | `int` | Start line of include (default: 1) |
| endLine | `int` | End line of include (default: number of the last line) |
| snippetStart | `str` | Start delimiter of a snippet |
| snippetEnd | `str` | End delimiter of a snippet |
| includeSnippetDelimiters | `bool` | Whether to include the delimiters (default: `False`) |
| incrementSection | `int` | Increment (or decrement) section levels of include |
| dedent | `int` | Remove n leading whitespaces of each line where possible (`-1` means remove all) |
| format | `str` | The input format of the included file (see `pandoc --list-input-formats`). It will be automatically deduced from the path if not set |

**Note**: the values above are parsed as Python literals. So `str` should be quoted like `'xxx'` or `"xxx"`; `bool` should be `True` or `False`.


### Header options

```
---
include-entry: '<path>'
include-order: 'natural'
pandoc-options:
  - --filter=pandoc-include
  - <other options>
---
```

The `include-entry` option is to make recursive includes work.
Its value is a path relative to current working directory or absolute
where the entry file (the initial file) locates.
It should be placed in the entry file only, not in the included files.
It is optional and the default `include-entry` value is `.`.

For example, to compile a file in current directory, no header is needed:

```
pandoc test.md --filter pandoc-include -o test.pdf
```

However, to compile a file not in current directory, like:

```
pandoc dir/test.md --filter pandoc-include -o test.pdf
```

The header should now be set to: `include-entry: 'dir'`.


The `include-order` options is to define the order of included files if the unix-style pathname matches multiple files.
The default value is `natural`, which means using the [natural order](https://en.wikipedia.org/wiki/Natural_sort_order).
Other possible values are `alphabetical` and `default`.
The `default` means to keep the order returned by the Python `glob` module.

The `pandoc-options` option is **a list** to specify the pandoc options when recursively processing included files.
By default, the included file will **inherit** the `pandoc-options` from its parent file, **unless** specified in its own file.

To make the recursive includes work, `--filter=pandoc-include` is **necessary**.
The default value of `pandoc-options` is:

```
pandoc-options:
  - --filter=pandoc-include
```


## Examples

### File include

File include can be used to separate chapters into different files,
or include some latex files:

```markdown

---
title: Article
author: Author
toc: true
---

!include chapters/chap01.md

!include chapters/chap02.md

!include chapters/chap03.md

!include data/table.tex

```

Recursive include is supported from v0.4.0.

### Header include

For header include, it is useful to define a header template
and include it in many files.

For example, in the `header.yaml`, we can define basic info:

```yaml
name: xxx
school: yyy
email: zzz
```

In the `main.md`, we can extend the header:

```markdown

---
title: Title
---

!include-header header.yaml

# Section

Body

```

The `main.md` then is equivalent to the follow markdown:

```markdown

---
title: Title
name: xxx
school: yyy
email: zzz
---

# Section

Body

```

## Trouble Shooting

The pandoc command-line options are processed in order.
If you want some options to be applied in included files,
make sure the `--filter pandoc-include` option is specified before those options.

For example, use bibliography in the included files:

```
pandoc main.md --filter pandoc-include --citeproc --bibliography=ref.bib -o main.pdf
```

## License

MIT License

