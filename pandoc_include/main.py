"""
Panflute filter to allow file includes
"""

import os
import json
import glob
import re

import panflute as pf

from natsort import natsorted
from urllib.parse import urlparse

from .format_heuristics import formatFromPath
from .config import parseConfig, parseOptions, TEMP_FILE


# Global variables
INCLUDE_CMDS     = ['!include', '$include', '!include-header', '$include-header']
INCLUDE_INVALID  = 0
INCLUDE_FILE     = 1
INCLUDE_HEADER   = 2


# Record whether the entry has been entered
entryEnter = False
# Inherited options
options = None


def is_include_line(elem):
    includeType = INCLUDE_INVALID
    config = {}
    name = None
    if not hasattr(elem, "_content"):
        includeType = INCLUDE_INVALID
    elif (len(elem.content) not in [3, 4]) \
        or (not isinstance(elem.content[0], pf.Str)) \
        or (elem.content[0].text not in INCLUDE_CMDS) \
        or (not isinstance(elem.content[-2], pf.Space)) \
        or (len(elem.content) == 4 and not isinstance(elem.content[1], pf.Code)):
        includeType = INCLUDE_INVALID
    else:
        if elem.content[0].text in ['!include', '$include']:
            includeType = INCLUDE_FILE
        else:
            includeType = INCLUDE_HEADER

        # filename
        fn = elem.content[-1]
        if isinstance(fn, pf.Quoted):
            # Convert list to args of Para
            name = pf.stringify(pf.Para(*fn.content), newlines=False)
        else:
            name = fn.text

        # config
        if len(elem.content) == 4:
            config = parseConfig(elem.content[1].text)

    return includeType, name, config


def is_code_include(elem):
    try:
        new_elem = pf.convert_text(elem.text)[0]
    except:
        return INCLUDE_INVALID, None, None

    includeType, name, config = is_include_line(new_elem)
    if includeType == INCLUDE_HEADER:
        pf.debug("[WARN] Invalid !include-header in code blocks")
        includeType = INCLUDE_INVALID

    return includeType, name, config


# Skip whitespaces until newline
def skipWhitespaces(content):
    whiteSpaceReg = re.compile(r"[^\s]|\n")
    m = whiteSpaceReg.search(content)
    if m == None:
        return None
    pos = m.span()[0]
    if content[pos] == "\n":
        pos += 1
    return pos

def removeLeadingWhitespaces(s, num):
    regex = re.compile(r"[^\s]")
    m = regex.search(s)
    if m == None:
        return
    pos = m.span()[0]
    if num < 0:
        return s[pos:]
    else:
        return s[min(pos, num):]

def dedent(content: str, num):
    lines = content.split("\n")
    return list(map(lambda s: removeLeadingWhitespaces(s, num), lines))


def read_file(filename, config: dict):
    with open(filename, encoding="utf-8") as f:
        content = f.read()

    if "startLine" in config or "endLine" in config:
        lines = content.split("\n")
        startLine = config.get("startLine", 1) - 1
        endLine = config.get("endLine", len(lines))
        # count from the end of file
        if startLine < 0:
            startLine += len(lines)
        if endLine < 0:
            endLine += len(lines) + 1
        result = lines[startLine:endLine]
        content = "\n".join(result)

    if "snippetStart" in config or "snippetEnd" in config:
        start = 0
        length = len(content)
        snippets = []
        includeSnippetDelimiters = config.get("includeSnippetDelimiters", False)

        while start < length:
            if "snippetStart" in config:
                pos = content.find(config["snippetStart"], start)
            else:
                pos = -1
            if pos != -1:
                start = pos
            else:
                # If not found for the first time, start from the beginning
                if start != 0:
                    break

            if not includeSnippetDelimiters:
                start += len(config.get("snippetStart", ""))
                # Skip whitespaces until newline
                pos = skipWhitespaces(content[start:])
                if pos == None:
                    break
                start += pos

            if "snippetEnd" in config:
                end = content.find(config["snippetEnd"], start)
            else:
                end = -1
            # no snippetEnd means the end of file
            if end == -1:
                snippets.append(content[start:])
                break

            if includeSnippetDelimiters:
                end += len(config.get("snippetEnd", ""))
                subEnd = end
            else:
                # Skip whitespaces until newline
                pos = skipWhitespaces(content[start:end][::-1])
                if pos == None:
                    subEnd = end
                else:
                    subEnd = end - pos

            snippets.append(content[start:subEnd])
            start = end
        content = "\n".join(snippets)

    if "dedent" in config:
        content = "\n".join(dedent(content, config["dedent"]))

    return content


