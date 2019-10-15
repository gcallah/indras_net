# This module handles the models portion of the API server.

import json


def load_models(indra_dir):
    model_file = indra_dir + "/models/models.json"
    with open(model_file) as file:
        return json.loads(file.read())["models_database"]


def get_models(indra_dir):
    try:
        models_db = load_models(indra_dir)
    except FileNotFoundError:
        return {"ERROR": "Model file not found."}

    models_response = []
    for model in models_db:
        doc = ""
        if "doc" in model:
            doc = model["doc"]
        models_response.append({"model ID": model["model ID"],
                                "name": model["name"],
                                "doc": doc,
                                "source": model["source"]})
    return models_response
