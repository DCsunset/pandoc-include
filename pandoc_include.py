"""
Panflute filter to allow file includes
"""

import tempfile
import os
import panflute as pf
import yaml
import json
import glob
import sys
from natsort import natsorted
from collections import OrderedDict


def is_include_line(elem):
    # Return 0 for false, 1 for include file, 2 for include header
    if len(elem.content) < 3:
        return 0
    elif not all(isinstance(x, (pf.Str, pf.Space)) for x in elem.content):
        return 0
    elif elem.content[0].text != '!include' and elem.content[0].text != '$include' and \
            elem.content[0].text != '!include-header' and elem.content[0].text != '$include-header':
        return 0
    elif type(elem.content[1]) != pf.Space:
        return 0
    elif elem.content[0].text == '!include' or elem.content[0].text == '$include':
        # include file
        return 1
    else:
        # include header
        return 2


def get_filename(elem, includeType):
    fn = pf.stringify(elem, newlines=False).split(maxsplit=1)[1]
    return fn


# Record whether the entry has been entered
entryEnter = False
# Inherited options
options = None

temp_filename = next(tempfile._get_candidate_names())

def action(elem, doc):
    global entryEnter
    global options

    if isinstance(elem, pf.Para):
        includeType = is_include_line(elem)
        if includeType == 0:
            return

        # Try to read inherited options from temp file
        if options is None:
            try:
                with open(temp_filename, 'r') as f:
                    options = json.load(f)
            except:
                options = {}
                pass

        # pandoc options
        pandoc_options = doc.get_metadata('pandoc-options')
        if not pandoc_options:
            if 'pandoc-options' in options:
                pandoc_options = options['pandoc-options']
            else:
                # default options
                pandoc_options = ['--filter=pandoc-include']
        else:
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

        name = get_filename(elem, includeType)
        # Enable shell-style wildcards
        files = glob.glob(name)
        if len(files) == 0:
            print('[Warn] included file not found: ' + name, file=sys.stderr)

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
            # save options
            with open(temp_filename, 'w+') as f:
                json.dump(options, f)

            # Add recursive include support
            new_elems = None
            new_metadata = None
            if includeType == 1:
                new_elems = pf.convert_text(
                    raw, extra_args=pandoc_options)

                # Get metadata (Recursive header include)
                new_metadata = pf.convert_text(raw, standalone=True, extra_args=pandoc_options).get_metadata()

            else:
                # Read header from yaml
                new_metadata = yaml.safe_load(raw)
                new_metadata = OrderedDict(new_metadata)

            # Merge metadata
            for key in new_metadata:
                if not key in doc.get_metadata():
                    doc.metadata[key] = new_metadata[key]

            # delete temp file (the file might have been deleted in subsequent executions)
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
            # Restore to current path
            os.chdir(cur_path)

            if new_elems != None:
                elements += new_elems

        return elements


def main(doc=None):
    return pf.run_filter(action, doc=doc)


if __name__ == '__main__':
    main()
