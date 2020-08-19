"""
This file contains miscellaneous.
"""
import os
import random

from propargs.propargs import PropArgs

from registry.execution_registry import execution_registry, EXEC_KEY
from registry.execution_registry import CLI_EXEC_KEY


def gaussian(mean, sigma, trim_at_zero=True):
    sample = random.gauss(mean, sigma)
    if trim_at_zero:
        if sample < 0:
            sample *= -1
    return sample


def get_func_name(f):
    # Until Agent.restore and Env.to_json can restore functions from function
    # names, strings will be returned as-is.
    if isinstance(f, str):
        return f
    elif f is not None:
        return f.__name__
    else:
        return ""


def get_prop_path(model_name, model_dir="models"):
    ihome = os.getenv("INDRA_HOME", " ")
    return ihome + "/" + model_dir + "/props/" + model_name + ".props.json"


def init_props(model_nm, props=None, model_dir="models",
               skip_user_questions=False):
    props_file = get_prop_path(model_nm, model_dir=model_dir)
    execution_key = CLI_EXEC_KEY if props is None else int(
        props.get(EXEC_KEY).get("val"))
    if props is None:
        pa = PropArgs.create_props(model_nm,
                                   ds_file=props_file,
                                   skip_user_questions=skip_user_questions)
    else:
        pa = PropArgs.create_props(model_nm,
                                   prop_dict=props,
                                   skip_user_questions=skip_user_questions)

    # we keep props available in registry:
    execution_registry.set_propargs(execution_key, pa)
    return pa


def get_props(model_nm, props=None, model_dir="models",
              skip_user_questions=False):
    """
    This name for the function is deprecated: use init_props()
    """
    return init_props(model_nm, props=props, model_dir=model_dir,
                      skip_user_questions=skip_user_questions)
