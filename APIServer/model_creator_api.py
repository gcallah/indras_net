# This module handles the model creation portion of the API server.

from flask_restplus import fields

from APIServer.api_utils import json_converter
from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env


class AgentTypes(fields.Raw):
    def put(self, name):
        return Composite(name)


class CreateGroups(fields.Raw):
    def generateFunc(self, actions):
        for action in actions:
            if action == "Test":
                print("Just testing the actions!!")
        return False

    def addAgents(self, agent_name, agent_num, agent_actions):
        agents_arr = []
        i = 0
        while i < agent_num:
            agents_arr.append(Agent(agent_name + str(i + 1),
                                    action=self.generateFunc(agent_actions),
                                    ))
            i = i + 1
        return agents_arr

    def put(self, group_list):
        groups_arr = []
        agents_arr = []
        for group in group_list:
            # add agents to the current group
            if group["num_of_agents"] > 0:  # want to add agents to the group
                agents_arr = self.addAgents(group["group_name"],
                                            group["num_of_agents"],
                                            group["group_actions"])
            # create the group
            groups_arr.append(Composite(group["group_name"],
                                        members=agents_arr, ))
        return groups_arr

def get_model_creator():
    return {'feature_name': 'This is the URL for the model creator: '
                            + 'it is used with a PUT request.'}


def put_model_creator(model_features):
    # allMembers = []
    all_groups = CreateGroups().put(model_features["groups"])
    # Loop to add composite(s) to membersList
    # for mem in model_features["agent_names"]:
    # (in for loop)allMembers.append(AgentTypes().put(mem))

    return json_converter(Env(model_features["model_name"],
                              members=all_groups,
                              width=model_features["env_width"],
                              height=model_features["env_height"]))
