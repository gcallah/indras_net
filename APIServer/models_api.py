# This module handles the models portion of the API server.

import json
from indra.user import user_log_notif, user_log_err
from APIServer.api_utils import ERROR

REGISTRY = "registry"
MODELS_DB = "models.json"
MODEL_FILE = "/" + REGISTRY + "/" + MODELS_DB

MODEL_ID = "model ID"


def load_models(indra_dir):
    model_file = indra_dir + MODEL_FILE
    with open(model_file) as file:
        return json.loads(file.read())["models_database"]


def get_models(indra_dir):
    try:
        models_db = load_models(indra_dir)
    except FileNotFoundError:
        return {ERROR: "Model file not found: indra dir is " + indra_dir}

    models_response = []
    for model in models_db:
        models_response.append(model)
    return models_response


def get_model(model_id, indra_dir=None, models_db=None):
    """
    Either indra_dir or models_db must be passed!
    """
    if models_db is None:
        try:
            models_db = load_models(indra_dir)
        except FileNotFoundError:
            msg = user_log_err("Model file not found: indra_dir is: " +
                               indra_dir)
            return {ERROR: msg}
    for model in models_db:
        if int(model[MODEL_ID]) == model_id:
            user_log_notif("Matched model: " + model["name"])
            return model
    msg = user_log_err("Model id not found: " + str(model_id))
    return {ERROR: msg}
