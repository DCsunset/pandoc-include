import re
import ast
import os
import json

import panflute as pf


CONFIG_KEYS = {
    "startLine": int,
    "endLine": int,
    "snippetStart": str,
    "snippetEnd": str,
    "xslt": str,
    "includeSnippetDelimiters": bool,
    "incrementSection": int,
    "dedent": int,
    "format": str,
    "raw": str
}

# The temp filename should be fixed
# in order to be found by subprocesses
TEMP_FILE = '.temp.pandoc-include'

def parseBoolValue(val):
    # use 1 or 0 (otherwise default to true if not empty)
    return val and val != "0"

# Keys for env config
class Env:
  NotFoundError = False

  def parse():
      Env.NotFoundError = parseBoolValue(os.environ.get(f"PANDOC_INCLUDE_NOT_FOUND_ERROR", "0"))


def parseConfig(text):
    regex = re.compile(
        r'''
            (?P<key>\w+)=      # Key consists of only alphanumerics
            (?P<quote>["'`]?)  # Optional quote character.
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
            pf.debug("[Warn] Invalid config key: " + key)

    return config


defaultOptions = {
    "current-path": ".",
    "include-resources": ".",
    "process-path": None,
    "include-order": "natural",
    "rewrite-path": True,
    "pandoc-options": ["--filter=pandoc-include"]
}

def parseOptions(doc):
    if os.path.isfile(TEMP_FILE):
        with open(TEMP_FILE, 'r') as f:
            # merge with default options to prevent missing keys
            options = defaultOptions | json.load(f)
    else:
        # entry file (default values)
        options = defaultOptions.copy()

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

    # resource path
    resource_path = doc.get_metadata("include-resources")
    if resource_path is not None:
        options["include-resources"] = resource_path

    # process path
    process_path = os.getcwd()
    if options["process-path"] is None:
        options["process-path"] = process_path

    return options
