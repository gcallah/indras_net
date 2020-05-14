#!/usr/bin/env python3

import json
import sys
import argparse

"""
    Combines all *_model.json files given and optionally, models.json file
    result outputs to stdout (default)

    Note: if no path to models.json is given (through --models_fp) but the file
    does exist, then script has no knowledge of any existing models that may
    have already been created. Thus, script will assign new model ids.

    Note 2: DO NOT ATTEMPT TO USE --models_fp with IO redirection that points
    to the same filepath given to --models_fp
    This will cause issues since IO redirection will truncate the file before
    the script has a chance to read the contents of the file.
"""

"""
    Usage:
    ./json_combiner.py [--models_fp] [filepaths...]

    Pass in the filepaths for *_model.json files

    --models_fp: optional flag to indicate the filepath to a models.json file
        This is used for the script to know about previously combined models
        (Will also store back the results to the same file)

    Default behavior: outputs to stdout
    Optional behavior: if given models_fp, then it will read from models_fp and
                        store result to models_fp
"""

DB_NAME = "models_database"
ID_FIELD = "model ID"
SOURCE_FIELD = "source"  # Used to determine new or old models

script_name = sys.argv[0]
model_id = 0  # Will be init to different value if models.json is given
result_json = {DB_NAME: []}


def validate_config():  # () -> None
    """
        Checks the configuration of this script
    """
    if(model_id < 0):
        script_output("model_id can't be negative")
        exit(1)


def script_output(message, withName=True):  # (str, bool) -> None
    """
        Wrapper for print to include the script's name
    """
    if(withName is True):
        print(script_name + ": " + message)
    else:
        print(message)


def save_result(dest_fp):
    """
        Handy function to encode result_json to json and save to file
    """
    with open(dest_fp, 'w') as output_stream:
        rawJSON = \
            json.JSONEncoder(sort_keys=True, indent=4).encode(result_json)
        output_stream.write(rawJSON)


def print_result():
    """
        Handy function to print result_json
    """
    print(json.JSONEncoder(sort_keys=True, indent=4).encode(result_json))


def get_prev_models(filepath):
    """
        Reads from models.json, which also happens to be our DEST_FOLDER
        If our DEST_FOLDER doesn't exist, it will just create the new file
        Otherwise, it will read in the json,
        so the script knows the model ID for exisiting models
    """
    try:
        with open(filepath, 'r') as input_stream:
            try:
                # Assumes models.json has DB_NAME that matches
                # what the script expects
                return json.load(input_stream)[DB_NAME]
            except ValueError:
                script_output("Invalid JSON in " + filepath)
                exit(1)

    except OSError:
        script_output("Could not open " + filepath)
        exit(1)


def get_models(model_files):
    """
        return all the models from list of model files (.json) for processing
    """
    model = []
    for file in model_files:
        if file.endswith("_model.json"):
            with open(file, 'r') as input_stream:
                try:
                    loadedData = json.load(input_stream)
                    if(len(loadedData) > 0):
                        model.append(loadedData)
                except ValueError:
                    script_output("Invalid JSON in " + file)
                    exit(1)
        else:
            script_output("File does not end with _model.json found")
            script_output(file, False)
            exit(1)

    return model


def init_model_id(known_models):
    """
        Sets model_id to be the next avaliable or free id for use
        Its based on whether there are existing models that the script is aware
        of. (if models.json doesn't exist, then it assume no existing models
        were ever created)
        model_id will default to 0 if no known model id were used
    """
    global model_id

    ids = []
    for model in known_models:
        ids.append(model[ID_FIELD])

    if(len(ids) > 0):
        model_id = max(ids)+1


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
        The old instance of the model will remain in models.json
    """
    global model_id
    new_models = []

    # Add models that are in known_models, but not in models to our result
    # Do not want to erase known_models if it happened to be more up to date
    # than what we have in registry/models
    for model in known_models:
        if(has_model(model[SOURCE_FIELD], models) is False):
            result_json[DB_NAME].append(model)

    # process the exisiting / known models first
    for model in models:
        knownID = get_model_id(model[SOURCE_FIELD], known_models)
        if(knownID == -1):
            new_models.append(model)
        else:
            model[ID_FIELD] = knownID
            result_json[DB_NAME].append(model)

    # Assign new models with unique IDs
    for model in new_models:
        model[ID_FIELD] = model_id
        result_json[DB_NAME].append(model)
        model_id += 1

    # Sort it out for neatness based on ID
    result_json[DB_NAME].sort(key=lambda model: model[ID_FIELD])


def main():
    validate_config()

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "filenames", nargs="+",
        help="indicate *_models.json files to combine"
    )
    arg_parser.add_argument(
        "--models_fp",
        help="indicate path to models.json file"
    )

    args = arg_parser.parse_args()

    model_files = args.filenames
    models_json_fp = args.models_fp

    # Step 1: try to load models from models.json if given
    prev_models = []

    if(models_json_fp is not None):
        if(models_json_fp.endswith(".json") is False):
            script_output("--models_fp is not referring to a *.json file")
            script_output("Please check your path", False)
            exit(1)

        prev_models = get_prev_models(models_json_fp)

    # Step 2: load models in from given list of *_model.json files
    models = get_models(model_files)

    # Step 3: change the init value of model_id to be
    # max(prev_model[model_id]) + 1
    init_model_id(prev_models)

    # Step 4: Combine models from models.json (known models) +
    # *_model.json (potentially new models)
    combine_models(models, prev_models)

    # If not none, then we have to save our result back to models_json_fp
    # We cannot use redirection because that truncates the file before we get a
    # chance to even read from models_json_fp
    if(models_json_fp is not None):
        save_result(models_json_fp)
    else:
        # Output result to stdout
        print_result()


if __name__ == "__main__":
    main()
