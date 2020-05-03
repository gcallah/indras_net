
"""
This module restores an env from json and runs it.
"""
from APIServer.api_utils import json_converter
from indra.env import Env
from indra.user import user_log_notif
from models.el_farol import MODEL_NAME as EFMODEL_NAME
from models.el_farol import set_env_attrs as ef_set_env_attrs
from models.forestfire import MODEL_NAME as FFMODEL_NAME
from models.forestfire import set_env_attrs as ff_set_env_attrs
from capital.money import MODEL_NAME as MNMODEL_NAME
from capital.money import set_env_attrs as mn_set_env_attrs
from capital.complementary import MODEL_NAME as CPMODEL_NAME
from capital.complementary import set_env_attrs as cp_set_env_attrs

env_attrs = {
    EFMODEL_NAME: ef_set_env_attrs,
    FFMODEL_NAME: ff_set_env_attrs,
    MNMODEL_NAME: mn_set_env_attrs,
    CPMODEL_NAME: cp_set_env_attrs,
}


def run_model_put(payload, run_time):
    """
    We create a dummy env that fills itself in to create
    the real env from the payload.
    """
    env = Env(name='temp name', serial_obj=payload)
    user_log_notif("Searching env attributes for " + env.name)
    if env.name in env_attrs:
        user_log_notif("Loading env attributes for " + env.name)
        env_attrs[env.name]()
        user_log_notif("Attributes for " + env.name + repr(env.attrs))
    env.runN(periods=run_time)
    return json_converter(env)
