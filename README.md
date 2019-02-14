# pandoc-include

Pandoc filter to allow file includes.

The filter script is originally from
[User Guide for Panflute](http://scorreia.com/software/panflute/guide.html#using-the-included-batteries).
This repository is to provide a simple way to install and use it.


## Installation

Use pip to install:

```
pip install --user pandoc-include
```


## Usage

Each include statement has its own line and has the syntax:

```
!include ../somefolder/somefile
```

Or

```
$include ../somefolder/somefile
```

Each include statement must be in its own paragraph. That is, in its own line
and separated by blank lines.

If no extension was given, ".md" is assumed.

**Note:**
The second syntax may lead to wrong highlighting when using a markdown editor.
If it happens, use the first syntax.

## License

MIT License

