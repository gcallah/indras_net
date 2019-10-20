# This module handles the model creation portion of the API server.

from flask_restplus import fields
from APIServer.api_utils import json_converter
from indra.env import Env
from indra.composite import Composite


class AgentTypes(fields.Raw):
    def put(self, name):
        return Composite(name)


def get_model_creator():
    return {'feature_name':
            'This is the URL for the model creator: '
            + 'it is used with a PUT request.'}


def put_model_creator(model_features):
    allMembers = []
    # Loop to add composite(s) to membersList
    for mem in model_features["agent_names"]:
        allMembers.append(AgentTypes().put(mem))

    return json_converter(Env(model_features["model_name"],
                              members=allMembers,
                              width=model_features["env_width"],
                              height=model_features["env_height"]))
