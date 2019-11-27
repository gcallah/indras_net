"""
This file contains miscelenious .
"""
import os

from propargs.propargs import PropArgs


def get_func_name(f):
    if f is not None:
        return f.__name__
    else:
        return ""


def get_prop_path(model_name, model_dir="models"):
    ihome = os.getenv("INDRA_HOME", " ")
    return ihome + "/" + model_dir + "/props/" + model_name + ".props.json"


def get_props(model_nm, props=None, model_dir="models"):
    props_file = get_prop_path(model_nm, model_dir=model_dir)
    if props is None:
        pa = PropArgs.create_props(model_nm,
                                   ds_file=props_file)
    else:
        pa = PropArgs.create_props(model_nm,
                                   prop_dict=props)
    return pa
