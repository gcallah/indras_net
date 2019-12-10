"""
This file contains miscellaneous.
"""
import os

from propargs.propargs import PropArgs


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


def get_props(model_nm, props=None, model_dir="models",
              skip_user_questions=False):
    props_file = get_prop_path(model_nm, model_dir=model_dir)
    if props is None:
        pa = PropArgs.create_props(model_nm,
                                   ds_file=props_file,
                                   skip_user_questions=skip_user_questions)
    else:
        pa = PropArgs.create_props(model_nm,
                                   prop_dict=props,
                                   skip_user_questions=skip_user_questions)
    return pa
