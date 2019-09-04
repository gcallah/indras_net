"""
Program that creates jupyter notebooks of models passed as
filename parameter
"""

import nbformat as nbf
import sys
import os


nb = nbf.v4.new_notebook()
filename = sys.argv[-1]
nb['cells'] = []

filepath = os.path.abspath('../models') + '/' + filename
with open(filepath) as fp:
    intro = """# This is the working of the """ + filename[:-3] + """ model."""

    nb['cells'].append(nbf.v4.new_markdown_cell(intro))

    line = fp.readline()

    #  Skip comments
    if '"""' in line:
        line = fp.readline()
        while '"""' not in line:
            line = fp.readline()
        line = fp.readline()

    nb['cells'].append(nbf.v4.new_markdown_cell(
        "First we import all necessary files"))

    # Import block
    importCode = ""
    line = fp.readline()
    while line.startswith("from ") or line.startswith("import "):
        importCode += line
        line = fp.readline()

    importCode += "from models." + filename[:-3] + " import set_up"

    nb['cells'].append(nbf.v4.new_code_cell(importCode))

    nb['cells'].append(nbf.v4.new_markdown_cell("We then initialize global variables"))

    # Globals block
    while line == '\n':
        line = fp.readline()

    prev = line
    globalCode = ""
    while not line.startswith('def '):
        globalCode += line
        line = fp.readline()
        if line == prev:
            break
        prev = line

    nb['cells'].append(nbf.v4.new_code_cell(globalCode))

    nb['cells'].append(nbf.v4.new_markdown_cell("Now we call the set_up function "
                       "to set up the environment of the model"))

    # set_up block
    setupCode = ""
    while "set_up()" not in line:
        line = fp.readline()

    code = line.split('    ')
    setupCode += code[1]
    nb['cells'].append(nbf.v4.new_code_cell(setupCode))

    # Finish making notebook and add notebook to
    # directory with the same name as the model
    fname = filename[:-3] + '.ipynb'
    with open(fname, 'w') as f:
        nbf.write(nb, f)
