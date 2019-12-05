"""
A trade model.
Places two groups of agents in the enviornment randomly
and moves them around randomly.
"""

from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import RED, BLUE
from indra.env import Env
from indra.registry import registry
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.utils import get_props

import edgeworthbox as edge

MODEL_NAME = "trade"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_CAGENTS = 1
DEF_NUM_WAGENTS = 1
DEF_NUM_CHEESE = 4
DEF_NUM_WINE = 4

DEF_MAX_UTIL = max(DEF_NUM_CHEESE, DEF_NUM_WINE)

wine_group = None
cheese_group = None
env = None
max_util = DEF_MAX_UTIL


def trade(agent):
    pass


def create_wagent(name, i, props=None):
    return edge.create_wagent(name, i, props=None)


def create_cagent(name, i, props=None):
    return edge.create_cagent(name, i, props=None)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    return edge.set_up(props=None)


def main():
    global wine_group
    global cheese_group
    global env
    global max_util

    (env, cheese_group, wine_group, max_util) = set_up()

    if DEBUG2:
        env.user.tell(env.__repr__())

    env()
    return 0


if __name__ == "__main__":
    main()
