import json
from APIServer.api_utils import json_converter, err_return
from APIServer.models_api import load_models
from models.run_dict_helper import setup_dict


def get_props(model_id, indra_dir):
    try:
        models_db = load_models(indra_dir)
        with open(indra_dir + "/" + models_db[model_id]["props"]) as file:
            model_prop = json.loads(file.read())
            return model_prop
    except (IndexError, KeyError, ValueError):
        return err_return("Invalid model id " + str(model_id))
    except FileNotFoundError:
        return err_return("Models or props file not found")


def put_props(model_id, payload, indra_dir):
    models_db = load_models(indra_dir)
    ret = setup_dict[models_db[model_id]["run"]](props=payload)
    env = ret[0]   # what the hey is 0 here? named constants!
    return json_converter(env)
