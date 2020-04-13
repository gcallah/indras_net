import json

from APIServer.api_utils import json_converter, err_return
from APIServer.models_api import get_model
from indra.registry import get_env
from registry.run_dict import setup_dict

ENV_INSTANCE = 0


def get_props(model_id, indra_dir):
    try:
        model = get_model(model_id, indra_dir=indra_dir)
        with open(indra_dir + "/" + model["props"]) as file:
            return json.loads(file.read())
    except (IndexError, KeyError, ValueError):
        return err_return("Invalid model id " + str(model_id))
    except FileNotFoundError:
        return err_return("Models or props file not found")


def put_props(model_id, payload, indra_dir):
    model = get_model(model_id, indra_dir=indra_dir)
    setup_dict[model["run"]](props=payload)
    env = get_env()
    print(env)
    return json_converter(get_env())
