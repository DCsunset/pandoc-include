---
include-entry: '.'
listings: true
title: Test
date: \today{}
test:
  adsf: a
  base:
    - b
    - c
pandoc-options:
  - --filter=pandoc-include
---

# Test

## Included file list

* included-1.md
	* included-r1.md
		* included-r2.md
* included 2.tex

## Include header

!include-header included/header.yaml

## Included file

!include included/included-1.md

### A simple latex table

$include "included/included 2.tex"

## Include files

!include included/*.md


| Key | Value |
| --- | ----- |
| 1   | 2     |
| 2   | 4     |


## Include code

```cpp
!include 1.cpp
```

## Include with options

### Delimiters


!include`snippetStart="|Start|", snippetEnd="|End|"` included/included-1.md

```cpp
!include`snippetStart="// Start", snippetEnd="// End"` 1.cpp
```

```cpp
!include`snippetStart="// Start"` 1.cpp
```

### Dedent

```cpp
!include`snippetStart="// Start", snippetEnd="// End", dedent=-1` 1.cpp
```

### Line Number

!include`startLine=1, endLine=5` included/included-1.md
