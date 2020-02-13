"""
A basic model.
Places two groups of agents in the enviornment randomly
and moves them around randomly.
"""

from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import RED, BLUE
from indra.env import Env
from indra.registry import get_env
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.utils import get_props

MODEL_NAME = "basic"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_BLUE = 10

DEF_NUM_RED = 10


def agent_action(agent):
    print("I'm " + agent.name + " and I'm acting.")
    # return False means to move
    return False


def create_agent(name, i, props=None):
    """
    Create an agent.
    """
    return Agent(name + str(i), action=agent_action)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    pa = get_props(MODEL_NAME, props)
    blue_group = Composite("Blues", {"color": BLUE},
                           member_creator=create_agent,
                           num_members=pa.get('num_blue', DEF_NUM_BLUE))
    red_group = Composite("Reds", {"color": RED},
                          member_creator=create_agent,
                          num_members=pa.get('num_red', DEF_NUM_RED))

    Env("env",
        height=pa.get('grid_height', DEF_HEIGHT),
        width=pa.get('grid_width', DEF_WIDTH),
        members=[blue_group, red_group],
        props=pa)


def main():
    set_up()

    get_env()()
    return 0


if __name__ == "__main__":
    main()
