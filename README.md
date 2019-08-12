# pandoc-include

[![PyPI](https://img.shields.io/pypi/v/pandoc-include)](https://pypi.org/project/pandoc-include/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pandoc-include)](https://pypi.org/project/pandoc-include/)
[![GitHub](https://img.shields.io/github/license/DCsunset/pandoc-include?color=blue)](https://github.com/DCsunset/pandoc-include)

Pandoc filter to allow file includes.

The filter script is based on
[User Guide for Panflute](http://scorreia.com/software/panflute/guide.html#using-the-included-batteries).
This repository is to provide a simple way to install and use it.


## Installation

First, install python and python-pip.

Then, use pip to install:

```
pip install --user pandoc-include
```

After installation,
make sure that the `pandoc-include` executable is put in the directory which is in **the PATH environment**.

## Usage

### Command

To use this filter, add to pandoc command

```
pandoc input.md --filter pandoc-include -o output.pdf
```

### Header option

```
---
include-entry: 'path'
---
```

This option is to make recursive includes work.

The `include-entry` option is a path relative to current working directory or absolute
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


### Syntax

Each include statement has its own line and has the syntax:

```
!include somefolder/somefile
```

Or

```
$include somefolder/somefile
```

Each include statement must be in its own paragraph. That is, in its own line
and separated by blank lines.

The path can be either absolute or relative to the **current** file's directory.
(If the include statement is in an included file,
then the path is relative to the included file itself.)
If no extension was given, ".md" is assumed.

For example,
it can be used to separate chapters into different files,
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

**Note:**
The second syntax may lead to wrong highlighting when using a markdown editor.
If it happens, use the first syntax.

## License

MIT License

