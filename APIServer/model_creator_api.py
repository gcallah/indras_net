# This module handles the model creation portion of the API server.

from flask_restplus import fields

from APIServer.api_utils import json_converter, ENDPOINT_DESCR
from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env
from indra.space import in_hood

groups_arr = []
agents_arr = []


def generate_func(agent):
    global agents_arr
    global groups_arr

    within_hood = groups_arr[0].subset(in_hood, agent, 3, name="hood")

    print("There are ", len(within_hood), "agents within range")
    return False


class CreateGroups(fields.Raw):
    def addAgents(self, agent_name, num_of_agents):
        agents_arr = []
        for agent_num in range(1, num_of_agents + 1):
            agents_arr.append(Agent(agent_name + "_agent" + str(agent_num),
                                    action=generate_func,
                                    attrs={"John": "Knox"},))
        return agents_arr

    def put(self, group_list):
        global groups_arr
        global agents_arr
        for group in group_list:
            # add agents to the current group
            if group["num_of_agents"] > 0:  # want to add agents to the group
                agents_arr = self.addAgents(group["group_name"],
                                            group["num_of_agents"])
            # create the group
            groups_arr.append(Composite(group["group_name"],
                                        members=agents_arr, ))
        return groups_arr


def get_model_creator():
    return {ENDPOINT_DESCR: ' create a new model.'}


def put_model_creator(model_features):
    all_groups = CreateGroups().put(model_features["groups"])

    return json_converter(Env(model_features["model_name"],
                              members=all_groups,
                              width=model_features["env_width"],
                              height=model_features["env_height"]))
