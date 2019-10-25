"""
A basic model.
Places two groups of agents in the enviornment randomly
and moves them around randomly.
"""
import copy
from indra.utils import get_props
from indra.agent import Agent
from indra.composite import Composite
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.env import Env
from indra.display_methods import RED, BLUE

MODEL_NAME = "capital"
DEBUG = False  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_ENTR = 10
DEF_NUM_RHOLDER = 10

DEF_ENTR_CASH = 10000
DEF_RHOLDER_CASH = 0
DEF_K_PRICE = 1000

DEF_RESOURCE_HOLD = {"land": 1000, "truck": 500, "labor": 200}
DEF_CAP_WANTED = {"land": 1000, "truck": 500, "labor": 200}

resource_holders = None  # list of resource holders
entrepreneurs = None  # list of entrepreneur
market = None


def entr_action(agent):
    nearby_rholder = market.get_neighbor_of_groupX(agent,
                                                   resource_holders,
                                                   hood_size=4)
    if nearby_rholder is not None:
        if agent["cash"] > 0:
            # try to buy a resource if you have cash
            for cap in agent["wants"].keys():
                # if find the resources entr want
                if cap in nearby_rholder["resources"].keys():
                    # update resources for the two groups
                    if cap not in agent["have"].keys():
                        agent["have"][cap] = 0
                    if nearby_rholder["resources"][cap] >= agent["wants"][cap]:
                        nearby_rholder["resources"][cap] -= agent["wants"][cap]
                        print(agent["wants"][cap], agent["have"][cap])
                        agent["have"][cap] += agent["wants"][cap]
                        agent["wants"][cap] = 0
                    else:
                        # rholder resources < entr wants
                        agent["wants"][cap] -= nearby_rholder["resources"][cap]
                        nearby_rholder["resources"][cap] = 0
                        agent["have"][cap] = nearby_rholder["resources"][cap]

                    if agent["wants"][cap] == 0:
                        agent["wants"].pop(cap)
                    if nearby_rholder["resources"][cap] == 0:
                        nearby_rholder["resources"].pop(cap)

                    # update cash for the two groups
                    agent["cash"] -= DEF_K_PRICE
                    nearby_rholder["cash"] += DEF_K_PRICE
                    break

            if agent["wants"] and agent["have"]:
                print("I'm " + agent.name + " and I will buy resources from "
                      + str(nearby_rholder) + ". I have "
                      + str(agent["cash"]) + " dollars left."
                      + " I want " + str(agent["wants"])
                      + ", and I have " + str(agent["have"]) + ".")
            elif agent["wants"]:
                print("I'm " + agent.name + " and I will buy resources from "
                      + str(nearby_rholder) + ". I have "
                      + str(agent["cash"]) + " dollars left."
                      + " I want " + str(agent["wants"])
                      + ", and I don't have any capital.")
            elif agent["have"]:
                print("I'm " + agent.name + " and I will buy resources from "
                      + str(nearby_rholder) + ". I have "
                      + str(agent["cash"]) + " dollars left."
                      + " I got all I need, and I have "
                      + str(agent["have"]) + "!")
            return False
            # move to find resource holder

        else:
            print("I'm " + agent.name + " and I'm broke!")
    else:
        print("I'm " + agent.name + " and I can't find resources.")
    return True


def rholder_action(agent):
    if agent["resources"]:
        print("I'm " + agent.name + " and I've got resources. I have "
              + str(agent["cash"]) + " dollors now."
              + " I have " + str(agent["resources"]) + ".")
    else:
        print("I'm " + agent.name + " and I've got resources. I have "
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

    return Agent(name + str(i), action=entr_action,
                 attrs={"cash": starting_cash,
                        "wants": copy.deepcopy(DEF_CAP_WANTED),
                        "have": {}})


def create_rholder(name, i, props=None):
    """
    Create an agent.
    """
    return Agent(name + str(i), action=rholder_action,
                 attrs={"cash": DEF_RHOLDER_CASH,
                        "resources": copy.deepcopy(DEF_RESOURCE_HOLD)})


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
        print(market.__repr__())

    market()
    return 0


if __name__ == "__main__":
    main()
