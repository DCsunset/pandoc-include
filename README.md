# pandoc-include

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

The `include-entry` option is a path relative to current working directory or absolute
where the entry file (the initial file) locates.
It should be placed in the entry file only, not in the included files.
The default `include-entry` value is `.`.

For example, to compile a file in current directory, no header is needed:

```
pandoc test.md --filter pandoc-include -o test.pdf
```

However to compile a file not in current directory, like:

```
pandoc dir/test.md --filter pandoc-include -o test.pdf
```

The header should now be set to: `include-entry: dir`.


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

Recursive include is supported from v0.3.1.

**Note:**
The second syntax may lead to wrong highlighting when using a markdown editor.
If it happens, use the first syntax.

## License

MIT License

