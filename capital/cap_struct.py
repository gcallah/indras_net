"""
A model for capital structure.
Places two groups of agents in the enviornment randomly
and moves them around randomly.
"""
import copy
import random

from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import RED, BLUE
from indra.env import Env
from registry.registry import get_env, get_prop
from registry.registry import user_tell
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.utils import init_props

MODEL_NAME = "capital"
DEBUG = False  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_ENTR = 10
DEF_NUM_RHOLDER = 10
DEF_TOTAL_RESOURCES_ENTR_WANT = 20000
DEF_TOTAL_RESOURCES_RHOLDER_HAVE = 30000

DEF_ENTR_CASH = 100000
DEF_RHOLDER_CASH = 0
DEF_K_PRICE = 1


DEF_RESOURCE_HOLD = {"land": 1000, "truck": 500, "building": 200}
DEF_CAP_WANTED = {"land": 1000, "truck": 500, "building": 200}
DEF_EACH_CAP_PRICE = {"land": DEF_K_PRICE,
                      "truck": DEF_K_PRICE,
                      "building": DEF_K_PRICE}

resource_holders = None  # list of resource holders
entrepreneurs = None  # list of entrepreneur


def dict_to_string(dict):
    return " ".join(good + " {0:.2f}".format(amt)
                    for good, amt in dict.items())


def entr_action(agent, **kwargs):
    if agent["cash"] > 0:
        nearby_rholder = get_env().get_neighbor_of_groupX(agent,
                                                          resource_holders,
                                                          hood_size=4)
        if nearby_rholder is not None:
            # try to buy a resource if you have cash
            for good in agent["wants"].keys():
                price = nearby_rholder["price"][good]
                entr_max_buy = min(agent["cash"], agent["wants"][good] * price)
                # if find the resources entr want
                if good in nearby_rholder["resources"].keys():
                    trade_amt = min(entr_max_buy,
                                    nearby_rholder["resources"][good])
                    # update resources for the two groups
                    if good not in agent["have"].keys():
                        agent["have"][good] = trade_amt
                    agent["have"][good] += trade_amt
                    agent["wants"][good] -= trade_amt
                    nearby_rholder["resources"][good] -= trade_amt
                    nearby_rholder["cash"] += trade_amt * price
                    agent["cash"] -= trade_amt * price
                    if agent["wants"][good] <= 0:
                        agent["wants"].pop(good)
                    if nearby_rholder["resources"][good] <= 0:
                        nearby_rholder["resources"].pop(good)
                    break

            if agent["wants"] and agent["have"]:
                user_tell("I'm " + agent.name
                          + " and I will buy resources from "
                          + str(nearby_rholder) + ". I have "
                          + "{0:.2f}".format(agent["cash"])
                          + " dollars left."
                          + " I want "
                          + dict_to_string(agent["wants"])
                          + ", and I have "
                          + dict_to_string(agent["have"]) + ".")
            elif agent["wants"]:
                user_tell("I'm " + agent.name
                          + " and I will buy resources from "
                          + str(nearby_rholder) + ". I have "
                          + "{0:.2f}".format(agent["cash"])
                          + " dollars left."
                          + " I want "
                          + dict_to_string(agent["wants"])
                          + ", and I don't have any capital.")
            elif agent["have"]:
                user_tell("I'm " + agent.name
                          + " and I will buy resources from "
                          + str(nearby_rholder) + ". I have "
                          + "{0:.2f}".format(agent["cash"])
                          + " dollars left."
                          + " I got all I need, and I have "
                          + dict_to_string(agent["have"]) + "!")
            return False
            # move to find resource holder

        else:
            user_tell("I'm " + agent.name + " and I'm broke!")
    else:
        user_tell("I'm " + agent.name
                  + " and I can't find resources.")
    return True


def rholder_action(agent, **kwargs):
    if agent["resources"]:
        get_env().user.tell("I'm " + agent.name
                            + " and I've got resources. I have "
                            + str(agent["cash"]) + " dollors now."
                            + " I have " + str(agent["resources"]) + ".")
    else:
        get_env().user.tell("I'm " + agent.name
                            + " and I've got resources. I have "
                            + str(agent["cash"]) + " dollors now."
                            + " I ran out of resources!")
    # resource holder dont move
    return True


def create_entr(name, i, props=None):
    """
    Create an agent.
    """
    starting_cash = DEF_ENTR_CASH
    if props is not None:
        starting_cash = get_prop('entr_starting_cash',
                                 DEF_ENTR_CASH)

    resources = copy.deepcopy(DEF_CAP_WANTED)
    if props is not None:
        total_resources = get_prop('entr_want_resource_total',
                                   DEF_TOTAL_RESOURCES_ENTR_WANT)
        num_resources = len(resources)
        for k in resources.keys():
            resources[k] = int((total_resources * 2)
                               * (random.random() / num_resources))

    return Agent(name + str(i), action=entr_action,
                 attrs={"cash": starting_cash,
                        "wants": resources,
                        "have": {}})


def create_rholder(name, i, props=None):
    """
    Create an agent.
    """
    k_price = DEF_K_PRICE
    resources = copy.deepcopy(DEF_CAP_WANTED)
    num_resources = len(resources)

    price_list = copy.deepcopy(DEF_EACH_CAP_PRICE)
    if props is not None:
        k_price = props.get('cap_price',
                            DEF_K_PRICE)
        for k in price_list.keys():
            price_list[k] = float("{0:.2f}".format(float(k_price
                                                         * random.uniform(0.5,
                                                                          1.5)
                                                         )))

    starting_cash = DEF_RHOLDER_CASH
    if props is not None:
        starting_cash = get_prop('rholder_starting_cash',
                                 DEF_RHOLDER_CASH)

    if props is not None:
        total_resources = get_prop('rholder_starting_resource_total',
                                   DEF_TOTAL_RESOURCES_RHOLDER_HAVE)
        for k in resources.keys():
            resources[k] = int((total_resources * 2)
                               * (random.random() / num_resources))

    return Agent(name + str(i), action=rholder_action,
                 attrs={"cash": starting_cash,
                        "resources": resources,
                        "price": price_list})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """

    global resource_holders
    global entrepreneurs

    pa = init_props(MODEL_NAME, props, model_dir="capital")
    entrepreneurs = Composite("Entrepreneurs", {"color": BLUE},
                              member_creator=create_entr,
                              props=pa,
                              num_members=pa.get('num_entr',
                                                 DEF_NUM_ENTR))
    resource_holders = Composite("Resource_holders", {"color": RED},
                                 member_creator=create_rholder,
                                 props=pa,
                                 num_members=pa.get('num_rholder',
                                                    DEF_NUM_RHOLDER))

    Env("neighborhood",
        height=get_prop('grid_height', DEF_HEIGHT),
        width=get_prop('grid_width', DEF_WIDTH),
        members=[resource_holders, entrepreneurs])

    return resource_holders, entrepreneurs


def main():
    global resource_holders
    global entrepreneurs

    (blue_group, red_group) = set_up()

    if DEBUG2:
        get_env().user.tell(get_env().__repr__())

    get_env()()
    return 0


if __name__ == "__main__":
    main()
