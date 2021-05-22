"""
Panflute filter to allow file includes
"""

import os
import panflute as pf
import json
import glob
import sys
import re
from natsort import natsorted
from collections import OrderedDict

def eprint(text):
    print(text, file=sys.stderr)

def is_include_line(elem):
    # value: return 0 for false, 1 for include file, 2 for include header
    value = 0
    config = None
    name = None
    firstElem = elem.content[0]
    if (len(elem.content) not in [3, 4]) \
        or (not isinstance(firstElem, pf.Str)) \
        or (firstElem.text not in ['!include', '$include', '!include-header', '$include-header']) \
        or (not isinstance(elem.content[-2], pf.Space)) \
        or (len(elem.content) == 4 and not isinstance(elem.content[1], pf.Code)):
        value = 0
    else:
        if firstElem.text in ['!include', '$include']:
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
        # TODO
        
    return value, name, config


def is_code_include(elem):
    new_elem = pf.convert_text(elem.text)[0]
    value, name, config = is_include_line(new_elem)
    if value == 2:
        eprint("[Warn] Invalid !include-header in code blocks")
        value = 0
    return value, name, config


# Record whether the entry has been entered
entryEnter = False
# Inherited options
options = None

# The temp filename should be fixed
# in order to be found by subprocesses
temp_filename = '.temp.pandoc-include'

def action(elem, doc):
    global entryEnter
    global options

    if isinstance(elem, pf.Para):
        includeType, name, _ = is_include_line(elem)

        if includeType == 0:
            return

        passOptions = False
        # Try to read inherited options from temp file
        if options is None:
            if os.path.isfile(temp_filename):
                # pass options when the parent has passed it
                passOptions = True
                with open(temp_filename, 'r') as f:
                    options = json.load(f)
            else:
                options = {}

        # pandoc options
        pandoc_options = doc.get_metadata('pandoc-options')
        if not pandoc_options:
            if 'pandoc-options' in options:
                pandoc_options = options['pandoc-options']
            else:
                # default options
                pandoc_options = ['--filter=pandoc-include']
        else:
            # pass options when they are modified
            passOptions = True
            # Replace em-dash to double dashes in smart typography
            for i in range(len(pandoc_options)):
                pandoc_options[i] = pandoc_options[i].replace('\u2013', '--')

            options['pandoc-options'] = pandoc_options

        # The entry file's directory
        entry = doc.get_metadata('include-entry')
        if not entryEnter and entry:
            os.chdir(entry)
            entryEnter = True
        
        # order of included files (natural, alphabetical, shell_default)
        include_order = doc.get_metadata('include-order')
        if not include_order:
            if 'include-order' in options:
                include_order = options['pandoc-options']
            else:
                include_order = 'natural'
        else:
            options['include-order'] = include_order

        # Enable shell-style wildcards
        files = glob.glob(name)
        if len(files) == 0:
            eprint('[Warn] included file not found: ' + name)

        # order
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

            with open(fn, encoding="utf-8") as f:
                raw = f.read()

            # Save current path
            cur_path = os.getcwd()

            # Change to included file's path so that sub-include's path is correct
            target = os.path.dirname(fn)
            # Empty means relative to current dir
            if not target:
                target = '.'

            os.chdir(target)

            if passOptions:
                # pass options by temp files
                with open(temp_filename, 'w+') as f:
                    json.dump(options, f)

            # Add recursive include support
            new_elems = None
            new_metadata = None
            if includeType == 1:
                new_elems = pf.convert_text(
                    raw, extra_args=pandoc_options)

                # Get metadata (Recursive header include)
                new_metadata = pf.convert_text(raw, standalone=True, extra_args=pandoc_options).get_metadata(builtin=False)

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

            if new_elems != None:
                elements += new_elems

        return elements
    
    elif isinstance(elem, pf.CodeBlock):
        if not is_code_include(elem):
            return
        
        # Single file
        filename = elem.text.split(maxsplit=1)[1]
        if not os.path.isfile(filename):
            eprint('[Warn] Unable to open included file: ' + filename)
            return

        with open(filename, encoding="utf-8") as f:
            code = f.read()

        elem.text = code


def main(doc=None):
    return pf.run_filter(action, doc=doc)


if __name__ == '__main__':
    main()
