# This module handles the models portion of the API server.

import json
from indra.user import user_log


def load_models(indra_dir):
    model_file = indra_dir + "/models/models.json"
    with open(model_file) as file:
        return json.loads(file.read())["models_database"]


def get_models(indra_dir):
    try:
        models_db = load_models(indra_dir)
    except FileNotFoundError:
        return {"ERROR": "Model file not found: indra dir is " + indra_dir}

    models_response = []
    for model in models_db:
        models_response.append({"model ID": model["model ID"],
                                "name": model["name"],
                                "doc": model.get("doc", ""),
                                "source": model.get("source", ""),
                                "graph": model.get("graph", "")})
    return models_response


def get_model(model_id, indra_dir=None, models_db=None):
    """
    Either indra_dir or models_db must be passed!
    """
    if models_db is None:
        try:
            models_db = load_models(indra_dir)
        except FileNotFoundError:
            return {"ERROR": "Model file not found: indra dir is " + indra_dir}
    for model in models_db:
        user_log("Model id:", model["model ID"])
        if int(model["model ID"]) == model_id:
            user_log("Matched model", model_id)
            return model
    raise KeyError