def action(elem, doc):
    global entryEnter
    global options

    # Try to read inherited options from temp file
    if options is None:
        options = parseOptions(doc)

    # The entry file's directory
    entry = doc.get_metadata('include-entry')
    if not entryEnter and entry:
        os.chdir(entry)
        entryEnter = True

    # --- Include statement ---
    if isinstance(elem, pf.Para):
        includeType, name, config = is_include_line(elem)

        if includeType == INCLUDE_INVALID:
            return

        # Enable shell-style wildcards
        files = glob.glob(name, recursive=True)
        if len(files) == 0:
            raise IOError(f"Included file not found: {name}")

        # order
        include_order = options['include-order']
        if include_order == 'natural':
            files = natsorted(files)
        elif include_order == 'alphabetical':
            files = sorted(files)
        elif include_order == 'default':
            pass
        else:
            raise ValueError('Invalid file order: ' + include_order)

        elements = []
        for fn in files:
            pf.debug(f"[INFO] including file '{fn}'", end="", flush=True)
            if not os.path.isfile(fn):
                raise IOError(f"Included file not found: {fn}")
            pf.debug(f"... ok")

            raw = read_file(fn, config)

            # Save current path
            cur_path = os.getcwd()

            # Change to included file's path so that sub-include's path is correct
            target = os.path.dirname(fn)
            # Empty means relative to current dir
            if not target:
                target = '.'

            currentPath = options["current-path"]
            options["current-path"] = os.path.normpath(os.path.join(currentPath, target))
            os.chdir(target)

            # pass options by temp files
            with open(TEMP_FILE, 'w+') as f:
                json.dump(options, f)

            # Add recursive include support
            new_elems = None
            new_metadata = None
            if includeType == 1:
                # Set file format
                if "format" in config:
                    fmt = config["format"]
                else:
                    fmt = formatFromPath(fn)
                # default use markdown
                if fmt is None:
                    fmt = "markdown"

                # copy since pf will modify this argument
                pandoc_options = list(options["pandoc-options"])

                if "raw" in config:
                    rawFmt = config.get("raw")
                    # raw block
                    new_elems = [pf.RawBlock(raw, format=rawFmt)]
                else:
                    new_doc = pf.convert_text(
                        raw,
                        input_format=fmt,
                        standalone=True,
                        extra_args=pandoc_options
                    )

                    new_metadata = new_doc.get_metadata(builtin=False)
                    new_elems = new_doc.content.list

            else:
                # Read header from yaml
                # Use pf to preserve all info
                new_metadata = pf.convert_text(f"---\n{raw}\n---", standalone=True).get_metadata(builtin=False)

            # Merge metadata
            if new_metadata is not None:
                for key in new_metadata.content:
                    if not key in doc.metadata.content:
                        doc.metadata[key] = new_metadata[key]

            # delete temp file (the file might have been deleted in subsequent executions)
            if os.path.exists(TEMP_FILE):
                os.remove(TEMP_FILE)
            # Restore to current path
            os.chdir(cur_path)
            options["current-path"] = currentPath

            # incremement headings
            increment = config.get('incrementSection', 0)

            if increment:
                for new_elem in new_elems:
                    if isinstance(new_elem, pf.Header):
                        new_elem.level += increment

            if new_elems != None:
                elements += new_elems

        return elements

    # --- Code Blocks ---
    elif isinstance(elem, pf.CodeBlock):
        includeType, name, config = is_code_include(elem)
        if includeType == 0:
            return

        # Enable shell-style wildcards
        files = glob.glob(name, recursive=True)
        if len(files) == 0:
            raise IOError(f"File not found: {name}")

        codes = []
        for fn in files:
            codes.append(read_file(fn, config))

        elem.text = "\n".join(codes)

    # --- Images ---
    elif isinstance(elem, pf.Image):
        rewritePath = options.get("rewrite-path", True)
        if not rewritePath:
            return

        url = elem.url
        # try to parse the url first
        result = urlparse(url)
        # url
        if result.scheme != "":
            return
        # absolute path
        if os.path.isabs(url):
            return

        # rewrite relative path
        elem.url = os.path.join(options["current-path"], url)


def main(doc=None):
    return pf.run_filter(action, doc=doc)


if __name__ == '__main__':
    main()
