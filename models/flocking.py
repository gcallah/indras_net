"""
    This is the flocking model written in indra.
"""

from propargs.propargs import PropArgs
from indra.utils import get_prop_path
from indra.agent import Agent
from indra.composite import Composite
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.env import Env
from indra.display_methods import BLUE, TREE

MODEL_NAME = "flocking"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_BIRDS = 10

bird_group = None
env = None


def agent_action(agent):
    print("I'm " + agent.name + " and I'm acting.")
    # return False means to move

    return False
    # if agent.neighbors is None:
    #     bird_group.get_moore_hood(agent, save_neighbors=False)



def create_agent(color, i):
    """
    Create an agent.
    """
    return Agent(color + str(i), action=agent_action)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    ds_file = get_prop_path(MODEL_NAME)
    if props is None:
        pa = PropArgs.create_props(MODEL_NAME,
                                   ds_file=ds_file)
    else:
        pa = PropArgs.create_props(MODEL_NAME,
                                   prop_dict=props)

    bird_group = Composite("Birds", {"color": BLUE, "marker": TREE},
                           member_creator=create_agent,
                           num_members=pa.get('num_birds', DEF_NUM_BIRDS))

    env = Env("env",
              height=pa.get('grid_height', DEF_HEIGHT),
              width=pa.get('grid_width', DEF_WIDTH),
              members=[bird_group])
    return (bird_group, env)


def main():
    global bird_group
    global env

    (bird_group, env) = set_up()

    if DEBUG2:
        print(env.__repr__())

    env()
    return 0


if __name__ == "__main__":
    main()
