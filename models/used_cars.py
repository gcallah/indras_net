"""
A used cars model.
Places two groups of agents in the enviornment randomly
and moves them around randomly.
"""

from indra.utils import get_props
from indra.agent import Agent
from indra.composite import Composite
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.env import Env
from indra.display_methods import RED, BLUE

MODEL_NAME = "used cars"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_BLUE = 10
DEF_NUM_RED = 10

buyer_group = None
seller_group = None
env = None


def seller_action(agent):
    print("I'm " + agent.name + " and I'm selling.")
    # return False means to move
    return False


def buyer_action(agent):
    print("I'm " + agent.name + " and I'm buying.")
    # return False means to move
    return False


def create_seller(name, i, props=None):
    """
    Create an agent.
    """
    return Agent(name + str(i), action=seller_action)


def create_buyer(name, i, props=None):
    """
    Create an agent.
    """
    return Agent(name + str(i), action=buyer_action)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    pa = get_props(MODEL_NAME, props)
    seller_group = Composite("Sellers", {"color": BLUE},
                             member_creator=create_seller,
                             num_members=pa.get('num_sellers', DEF_NUM_BLUE))
    buyer_group = Composite("Buyers", {"color": RED},
                            member_creator=create_buyer,
                            num_members=pa.get('num_buyers', DEF_NUM_RED))

    env = Env("env",
              height=pa.get('grid_height', DEF_HEIGHT),
              width=pa.get('grid_width', DEF_WIDTH),
              members=[seller_group, buyer_group],
              props=pa)

    return (env, seller_group, buyer_group)


def main():
    global buyer_group
    global seller_group
    global env

    (env, seller_group, buyer_group) = set_up()

    if DEBUG2:
        print(env.__repr__())

    env()
    return 0


if __name__ == "__main__":
    main()
