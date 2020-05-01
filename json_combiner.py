#!/usr/bin/env python3

"""
    Combines all *_model.json files in registry/models
    to one models.json file
"""

import json
import sys
import os

DEST_FILE = "registry/models/models.json"
SRC_FOLDER = "registry/models/"  # must have trailing /
SCRIPT_NAME = sys.argv[0]
DB_NAME = "models_database"
RESULT_JSON = { DB_NAME : [] }

def usage():  # () -> None
    """
        Prints usage message
    """
    print("Usage: " + SCRIPT_NAME)


def validate_config():  # () -> None
    """
        Checks the configuration of this script
    """
    if(len(DEST_FILE) == 0):
        script_output("Please the path for destination file, DEST_FILE")
        exit(1)
    if(DEST_FILE[-1] == "/"):
        script_output("DEST_FILE should not have trailing /")
        exit(1)
    if(DEST_FILE[len(DEST_FILE)-5:] != ".json"):
        script_output("DEST_FILE should be a .json file")
        exit(1)
    if(len(SRC_FOLDER) == 0):
        script_output("Please indicate a source folder, SRC_FOLDER")
        exit(1)
    if(SRC_FOLDER[-1] != "/"):
        script_output("SRC_FOLDER should have a trailing /")
        exit(1)


def script_output(message, withName=True):  # (str, bool) -> None
    """
        Wrapper for print to include the script's name
    """
    if(withName is True):
        print(SCRIPT_NAME + ": " + message)
    else:
        print(message)

def get_prev_models():
    try:
        with open(DEST_FILE, 'r') as input_stream:
           return json.load(input_stream)[DB_NAME]

    except OSError:
        script_output("No existing models.json found")
        script_output("Creating empty models.json file in: " + DEST_FILE)
        with open(DEST_FILE, 'w') as output_stream:
            rawJSON = \
                json.JSONEncoder(sort_keys=True, indent=4).encode(RESULT_JSON)
            output_stream.write(rawJSON)
        return []

def get_model_files():
    model_files = []
    for file in os.listdir(SRC_FOLDER):
        if file.endswith("_model.json"):
            model_files.append(os.path.join(SRC_FOLDER, file))
    
    return model_files

def combine_models(model_files, known_models=[]):
    print(model_files, known_models)

if __name__ == "__main__":
    if(len(sys.argv) > 1):
        usage()
        exit(0)
    
    validate_config()

    combine_models(get_model_files(), get_prev_models())