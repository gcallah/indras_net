"""
    This is the fashion model re-written in indra.
"""

from propargs.propargs import PropArgs
from indra.utils import get_prop_path
from indra.agent import Agent
from indra.composite import Composite
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.env import Env
from indra.display_methods import RED, GREEN

MODEL_NAME = "bacteria"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_BACT = 1
DEF_NUM_TOXINS = 1

bact_group = None
toxin_group = None
env = None


def bacterium_action(agent, **kwargs):
    print("I'm " + agent.name + " and I'm hungry.")
    # return False means to move
    return False


def toxin_action(agent, **kwargs):
    print("I'm " + agent.name + " and I'm poisonous.")
    # return False means to move
    return False


def create_bacterium(name, i):
    """
    Create an agent.
    """
    return Agent(name + str(i), action=bacterium_action)


def create_toxin(name, i):
    """
    Create an agent.
    """
    return Agent(name + str(i), action=toxin_action)


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

    toxin_group = Composite("Toxins", {"color": RED},
                            member_creator=create_toxin,
                            num_members=pa.get('num_toxins',
                                               DEF_NUM_TOXINS))
    bact_group = Composite("Bacteria", {"color": GREEN},
                           member_creator=create_bacterium,
                           num_members=pa.get('num_bacteria',
                                              DEF_NUM_BACT))

    env = Env("env",
              height=pa.get('grid_height', DEF_HEIGHT),
              width=pa.get('grid_width', DEF_WIDTH),
              members=[toxin_group, bact_group],
              props=pa)
    return (env, toxin_group, bact_group)


def main():
    global bact_group
    global toxin_group
    global env

    (env, toxin_group, bact_group) = set_up()

    if DEBUG2:
        print(env.__repr__())

    env()
    return 0


if __name__ == "__main__":
    main()
