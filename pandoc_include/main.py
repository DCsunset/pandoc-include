"""
Panflute filter to allow file includes
"""

import os
import panflute as pf
import json
import glob
import sys
import re
import ast
from natsort import natsorted
from urllib.parse import urlparse
from collections import OrderedDict
from .format_heuristics import formatFromPath

CONFIG_KEYS = {
    "startLine": int,
    "endLine": int,
    "snippetStart": str,
    "snippetEnd": str,
    "includeSnippetDelimiters": bool,
    "incrementSection": int,
    "dedent": int,
    "format": str
}

def eprint(text):
    print(text, file=sys.stderr)

def parse_config(text):
    regex = re.compile(
        r'''
            (?P<key>\w+)=      # Key consists of only alphanumerics
            (?P<quote>["'`]?)   # Optional quote character.
            (?P<value>.*?)     # Value is a non greedy match
            (?P=quote)         # Closing quote equals the first.
            ($|,)              # Entry ends with comma or end of string
        ''',
        re.VERBOSE
    )

    config = {}
    for match in regex.finditer(text):
        key = match.group('key')
        if key in CONFIG_KEYS:
            # Include the original quotes
            raw_value = f"{match.group('quote')}{match.group('value')}{match.group('quote')}"
            try:
                value = ast.literal_eval(raw_value)
            except:
                raise ValueError(f"Invalid config: {key}={raw_value}")
            if not isinstance(value, CONFIG_KEYS[key]):
                raise ValueError(f"Invalid value type: {key}={raw_value}")
            config[key] = value

        else:
            eprint("[Warn] Invalid config key: " + key)

    return config


def is_include_line(elem):
    # value: return 0 for false, 1 for include file, 2 for include header
    value = 0
    config = {}
    name = None
    if not hasattr(elem, "_content"):
        value = 0
    elif (len(elem.content) not in [3, 4]) \
        or (not isinstance(elem.content[0], pf.Str)) \
        or (elem.content[0].text not in ['!include', '$include', '!include-header', '$include-header']) \
        or (not isinstance(elem.content[-2], pf.Space)) \
        or (len(elem.content) == 4 and not isinstance(elem.content[1], pf.Code)):
        value = 0
    else:
        if elem.content[0].text in ['!include', '$include']:
            # include file
            value = 1
        else:
            # include header
            value = 2

        # filename
        fn = elem.content[-1]
        if isinstance(fn, pf.Quoted):
            # Convert list to args of Para
            name = pf.stringify(pf.Para(*fn.content), newlines=False)
        else:
            name = fn.text
        
        # config
        if len(elem.content) == 4:
            config = parse_config(elem.content[1].text)
        
    return value, name, config


def is_code_include(elem):
    new_elem = pf.convert_text(elem.text)[0]
    value, name, config = is_include_line(new_elem)
    if value == 2:
        eprint("[Warn] Invalid !include-header in code blocks")
        value = 0
    return value, name, config


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


# Record whether the entry has been entered
entryEnter = False
# Inherited options
options = None

# The temp filename should be fixed
# in order to be found by subprocesses
temp_filename = '.temp.pandoc-include'

def parse_options(doc):
    if os.path.isfile(temp_filename):
        with open(temp_filename, 'r') as f:
            options = json.load(f)
    else:
        # entry file (default values)
        options = {
            "current-path": ".",
            "include-order": "natural",
            "rewrite-path": True,
            "pandoc-options": ["--filter=pandoc-include"]
        }

    # pandoc options
    pandoc_options = doc.get_metadata('pandoc-options')
    if pandoc_options is not None:
        # Replace em-dash to double dashes in smart typography
        for i in range(len(pandoc_options)):
            pandoc_options[i] = pandoc_options[i].replace('\u2013', '--')
        options['pandoc-options'] = pandoc_options

    # order of included files (natural, alphabetical, shell_default)
    include_order = doc.get_metadata("include-order")
    if include_order is not None:
        options["include-order"] = include_order
    
    # rewrite path
    rewrite_path = doc.get_metadata("rewrite-path")
    if rewrite_path is not None:
        options["rewrite-path"] = rewrite_path
    
    return options


def action(elem, doc):
    global entryEnter
    global options

    # Try to read inherited options from temp file
    if options is None:
        options = parse_options(doc)

    # The entry file's directory
    entry = doc.get_metadata('include-entry')
    if not entryEnter and entry:
        os.chdir(entry)
        entryEnter = True

    if isinstance(elem, pf.Para):
        includeType, name, config = is_include_line(elem)

        if includeType == 0:
            return

        # Enable shell-style wildcards
        files = glob.glob(name)
        if len(files) == 0:
            eprint('[Warn] included file not found: ' + name)

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
            if not os.path.isfile(fn):
                continue

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
            with open(temp_filename, 'w+') as f:
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

                new_elems = pf.convert_text(
                    raw,
                    input_format=fmt,
                    extra_args=pandoc_options
                )

                # Get metadata (Recursive header include)
                new_metadata = pf.convert_text(
                    raw,
                    input_format=fmt,
                    standalone=True,
                    extra_args=pandoc_options
                ).get_metadata(builtin=False)

            else:
                # Read header from yaml
                # Use pf to preserve all info
                new_metadata = pf.convert_text(f"---\n{raw}\n---", standalone=True).get_metadata(builtin=False)

            # Merge metadata
            for key in new_metadata.content:
                if not key in doc.metadata.content:
                    doc.metadata[key] = new_metadata[key]

            # delete temp file (the file might have been deleted in subsequent executions)
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
            # Restore to current path
            os.chdir(cur_path)
            options["current-path"] = currentPath 

            # incremement headings
            increment = config.get('incrementSection', 0)

            if increment:
                for elem in new_elems:
                    if isinstance(elem, pf.Header):
                        elem.level += increment

            if new_elems != None:
                elements += new_elems

        return elements
    
    elif isinstance(elem, pf.CodeBlock):
        includeType, name, config = is_code_include(elem)
        if includeType == 0:
            return
        
        # Enable shell-style wildcards
        files = glob.glob(name)
        if len(files) == 0:
            eprint('[Warn] included file not found: ' + name)

        codes = []
        for fn in files:
            codes.append(read_file(fn, config))

        elem.text = "\n".join(codes)
    
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
