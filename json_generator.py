#!/usr/bin/env python3

"""
    Script to generate *_model.json files, given *.py
    *.py files must have docstring at the header of the file first
    otherwise, an empty *_model.json file will be generated
"""

# Docstring format
"""
    name: str,
    run: str,
    props: str,
    doc: str,
    source: str,
    graph: str,
    active: bool
"""

import sys
import json
import os.path

# Docstring must be in same order
jsonFields = ["name", "run", "props", "doc", "source", "graph", "active"]
SCRIPT_NAME = sys.argv[0]
DEST_FOLDER = "registry/models/"  # must have trailing /

def usage():
    """
        Prints usage message
    """
    print("Usage: " + SCRIPT_NAME + " [filepath...]")

def script_output(message, withName=True):
    """
        Wrapper for print to include the script's name
    """
    if(withName is True):
        print(SCRIPT_NAME + ": " + message)
    else:
        print(message)

def parse_docstring(file_path):
    print(file_path)
    with open(file_path, 'r') as input_stream:
        # skip blank lines until first sign of docstring
        # error if found anything else.
        # Step 1: create the empty json file
        filename = os.path.basename(file_path)
        if(len(filename) == 0):
            script_output(filename + " not a file")
            exit(1)
        # Strip away the extension and create file
        name, ext = os.path.splitext(filename)
        fd = open(DEST_FOLDER + name + "_model.json", "w")

        # line = ""
        # doc1,doc2 = -1,-1 # doc1 for docstrings using double quotes
        # while(doc1 == -1 and doc2 == -1):
        #     line = input_stream.readline()

        #     # EOF
        #     if(len(line) == 0):
                
        #         fd = open("")
        #         return

        fd.close()

def generate_json(content):
    return 2

if __name__ == "__main__":
    model_files = sys.argv[1:]
    if(len(model_files) == 0):
        usage()
        exit(0)
    print(model_files)
    for file in model_files:
        generate_json(parse_docstring(file))
    
    
