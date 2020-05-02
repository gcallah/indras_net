#!/usr/bin/env python3

"""
    Combines all *_model.json files in registry/models
    to one models.json file
"""

import json
import sys
import os
import copy

DEST_FILE = "registry/models/models.json"
SRC_FOLDER = "registry/models/"  # must have trailing /
SCRIPT_NAME = sys.argv[0]
DB_NAME = "models_database"
ID_FIELD = "model ID"
NAME_FIELD = "name"
RESULT_JSON = { DB_NAME : [] }
MODEL_ID = 0

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

def save_result():
    with open(DEST_FILE, 'w') as output_stream:
        rawJSON = \
            json.JSONEncoder(sort_keys=True, indent=4).encode(RESULT_JSON)
        output_stream.write(rawJSON)

def get_prev_models():
    try:
        with open(DEST_FILE, 'r') as input_stream:
           return json.load(input_stream)[DB_NAME]

    except OSError:
        script_output("No existing models.json found")
        script_output("Creating empty models.json file in: " + DEST_FILE)
        save_result()
        return []

def get_model_files():
    model_files = []
    for file in os.listdir(SRC_FOLDER):
        if file.endswith("_model.json"):
            model_files.append(os.path.join(SRC_FOLDER, file))
    
    return model_files

def load_models(model_files):
    model = []
    for file in model_files:
        with open(file, 'r') as input_stream:
            model.append(json.load(input_stream))
    
    return model

def init_model_id(known_models):
    global MODEL_ID

    ids = []
    for model in known_models:
        ids.append(model[ID_FIELD])
    
    if(len(ids) > 0):
        MODEL_ID = max(ids)+1

def get_model_id(targetName, known_models):
    id = -1
    for model in known_models:
        if(targetName == model[NAME_FIELD]):
            id = model[ID_FIELD]
            break

    return id

def combine_models(models, known_models=[]):
    #print(models, known_models)
    global MODEL_ID
    new_models = []

    # process the exisiting / known models first
    for model in models:
        knownID = get_model_id(model[NAME_FIELD], known_models)
        if(knownID == -1):
            new_models.append(model)
        else:
            model[ID_FIELD] = knownID
            RESULT_JSON[DB_NAME].append(model)
    
    #print(new_models)

    for model in new_models:
        model[ID_FIELD] = MODEL_ID
        RESULT_JSON[DB_NAME].append(model)
        MODEL_ID += 1

    # write out to DEST_FILE
    save_result()

if __name__ == "__main__":
    if(len(sys.argv) > 1):
        usage()
        exit(0)
    
    validate_config()

    models = load_models(get_model_files())
    prev_models = get_prev_models()
    init_model_id(prev_models)

    combine_models(models, prev_models)