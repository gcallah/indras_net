"""
This file contains miscelenious .
"""
import os

from propargs.propargs import PropArgs


def get_prop_path(model_name):
    ihome = os.getenv("INDRA_HOME", " ")
    return ihome + "/models/props/" + model_name + ".props.json"


def get_props(model_nm, props=None):
    ds_file = get_prop_path(model_nm)
    if props is None:
        pa = PropArgs.create_props(model_nm,
                                   ds_file=ds_file)
    else:
        pa = PropArgs.create_props(model_nm,
                                   prop_dict=props)
    return pa
