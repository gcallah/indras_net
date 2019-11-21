"""
A basic model.
Places two groups of agents in the enviornment randomly
and moves them around randomly.
"""
import copy
import random

from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import RED, BLUE
from indra.env import Env
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.utils import get_props

MODEL_NAME = "capital"
DEBUG = False  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_ENTR = 10
DEF_NUM_RHOLDER = 10
DEF_TOTAL_RESOURCES_ENTR_WANT = 2000
DEF_TOTAL_RESOURCES_RHOLDER_HAVE = 3000

DEF_ENTR_CASH = 10000
DEF_RHOLDER_CASH = 0
DEF_K_PRICE = 1


DEF_RESOURCE_HOLD = {"land": 1000, "truck": 500, "building": 200}
DEF_CAP_WANTED = {"land": 1000, "truck": 500, "building": 200}

resource_holders = None  # list of resource holders
entrepreneurs = None  # list of entrepreneur
market = None


def entr_action(agent):
    if agent["cash"] > 0:
        nearby_rholder = market.get_neighbor_of_groupX(agent,
                                                       resource_holders,
                                                       hood_size=4)
        if nearby_rholder is not None:
            # try to buy a resource if you have cash
            for good in agent["wants"].keys():
                price = nearby_rholder["price"]
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
                    if agent["wants"][good] == 0:
                        agent["wants"].pop(good)
                    if nearby_rholder["resources"][good] == 0:
                        nearby_rholder["resources"].pop(good)
                    break

            if agent["wants"] and agent["have"]:
                market.user.tell("I'm " + agent.name
                                 + " and I will buy resources from "
                                 + str(nearby_rholder) + ". I have "
                                 + str(agent["cash"]) + " dollars left."
                                 + " I want " + str(agent["wants"])
                                 + ", and I have " + str(agent["have"]) + ".")
            elif agent["wants"]:
                market.user.tell("I'm " + agent.name
                                 + " and I will buy resources from "
                                 + str(nearby_rholder) + ". I have "
                                 + str(agent["cash"]) + " dollars left."
                                 + " I want " + str(agent["wants"])
                                 + ", and I don't have any capital.")
            elif agent["have"]:
                market.user.tell("I'm " + agent.name
                                 + " and I will buy resources from "
                                 + str(nearby_rholder) + ". I have "
                                 + str(agent["cash"]) + " dollars left."
                                 + " I got all I need, and I have "
                                 + str(agent["have"]) + "!")
            return False
            # move to find resource holder

        else:
            market.user.tell("I'm " + agent.name + " and I'm broke!")
    else:
        market.user.tell("I'm " + agent.name + " and I can't find resources.")
    return True


def rholder_action(agent):
    if agent["resources"]:
        market.user.tell("I'm " + agent.name
                         + " and I've got resources. I have "
                         + str(agent["cash"]) + " dollors now."
                         + " I have " + str(agent["resources"]) + ".")
    else:
        market.user.tell("I'm " + agent.name
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
        starting_cash = props.get('entr_starting_cash',
                                  DEF_ENTR_CASH)

    resources = copy.deepcopy(DEF_CAP_WANTED)
    if props is not None:
        total_resources = props.get('entr_want_resource_total',
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
    if props is not None:
        k_price = props.get('cap_price',
                            DEF_K_PRICE)

    starting_cash = DEF_RHOLDER_CASH
    if props is not None:
        starting_cash = props.get('rholder_starting_cash',
                                  DEF_RHOLDER_CASH)

    resources = copy.deepcopy(DEF_CAP_WANTED)
    if props is not None:
        total_resources = props.get('rholder_starting_resource_total',
                                    DEF_TOTAL_RESOURCES_RHOLDER_HAVE)
        num_resources = len(resources)
        for k in resources.keys():
            resources[k] = int((total_resources * 2)
                               * (random.random() / num_resources))

    return Agent(name + str(i), action=rholder_action,
                 attrs={"cash": starting_cash,
                        "resources": resources,
                        "price": k_price})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """

    global resource_holders
    global entrepreneurs
    global market

    pa = get_props(MODEL_NAME, props)
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

    market = Env("neighborhood",
                 height=pa.get('grid_height', DEF_HEIGHT),
                 width=pa.get('grid_width', DEF_WIDTH),
                 members=[resource_holders, entrepreneurs],
                 props=pa)

    return (market, resource_holders, entrepreneurs)


def main():
    global resource_holders
    global entrepreneurs
    global market

    (market, blue_group, red_group) = set_up()

    if DEBUG2:
        market.user.tell(market.__repr__())

    market()
    return 0


if __name__ == "__main__":
    main()
