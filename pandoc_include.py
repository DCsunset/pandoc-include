"""
Panflute filter to allow file includes

Each include statement has its own line and has the syntax:

    !include ../somefolder/somefile

    !include-header ./header.yaml

Or

    $include ../somefolder/somefile

    $include-header ./header.yaml

Each include statement must be in its own paragraph. That is, in its own line
and separated by blank lines.

If no extension was given, ".md" is assumed.
"""

import os
import panflute as pf
import yaml
import json
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
    if not os.path.splitext(fn)[1]:
        if includeType == 1:
            fn += '.md'
        else:
            fn += '.yaml'
    return fn


# Record whether the entry has been entered
entryEnter = False
# Inherited options
options = None

temp_filename = '.temp.pandoc-include'

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

        fn = get_filename(elem, includeType)

        if not os.path.isfile(fn):
            raise ValueError('Included file not found: ' +
                             '%r %r %r' % (fn, entry, os.getcwd()))

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

        # Alternative A:
        return new_elems
        # Alternative B:
        # div = pf.Div(*new_elems, attributes={'source': fn})
        # return div


def main(doc=None):
    return pf.run_filter(action, doc=doc)


if __name__ == '__main__':
    main()
