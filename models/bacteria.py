"""
This is the model that stimulate the behavior
of bacterias according to toxin and nutrients level.
"""

from indra.utils import get_props
from indra.agent import Agent
from indra.composite import Composite
from indra.space import DEF_HEIGHT, DEF_WIDTH, distance
from indra.env import Env
from indra.display_methods import RED, GREEN, YELLOW
from random import randint
import sys

MODEL_NAME = "bacteria"
DEBUG = False  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_BACT = 1
NUM_TOXINS = 1
DEF_NUM_NUTRIENTS = 1
DEF_THRESHOLD = -0.2
DEF_TOXIN_MOVE = 1
DEF_BACTERIUM_MOVE = 3
DEF_NUTRIENT_MOVE = 2

bacteria = None
toxins = None
nutrients = None
petri_dish = None


def calc_toxin(group, agent):
    """
    Calculate the strength of a toxin / nutrient field for an agent.
    """
    toxin_strength = 0
    for toxin in group:
        if distance(group[toxin], agent) != 0:
            toxin_strength += 1 / (distance(group[toxin], agent) ** 2)
        else:
            toxin_strength += sys.maxsize
    toxin_strength *= -1
    return toxin_strength


def calc_nutrient(group, agent):
    nutrient_strength = 0
    for nutrient in group:
        if distance(group[nutrient], agent) != 0:
            nutrient_strength += 1 / (distance(group[nutrient], agent) ** 2)
        else:
            nutrient_strength += sys.maxsize
    return nutrient_strength


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
    if DEBUG:
        print("I'm " + agent.name + " and I'm hungry.")

    toxin_level = calc_toxin(toxins, agent)
    nutrient_level = calc_nutrient(nutrients, agent)

    if agent["prev_toxicity"] is not None:
        toxin_change = calc_toxin(toxins, agent) - agent["prev_toxicity"]
    else:
        toxin_change = sys.maxsize * (-1)

    if agent["prev_nutricity"] is not None:
        nutrient_change = calc_nutrient(nutrients,
                                        agent) - agent["prev_nutricity"]
    else:
        nutrient_change = sys.maxsize * (-1)

    threshold = DEF_THRESHOLD
    agent["prev_toxicity"] = toxin_level
    agent["prev_nutricity"] = nutrient_level

    if (toxin_change > nutrient_change) or (threshold >= toxin_level):
        if agent["angle"] is None:
            new_angle = randint(0, 360)
        else:
            angle_shift = randint(45, 315)
            new_angle = agent["angle"] + angle_shift
        if (new_angle > 360):
            new_angle = new_angle % 360
        agent["angle"] = new_angle

    # return False means to move
    return False


def toxin_action(agent, **kwargs):
    if DEBUG:
        print("I'm " + agent.name + " and I'm poisonous.")
    # return False means to move
    return False


def nutrient_action(agent, **kwargs):
    if DEBUG:
        print("I'm " + agent.name + " and I'm nutrious.")
    # return False means to move
    return False


def create_bacterium(name, i, props=None):
    """
    Create a baterium.
    """
    bacterium = Agent(name + str(i), action=bacterium_action)
    bacterium["prev_toxicity"] = None
    bacterium["prev_nutricity"] = None
    bacterium["angle"] = None
    bacterium["max_move"] = props.get("bacterium_move", DEF_BACTERIUM_MOVE)
    return bacterium


def create_toxin(name, i, props=None):
    """
    Create a toxin.
    """
    toxin = Agent(name + str(i), action=toxin_action)
    toxin["max_move"] = props.get("toxin_move", DEF_TOXIN_MOVE)
    return toxin


def create_nutrient(name, i, props=None):
    """
    Create a nutrient.
    """
    nutrient = Agent(name + str(i), action=nutrient_action)
    nutrient["max_move"] = props.get("nutrient_move", DEF_NUTRIENT_MOVE)
    return nutrient


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    pa = get_props(MODEL_NAME, props)

    toxins = Composite("Toxins", {"color": RED}, props=pa,
                       member_creator=create_toxin,
                       num_members=pa.get('num_toxins', NUM_TOXINS))
    # for i in range(pa.get('num_toxins', NUM_TOXINS)):
    #     toxins += create_toxin("Toxins", i, pa)

    nutrients = Composite("Nutrients", {"color": YELLOW}, props=pa,
                          member_creator=create_nutrient,
                          num_members=pa.get('num_nutrients', NUM_TOXINS))

    bacteria = Composite("Bacteria", {"color": GREEN}, props=pa,
                         member_creator=create_bacterium,
                         num_members=pa.get('num_toxins',
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
    global nutrients
    global env

    (petri_dish, toxins, nutrients, bacteria) = set_up()

    if DEBUG2:
        print(petri_dish.__repr__())

    petri_dish()
    return 0


if __name__ == "__main__":
    main()
