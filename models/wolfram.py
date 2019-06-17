"""

"""

from propargs.propargs import PropArgs

from indra.agent import Agent
from indra.env import Env
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.composite import Composite
from indra.display_methods import RED, BLUE

X = 0
Y = 1

DEBUG = True  # Turns debugging code on or off
DEBUG2 = False  # Turns deeper debugging code on or off

# Default number of agents
DEF_NUM_RED = 10
DEF_NUM_BLUE = 10

# States
R = 1
B = 0

STATE_MAP = {R: RED, B: BLUE}

# Some dictionaries of rules:
RULE30 = {
    (R, R, R): B,
    (R, R, B): B,
    (R, B, R): B,
    (R, B, B): R,
    (B, R, R): R,
    (B, R, B): R,
    (B, B, R): R,
    (B, B, B): B
}

GRID_WIDTH = 30
GRID_HEIGHT = 30


def setup():
    red = Composite("red", {"color": RED})
    blue = Composite("blue", {"color": BLUE})
    wolframEnv = Env("wolframEnv", height=GRID_HEIGHT, width=GRID_WIDTH)
    return (red, blue, wolframEnv)


def agent_action(agent):
    print("I'm " + agent.name + " and I'm acting.")
    # Returning false means to move
    return False


def create_agent(color, i):
    """
    Create an agent.
    """
    return Agent(color + str(i), action=agent_action)


def set_up():
    """
    A func to set up run that can also be used by test code.
    """
    pa = PropArgs.create_props('basic_props',
                               ds_file='props/basic.props.json')
    blue_group = Composite("blues", {"color": BLUE},
                           member_creator=create_agent,
                           num_members=pa.get('num_blue', DEF_NUM_BLUE))
    red_group = Composite("reds", {"color": RED},
                          member_creator=create_agent,
                          num_members=pa.get('num_red', DEF_NUM_RED))

    env = Env("env",
              height=pa.get('grid_height', DEF_HEIGHT),
              width=pa.get('grid_width', DEF_WIDTH),
              members=[blue_group, red_group])
    return (blue_group, red_group, env)


def main():
    global blue_group
    global red_group
    global env
    # (red, blue, wolframEnv) = setup()
    (red, blue, env) = set_up()
    #  wolframEnv()
    env()
    return 0


if __name__ == "__main__":
    main()
