"""

"""

from propargs.propargs import PropArgs

from indra.agent import Agent
from indra.env import Env
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.composite import Composite
from indra.display_methods import BLACK, WHITE

X = 0
Y = 1

DEBUG = True  # Turns debugging code on or off
DEBUG2 = False  # Turns deeper debugging code on or off

# Default number of agents
DEF_NUM_WHITE = 10
DEF_NUM_BLACK = 10

# States
B = 1
W = 0

STATE_MAP = {B: BLACK, W: WHITE}

# Some dictionaries of rules:
RULE30 = {
    (B, B, B): W,
    (B, B, W): W,
    (B, W, B): W,
    (B, W, W): B,
    (W, B, B): B,
    (W, B, W): B,
    (W, W, B): B,
    (W, W, W): W
}

GRID_WIDTH = 30
GRID_HEIGHT = 30


def setup():
    black = Composite("black", {"color": BLACK})
    white = Composite("white", {"color": WHITE})
    wolframEnv = Env("wolframEnv", height=GRID_HEIGHT, width=GRID_WIDTH)
    return (white, black, wolframEnv)


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
    black_group = Composite("blacks", {"color": BLACK},
                            member_creator=create_agent,
                            num_members=pa.get('num_black', DEF_NUM_BLACK))
    white_group = Composite("whites", {"color": WHITE},
                            member_creator=create_agent,
                            num_members=pa.get('num_white', DEF_NUM_WHITE))
    env = Env("env",
              height=pa.get('grid_height', DEF_HEIGHT),
              width=pa.get('grid_width', DEF_WIDTH),
              members=[black_group, white_group])
    return (black_group, white_group, env)


def main():
    global black_group
    global white_group
    global env
    # (white, black, wolframEnv) = setup()
    (white, black, env) = set_up()
    #  wolframEnv()
    env()
    return 0


if __name__ == "__main__":
    main()
