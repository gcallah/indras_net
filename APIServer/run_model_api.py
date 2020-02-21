
"""
This module restores an env from json and runs it.
"""
from APIServer.api_utils import json_converter
from indra.env import Env


def run_model_put(payload, run_time):
    """
    We create a dummy env that fills itself in to create
    the real env from the payload.
    """
    env = Env(name='temp name', serial_obj=payload)
    env.runN(periods=run_time)
    return json_converter(env)
