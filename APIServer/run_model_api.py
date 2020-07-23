
"""
This module restores an env from json and runs it.
"""
from APIServer.api_utils import json_converter
from registry.execution_registry import execution_registry
from registry.registry import clear_registry
from registry.run_dict import env_attrs
from indra.env import Env
from indra.user import user_log_notif
import pdb

def run_model_put(payload, run_time):
    """
    We create a dummy env that fills itself in to create
    the real env from the payload.
    """
    # env = Env(name='temp name', serial_obj=payload)
    # pdb.set_trace()
    execution_key=payload.get("execution_key")
    env = execution_registry.get_registered_env(execution_key)
    user_log_notif("Searching env attributes for " + env.name)
    if env.name in env_attrs:
        user_log_notif("Loading env attributes for " + env.name)
        env_attrs[env.name]()
        user_log_notif("Attributes for " + env.name + repr(env.attrs))
    else:
        user_log_notif(env.name + " not found in env_attrs")
    env.runN(periods=run_time, execution_key=execution_key)
    return json_converter(env)
