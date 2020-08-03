"""
This module restores an env from json and runs it.
"""
from APIServer.api_utils import json_converter
from registry.run_dict import env_attrs
from indra.env import Env
from indra.user import user_log_notif
from registry.execution_registry import EXECUTION_KEY_NAME, \
    is_model_ported_to_new_registry, COMMANDLINE_EXECUTION_KEY


def run_model_put(payload, run_time):
    """
    We create a dummy env that fills itself in to create
    the real env from the payload.
    """
    if not is_model_ported_to_new_registry(
            payload.get("name")
    ):
        payload[EXECUTION_KEY_NAME] = COMMANDLINE_EXECUTION_KEY
    execution_key = payload.get(EXECUTION_KEY_NAME)
    env = Env(name="temp_env", serial_obj=payload, execution_key=execution_key)
    user_log_notif("Searching env attributes for " + env.name)
    if env.name in env_attrs:
        user_log_notif("Loading env attributes for " + env.name)
        env_attrs[env.name](execution_key=execution_key)
        user_log_notif("Attributes for " + env.name + repr(env.attrs))
    else:
        user_log_notif(env.name + " not found in env_attrs")
    env.runN(periods=run_time, execution_key=execution_key)
    return json_converter(env)
