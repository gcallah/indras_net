"""
    This is the fashion model re-written in indra.
"""

from propargs.propargs import PropArgs
from indra.utils import get_prop_path
from indra.agent import Agent
from indra.composite import Composite
from indra.space import DEF_HEIGHT, DEF_WIDTH, distance
from indra.env import Env
from indra.display_methods import RED, GREEN, YELLOW
from random import randint

MODEL_NAME = "bacteria"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_BACT = 1
DEF_NUM_TOXINS = 1
DEF_NUM_NUTRIENTS = 1
DEF_THRESHOLD = 0.2

bacteria = None
toxins = None
nutrients = None
petri_dish = None


def calc_toxin(group, agent):
    """
    Calculate the strength of a toxin / nutrient field for an agent.
    """
    print("This is group: ", group.members["Toxins0"])
    toxin_strength = 1 / float(distance(group["Toxins0"], agent))
    print("This is toxin strength: ", toxin_strength)
    return toxin_strength


def calc_nutrient(group, agent):
    nutrient_strength = 1 / float(distance(group["Nutrients0"], agent))
    print("This is nutrient strength: ", nutrient_strength)
    return nutrient_strength


def change_direction(toxins, nutrients, agent):
    toxin_level = calc_toxin(toxins, agent)
    nutrient_level = calc_nutrient(nutrients, agent)
    threshold = DEF_THRESHOLD
    if (toxin_level > threshold or toxin_level > nutrient_level):
        agent["prev_toxicity"] = toxin_level
        agent["prev_nutricity"] = nutrient_level
        return True
    return False


def bacterium_action(agent, **kwargs):
    """
    Algorithm:
        1) sense env
            (toxin_level = calc_toxin(toxins, agent))
        2) see if it is worse or better than previous env
        3) if worse, change direction
            (agent["angle"] = new_angle)
        4) move (done automatically by returning False)
    """
    print("I'm " + agent.name + " and I'm hungry.")
    if agent["prev_toxicity"] is None or change_direction(toxins,
                                                          nutrients, agent):
        new_angle = randint(0, 360)
        print("This is angle: ", new_angle)
        agent["angle"] = new_angle
        print("Get to the bottom of the if: ", agent["prev_toxicity"])
    # return False means to move
    return False


def toxin_action(agent, **kwargs):
    print("I'm " + agent.name + " and I'm poisonous.")
    # return False means to move
    return False


def nutrient_action(agent, **kwargs):
    print("I'm" + agent.name + "and I'm nutrious.")
    # return False means to move
    return False


def create_bacterium(name, i):
    """
    Create a baterium.
    """
    bacterium = Agent(name + str(i), action=bacterium_action)
    bacterium["prev_toxicity"] = None
    bacterium["prev_nutricity"] = None
    bacterium["max_move"] = 4
    return bacterium


def create_toxin(name, i):
    """
    Create a toxin.
    """
    toxin = Agent(name + str(i), action=toxin_action)
    toxin["max_move"] = 1
    return toxin


def create_nutrient(name, i):
    """
    Create a nutrient.
    """
    nutrient = Agent(name + str(i), action=nutrient_action)
    nutrient["max_move"] = 3
    return nutrient


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
    nutrients = Composite("Nutrients", {"color": YELLOW},
                          member_creator=create_nutrient,
                          num_members=pa.get('num_nutrients',
                                             DEF_NUM_NUTRIENTS))
    bacteria = Composite("Bacteria", {"color": GREEN},
                         member_creator=create_bacterium,
                         num_members=pa.get('num_bacteria',
                                            DEF_NUM_BACT))

    petri_dish = Env("Petrie dish",
                     height=pa.get('grid_height', DEF_HEIGHT),
                     width=pa.get('grid_width', DEF_WIDTH),
                     members=[toxins, nutrients, bacteria],
                     props=pa)
    return (petri_dish, toxins, nutrients, bacteria)


def main():
    global bacteria
    global toxins
    global env

    (petri_dish, toxins, nutrients, bacteria) = set_up()

    if DEBUG2:
        print(petri_dish.__repr__())

    petri_dish()
    return 0


if __name__ == "__main__":
    main()
