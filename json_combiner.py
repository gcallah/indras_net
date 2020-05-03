#!/usr/bin/env python3

import json
import sys
import os

"""
    Combines all *_model.json files in registry/models
    to one models.json file
"""


DEST_FILE = "registry/models/models.json"
SRC_FOLDER = "registry/models/"  # must have trailing /
SCRIPT_NAME = sys.argv[0]
DB_NAME = "models_database"
ID_FIELD = "model ID"
SOURCE_FIELD = "source"  # Used to determine new or old models
RESULT_JSON = {DB_NAME: []}
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
    """
        Handy function to saves RESULTJSON to the DEST_FILE
    """
    with open(DEST_FILE, 'w') as output_stream:
        rawJSON = \
            json.JSONEncoder(sort_keys=True, indent=4).encode(RESULT_JSON)
        output_stream.write(rawJSON)


def get_prev_models():
    """
        Reads from models.json, which also happens to be our DEST_FILE
        If our DEST_FILE doesn't exist, it will just create the new file
        Otherwise, it will read in the json,
        so the script knows the model ID for exisiting models
    """
    try:
        with open(DEST_FILE, 'r') as input_stream:
            return json.load(input_stream)[DB_NAME]

    except OSError:
        script_output("No existing models.json found")
        script_output("Creating empty models.json file in: " + DEST_FILE)
        save_result()
        return []


def get_model_files():
    """
        Gets all the filepaths for *_model.json files from the SRC_FOLDER
    """
    model_files = []
    for file in os.listdir(SRC_FOLDER):
        if file.endswith("_model.json"):
            model_files.append(os.path.join(SRC_FOLDER, file))

    return model_files


def load_models(model_files):
    """
        Loads all the models from list of model files (.json) for processing
    """
    model = []
    for file in model_files:
        with open(file, 'r') as input_stream:
            model.append(json.load(input_stream))

    return model


def init_model_id(known_models):
    """
        Sets model_id to be the next avaliable or free id for use
        Its based on whether there are existing models that the script is aware
        of. (if models.json doesn't exist, then it assume no existing models
        were ever created)
        MODEL_ID will default to 0 if no known model id were used
    """
    global MODEL_ID

    ids = []
    for model in known_models:
        ids.append(model[ID_FIELD])

    if(len(ids) > 0):
        MODEL_ID = max(ids)+1


def get_model_id(targetValue, known_models):
    """
        Gets the model id for the model with given targetValue
        targetValue should be the source since its used as the unique feature
        of each model
    """
    id = -1
    for model in known_models:
        if(targetValue == model[SOURCE_FIELD]):
            id = model[ID_FIELD]
            break

    return id


def has_model(targetValue, models):
    """
        Checks if a model exists with given targetValue
        Model should have source_field
    """
    for model in models:
        if(targetValue == model[SOURCE_FIELD]):
            return True

    return False


def combine_models(models, known_models=[]):
    """
        Merges known models (from models.json) with models from
        model.json files

        models.json could have models that don't have a model.json files

        combine_models() just puts every unique models into our set

        Note: this script's definition of unique is purely based on "source"
        field. The reason is that a model's source should not be the same
        as another model.

        This does mean that if a model's source is changed,
        a new model id is assigned.
        The old instance of the model will remain in model.json
    """
    global MODEL_ID
    new_models = []

    # Add models that are in known_models, but not in models to our result
    # Do not want to erase known_models if it happened to be more up to date
    # than what we have in registry/models
    for model in known_models:
        if(has_model(model[SOURCE_FIELD], models) is False):
            RESULT_JSON[DB_NAME].append(model)

    # process the exisiting / known models first
    for model in models:
        knownID = get_model_id(model[SOURCE_FIELD], known_models)
        if(knownID == -1):
            new_models.append(model)
        else:
            model[ID_FIELD] = knownID
            RESULT_JSON[DB_NAME].append(model)

    # Assign new models with unique IDs
    for model in new_models:
        model[ID_FIELD] = MODEL_ID
        RESULT_JSON[DB_NAME].append(model)
        MODEL_ID += 1

    # Sort it out for neatness based on ID
    RESULT_JSON[DB_NAME].sort(key=lambda model: model[ID_FIELD])

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
