"""
A basic model.
Places two groups of agents in the enviornment randomly
and moves them around randomly.
"""

from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import RED, BLUE
from indra.env import Env
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.utils import get_props

MODEL_NAME = "edgeworthbox"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_CAGENTS = 1
DEF_NUM_WAGENTS = 1
DEF_NUM_CHEESE = 10
DEF_NUM_WINE = 10

wine_group = None
cheese_group = None
env = None


def gen_util_func(qty):
    return 10 - 0.5 * qty


def seek_a_trade(agent):

    nearby_agent = env.get_neighbor_of_groupX(agent,
                                              cheese_group,
                                              hood_size=4)

    if nearby_agent is not None:
        env.user.tell("I'm " + agent.name + " and I find "
                      + nearby_agent.name)

    if "cheese" not in agent["goods"].keys():
        add_good(agent, "cheese")
    if "wine" not in agent["goods"].keys():
        add_good(agent, "wine")

    env.user.tell("I'm " + agent.name
                  + ". I have " + str(agent["goods"]["wine"]["endow"])
                  + " wine and "
                  + str(agent["goods"]["cheese"]["endow"]) + " cheese.")

    # return False means to move
    return False


def endow(agent, good, new_endow, util_func=None):
    return


def incr_util(agent, good, incr):
    return


def rec_offer(agent, good, amt, counterparty):
    return


def rec_reply(agent, my_good, my_amt, his_good, his_amt):
    return


def trade(agent, my_good, my_amt, counterparty, his_good, his_amt):
    return


def util_gain(agent):
    return


def marginal_util(agent, good, amt):
    return


def add_good(agent, good):
    agent["goods"][good] = {"endow": 0,
                            "util_func": gen_util_func,
                            "incr": 0.0}


def create_wagent(name, i, props=None):
    start_wine = DEF_NUM_WINE
    if props is not None:
        start_wine = props.get('start_wine',
                               DEF_NUM_WINE)
    return Agent(name + str(i), action=seek_a_trade,
                 attrs={"goods": {"wine": {"endow": start_wine,
                                           "util_func": gen_util_func,
                                           "incr": 0}}})


def create_cagent(name, i, props=None):
    start_cheese = DEF_NUM_CHEESE
    if props is not None:
        start_cheese = props.get('start_cheese',
                                 DEF_NUM_CHEESE)
    return Agent(name + str(i), action=seek_a_trade,
                 attrs={"goods": {"cheese": {"endow": start_cheese,
                                             "util_func": gen_util_func,
                                             "incr": 0}}})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    pa = get_props(MODEL_NAME, props, model_dir="capital")
    cheese_group = Composite("Cheese holders", {"color": BLUE},
                             member_creator=create_cagent,
                             props=pa,
                             num_members=pa.get('num_cagents',
                                                DEF_NUM_CAGENTS))
    wine_group = Composite("Wine holders", {"color": RED},
                           member_creator=create_wagent,
                           props=pa,
                           num_members=pa.get('num_wagents',
                                              DEF_NUM_WAGENTS))

    env = Env("env",
              height=pa.get('grid_height', DEF_HEIGHT),
              width=pa.get('grid_width', DEF_WIDTH),
              members=[cheese_group, wine_group],
              props=pa)

    return (env, cheese_group, wine_group)


def main():
    global wine_group
    global cheese_group
    global env

    (env, cheese_group, wine_group) = set_up()

    if DEBUG2:
        env.user.tell(env.__repr__())

    env()
    return 0


if __name__ == "__main__":
    main()
