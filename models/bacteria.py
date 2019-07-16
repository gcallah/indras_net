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

bacteria = None
toxins = None
petri_dish = None


def calc_strength(group, agent):
    """
    Calculate the strength of a toxin / nutrient field for an agent.
    """
    pass


def bacterium_action(agent, **kwargs):
    """
    Algorithm:
        1) sense env
            (toxin_level = calc_strength(toxins, agent))
        2) see if it is worse or better than previous env
        3) if worse, change direction
            (agent["angle"] = new_angle)
        4) move (done automatically by returning False)
    """
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
    toxin = Agent(name + str(i), action=toxin_action)
    toxin["max_move"] = 1
    return toxin


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

    toxins = Composite("Toxins", {"color": RED},
                       member_creator=create_toxin,
                       num_members=pa.get('num_toxins',
                                          DEF_NUM_TOXINS))
    bacteria = Composite("Bacteria", {"color": GREEN},
                         member_creator=create_bacterium,
                         num_members=pa.get('num_bacteria',
                                            DEF_NUM_BACT))

    petri_dish = Env("Petrie dish",
                     height=pa.get('grid_height', DEF_HEIGHT),
                     width=pa.get('grid_width', DEF_WIDTH),
                     members=[toxins, bacteria],
                     props=pa)
    return (petri_dish, toxins, bacteria)


def main():
    global bacteria
    global toxins
    global env

    (petri_dish, toxins, bacteria) = set_up()

    if DEBUG2:
        print(petri_dish.__repr__())

    petri_dish()
    return 0


if __name__ == "__main__":
    main()
