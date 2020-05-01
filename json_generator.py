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
    """
        parses the docstring at the top of every model file
        returns a [] with tuples (KEY, VAL) in the order of the jsonFields
    """
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
        fd.close()

        # Step 2: find the beginning of the docstring
        line = ""
        doc1,doc2 = -1,-1 # doc1 for docstrings using double quotes
        while(doc1 == -1 and doc2 == -1):
            line = input_stream.readline()

            # EOF
            # Nothing to add no docstring
            if(len(line) == 0):
                return []

            line = line.strip()
            if(len(line) == 0):
                continue
            
            doc1 = line.find("\"\"\"")
            doc2 = line.find("\'\'\'")
            if(doc1 != -1 or doc2 != -1):
                # We reached the start of the docstring
                break
            else:
                # Indicates we found some other string first
                script_output("model docstring must be at the header of file")
                script_output("error found in " + file_path, False)
                exit(1)

        # # Step 3 start reading until last key
        # for i in range(len(jsonFields)):
        #     line = input_stream.readline()
        #     keyIndex = line.find(jsonFields[i] + ": ")
        #     if(keyIndex == -1):



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
    
    
