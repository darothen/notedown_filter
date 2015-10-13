#!/usr/bin/env python
"""
Strip output from a markdown/notedown format Jupyter Notebook.

Usage:
    stripoutput.py [<NOTEBOOK_FILE>]
    stripoutput.py install
    stripoutput.py -h | --help

Options:
    -h, --help      Show this help message.

Arguments:
    <NOTEBOOK_FILE> The notebook to read/strip.

To install into the current git repository, execute the "install"
subcommand.

"""
from __future__ import print_function

import docopt
import sys

from io import open
from nbformat import read, write, NO_CONVERT
from notedown import (strip, MarkdownReader, MarkdownWriter,
                      markdown_template)


def install():
    """ Install the git filter and set it up in the current
    directory. """
    from os import path
    from subprocess import check_call, check_output, CalledProcessError

    # First see if git is even available in the current directory
    try:
        git_dir = check_output(['git', 'rev-parse', '--git-dir']).strip()
    except CalledProcessError:
        print("Can't install; not a git repository.",
              file=sys.stderr)
        sys.exit(1)

    path_to_script = path.abspath(__file__)

    check_call(['git', 'config', 'filter.stripoutput.clean',
                "'%s'" % path_to_script])
    check_call(['git', 'config', 'filter.stripoutput.smudge', 'cat'])
    check_call(['git', 'config', 'filter.stripoutput.required', 'true'])

    git_attributes_file = path.join(git_dir, 'info', 'attributes')

    # Check if there's already a filter specified
    if path.exists(git_attributes_file):
        with open(git_attributes_file, 'r') as f:
            if "*.md filter" in f.read():
                return
    with open(git_attributes_file, 'w') as f:
        f.write(u"\n*.md filter=stripoutput")

if __name__ == "__main__":
    args = docopt.docopt(__doc__)

    reader = MarkdownReader(precode='\n',
                            magic=False,
                            match='fenced',
                            caption_comments=False)
    writer = MarkdownWriter(markdown_template,
                            strip_outputs=True)

    print(args, file=sys.stderr)

    if args['<NOTEBOOK_FILE>'] == 'install':
        install()
    elif args['<NOTEBOOK_FILE>'] is not None:
        # Read in the notebook from a named file
        input_filename = args['<NOTEBOOK_FILE>']
        with open(input_filename, 'r', encoding='utf-8') as f:
            notebook = reader.read(f)

        # Strip output cells
        strip(notebook)

        # Render processed notebook and write
        output = writer.writes(notebook)
        with open(input_filename, "w", encoding='utf-8') as f:
            f.write(output)
    else:
        # Read in a notebook from stdin
        notebook = reader.read(sys.stdin)
        strip(notebook)
        print(notebook, file=sys.stderr)
        output = writer.writes(notebook)
        sys.stdout.write(output)
