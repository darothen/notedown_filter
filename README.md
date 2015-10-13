{'--help': False,
 '<NOTEBOOK_FILE>': None,
 'install': False}
# notedown_filter

This is an uber straightforward script which is intended to be used as a git
filter for stripping output from markdown-format Jupyter notebooks before
diffing or committing.

## Requirements

- [notedown](https://github.com/aaren/notedown)

## Usage

Simply run the script on a notedown/Jupyter Notebook file:

```python
stripoutput.py FILE.md
```

The script can be installed into the local git repository as a filter by
executed `stripoutput.py install` from the command line once in the directory
where this functionality is desired.

## Potential Improvements

- Run, render, and save figures as alternative pre-commit or other git hook
- overwrite option
- Better docopt handling of `install` arguments
