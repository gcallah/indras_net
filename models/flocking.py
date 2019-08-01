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

flock = None
the_sky = None


def agent_action(agent):
    # print("I'm " + agent.name + " and I'm acting.")
    # # return False means to move
    # return False
    if agent.neighbors is None:
        neighbors = agent.locator.get_moore_hood(agent, save_neighbors=False)

    if neighbors is not None:
        print("Creating Birds in a group")
    return False


def create_agent(color, i):
    """
    Create an agent.
    """
    return Agent(color + str(i), action=agent_action)


# def closest_bird(dist, desired):

#     if dist > desired:

#     elif dist < desired:

#     else:
#         pass


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

    flock = Composite("Birds", {"color": BLUE, "marker": TREE},
                      member_creator=create_agent,
                      num_members=pa.get('num_flock', DEF_NUM_BIRDS))

    the_sky = Env("the_sky",
                  height=pa.get('grid_height', DEF_HEIGHT),
                  width=pa.get('grid_width', DEF_WIDTH),
                  members=[flock])
    return (the_sky, flock)


def main():
    global flock
    global the_sky

    (the_sky, flock) = set_up()
    the_sky()
    return 0


if __name__ == "__main__":
    main()
