"""

"""

from propargs.propargs import PropArgs

from indra.agent import Agent, switch
from indra.env import Env
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.composite import Composite
from indra.display_methods import BLACK, WHITE, BLUE

X = 0
Y = 1

DEBUG = True  # Turns debugging code on or off
DEBUG2 = False  # Turns deeper debugging code on or off

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

GRID_WIDTH = 31
GRID_HEIGHT = 31

groups = []


def create_agent(name):
    """
    Create an agent with the passed in name
    """
    return Agent(str(name), action=agent_action)


def wolfram_action(env):
    if DEBUG:
        print("In wolfram_action")


def agent_action(agent):
    print("I'm " + agent.name + " and I'm acting.")
    # Returning false means to move
    return False


def get_neighbors(agent):
    wolfram_env.get_neighbors(agent)


def set_up():
    """
    A func to set up run that can also be used by test code.
    """
    pa = PropArgs.create_props('basic_props',
                               ds_file='props/basic.props.json')
    width = pa.get('grid_width', DEF_WIDTH)
    height = pa.get('grid_height', DEF_HEIGHT)
    black = Composite("black", {"color": BLACK})
    white = Composite("blue", {"color": BLUE})
    groups.append(white)
    groups.append(black)
    print("Height and width: ", height, width)
    for i in range(height * width):
        groups[0] += create_agent(i)
    wolfram_env = Env("wolfram env",
                      action=wolfram_action,
                      height=height,
                      width=width,
                      members=groups)
    wolfram_env.attrs["center_agent"] = wolfram_env.get_agent_at(height // 2,
                                                                 width - 1)
    switch(wolfram_env.attrs["center_agent"], white, black)
    return (groups, wolfram_env)


def main():
    global groups
    global wolfram_env
    (groups, wolfram_env) = set_up()
    wolfram_env()
    return 0


if __name__ == "__main__":
    main()
