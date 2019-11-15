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

MODEL_NAME = "basic"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_CAGENTS = 1
DEF_NUM_WAGENTS = 1

wine_group = None
cheese_group = None
env = None


def seek_a_trade(agent):
    print("I'm " + agent.name + " and I'm acting.")
    # return False means to move
    return False


def create_wagent(name, i, props=None):
    """
    Create an agent.
    """
    return Agent(name + str(i), action=seek_a_trade,
                 attrs={"wine": 20, "cheese": 0})


def create_cagent(name, i, props=None):
    """
    Create an agent.
    """
    return Agent(name + str(i), action=seek_a_trade,
                 attrs={"wine": 0, "cheese": 20})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    pa = get_props(MODEL_NAME, props)
    cheese_group = Composite("Cheese holders", {"color": BLUE},
                           member_creator=create_cagent,
                           num_members=pa.get('num_cagents', DEF_NUM_CAGENTS))
    wine_group = Composite("Wine holders", {"color": RED},
                          member_creator=create_wagent,
                          num_members=pa.get('num_wagents', DEF_NUM_WAGENTS))

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
        print(env.__repr__())

    env()
    return 0


if __name__ == "__main__":
    main()
