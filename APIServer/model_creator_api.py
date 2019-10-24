# This module handles the model creation portion of the API server.

from flask_restplus import fields
from APIServer.api_utils import json_converter
from indra.env import Env
from indra.agent import Agent
from indra.composite import Composite


class AgentTypes(fields.Raw):
    def put(self, name):
        return Composite(name)


class CreateGroups(fields.Raw):
    def addAgents(self, agent_name, agent_num):
        agentsArr = []
        i = 0
        while i < agent_num:
            agentsArr.append(Agent(agent_name + str(i + 1)))
            i = i + 1
        return agentsArr

    def put(self, group_list):
        groupsArr = []
        agentsArr = []
        for group in group_list:
            # add agents to the current group
            if group["num_of_agents"] > 0:  # want to add agents to the group
                agentsArr = self.addAgents(group["group_name"],
                                           group["num_of_agents"])
            # create the group
            groupsArr.append(Composite(group["group_name"],
                                       members=agentsArr,))
        return groupsArr


def get_model_creator():
    return {'feature_name':
            'This is the URL for the model creator: '
            + 'it is used with a PUT request.'}


def put_model_creator(model_features):
    # allMembers = []
    allGroups = CreateGroups().put(model_features["groups"])
    # Loop to add composite(s) to membersList
    # for mem in model_features["agent_names"]:
    # (in for loop)allMembers.append(AgentTypes().put(mem))

    return json_converter(Env(model_features["model_name"],
                              members=allGroups,
                              width=model_features["env_width"],
                              height=model_features["env_height"]))
