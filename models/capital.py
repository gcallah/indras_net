"""
A basic model.
Places two groups of agents in the enviornment randomly
and moves them around randomly.
"""

from indra.utils import get_props
from indra.agent import Agent
from indra.composite import Composite
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.env import Env
from indra.display_methods import RED, BLUE

MODEL_NAME = "capital"
DEBUG = False  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_BLUE = 10

DEF_NUM_RED = 10

resource_holders = None #list of resource holders
entrepreneurs = None  #list of entrepreneur
market = None


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

    global resource_holders
    global entrepreneurs
    global market

    pa = get_props(MODEL_NAME, props)
    entrepreneurs = Composite("Entrepreneurs", {"color": BLUE},
                           member_creator=create_agent,
                           num_members=pa.get('num_blue', DEF_NUM_BLUE))
    resource_holders = Composite("Resource_holders", {"color": RED},
                          member_creator=create_agent,
                          num_members=pa.get('num_red', DEF_NUM_RED))

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
