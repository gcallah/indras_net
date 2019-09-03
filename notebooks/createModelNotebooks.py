"""
Program that creates jupyter notebooks of models passed as
filename parameter
"""

import nbformat as nbf
import sys
import os


nb = nbf.v4.new_notebook()
filename = sys.argv[-1]

filepath = os.path.abspath('../models') + '/' + filename
with open(filepath) as fp:
    intro = """\
    # My first automatic Jupyter Notebook
    This is an auto-generated notebook."""

    line = fp.readline()
    importCode = ""
    if '"""' in line:
        line = fp.readline()
        while '"""' not in line:
            line = fp.readline()
        line = fp.readline()

    # Import block
    line = fp.readline()
    while line.startswith("from ") or line.startswith("import "):
        importCode += line
        line = fp.readline()

    nb['cells'] = [nbf.v4.new_markdown_cell(intro),
                   nbf.v4.new_code_cell(importCode)]

    # set_up block
    while not line.startswith("def set_up("):
        line = fp.readline()

    setupCode = ""
    setupCode += line
    line = fp.readline()
    while "return " not in line:
        setupCode += line
        line = fp.readline()
    setupCode += line

    nb['cells'].append(nbf.v4.new_code_cell(setupCode))

    # Finish making notebook and add notebook to
    # directory with the same name as the model
    fname = filename[:-3] + '.ipynb'
    with open(fname, 'w') as f:
        nbf.write(nb, f)
