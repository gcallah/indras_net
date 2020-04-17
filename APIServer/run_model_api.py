
"""
This module restores an env from json and runs it.
"""
from APIServer.api_utils import json_converter
from indra.env import Env
from models.el_farol import MODEL_NAME as EFMODEL_NAME
from models.el_farol import set_env_attrs as ef_set_env_attrs
from models.forestfire import MODEL_NAME as FFMODEL_NAME
from models.forestfire import set_env_attrs as ff_set_env_attrs

env_attrs = {
    EFMODEL_NAME: ef_set_env_attrs,
    FFMODEL_NAME: ff_set_env_attrs,
}


def run_model_put(payload, run_time):
    """
    We create a dummy env that fills itself in to create
    the real env from the payload.
    """
    env = Env(name='temp name', serial_obj=payload)
    if env.name in env_attrs:
        env_attrs[env.name]()
    env.runN(periods=run_time)
    return json_converter(env)
