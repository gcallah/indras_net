"""
This file contains miscelenious .
"""
import os


def get_prop_path(model_name):
    ihome = os.getenv("INDRA_HOME", " ")
    return ihome + "/models/props/" + model_name + ".props.json"
