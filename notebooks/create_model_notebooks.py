"""
Program that creates jupyter notebooks of models passed as
input_file parameter
"""

import nbformat as nbf
import sys


def skip_comments(fp, line):
    # if '"""' in line:
    line = fp.readline()
    while '"""' not in line:
        line = fp.readline()
    return fp.readline()


def import_block(fp, line):
    import_code = ""
    line = fp.readline()
    while line.startswith("from ") or line.startswith("import "):
        import_code += line
        line = fp.readline()

    return line, import_code


def globals_block(fp, line):
    while line == '\n':
        line = fp.readline()

    prev = line
    global_code = ""
    while not line.startswith('def '):
        global_code += line
        line = fp.readline()
        if line == prev:
            break
        prev = line

    return line, global_code


def set_up_block(fp, line):
    setup_code = ""
    env = None
    prev = None

    while "set_up()" not in line:
        if 'Env(' in line:
            code = line.split('    ')
            env = code[1].split(' = ')[0]
        prev = line
        line = fp.readline()

    code = line.split('    ')

    # Check for broken up long lines
    first_part = code[1].split(' = ')[0]
    if ')' in first_part and '(' not in first_part:
        setup_code += prev.split('    ')[1]

    setup_code += code[1]

    return line, setup_code, env


def execute(nb, env):
    nb['cells'].append(nbf.v4.new_markdown_cell
                       ("You can run the model N periods by typing the number"
                        " you want in the following function and then running it."))

    nb['cells'].append(nbf.v4.new_code_cell(env + ".runN()"))

    # Displaying the scatter graph
    nb['cells'].append(nbf.v4.new_markdown_cell
                       ("You can view the position of all of the agents in "
                        "space with the following command:"))

    nb['cells'].append(nbf.v4.new_code_cell(env + ".scatter_graph()"))

    # Displaying the line graph
    nb['cells'].append(nbf.v4.new_markdown_cell
                       ("You can view the line graph through the following command:"))

    nb['cells'].append(nbf.v4.new_code_cell(env + ".line_graph()"))

    return nb


def main():
    REMOVE_EXT = -3
    nb = nbf.v4.new_notebook()
    if len(sys.argv) < 3:
        print("Usage: PROG [input file] [output file]")
        exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    nb['cells'] = []

    filepath = input_file
    with open(filepath) as fp:
        intro = """# How to run the """ + input_file[:-3] + """ model."""

        nb['cells'].append(nbf.v4.new_markdown_cell(intro))

        line = fp.readline()

        if line == "":
            return

        #  Skip comments
        if '"""' in line:
            line = skip_comments(fp, line)

        nb['cells'].append(nbf.v4.new_markdown_cell(
            "First we import all necessary files."))

        # Import block
        line, import_code = import_block(fp, line)
        parts = input_file.split('/')
        import_code += "from models." + parts[-1][:REMOVE_EXT] + " import set_up"

        nb['cells'].append(nbf.v4.new_code_cell(import_code))

        nb['cells'].append(nbf.v4.new_markdown_cell(
            "We then initialize global variables."))

        # Globals block
        line, global_code = globals_block(fp, line)

        nb['cells'].append(nbf.v4.new_code_cell(global_code))

        nb['cells'].append(nbf.v4.new_markdown_cell
                           ("Next we call the `set_up` function "
                            "to set up the environment, groups, and agents of the model."))

        # set_up block
        line, setup_code, env = set_up_block(fp, line)

        nb['cells'].append(nbf.v4.new_code_cell(setup_code))

        # Running the model
        nb = execute(nb, env)

    # Finish making notebook and add notebook 
    with open(output_file, 'w') as f:
        nbf.write(nb, f)

    return 0


if __name__ == "__main__":
    main()
