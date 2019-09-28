---
include-entry: '.'
test:
	adsf: a
	base:
		- b
		- c
---

# Test

## Included file list

* included-1.md
	* included-r1.md
		* included-r2.md
* included 2.tex

## Include header

!include-header included/included-header.md

## Included file

!include included/included-1.md

### A simple latex table

$include included/included 2.tex

