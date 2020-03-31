"""
This is the model that stimulates the behavior
of bacterias according to toxin and nutrients level.
"""

import sys
from random import randint

from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import BLUE, GREEN, RED
from indra.env import Env
from indra.registry import get_env, get_group, get_prop
from indra.space import DEF_HEIGHT, DEF_WIDTH, distance
from indra.utils import init_props
from indra.user import user_log

MODEL_NAME = "bacteria"
DEBUG = False  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

TOXINS = "Toxins"
NUTRIENTS = "Nutrients"

DEF_NUM_BACT = 1
NUM_TOXINS = 1
DEF_NUM_NUTRIENTS = 1
DEF_THRESHOLD = -0.2
DEF_TOXIN_MOVE = 1
DEF_BACTERIUM_MOVE = 3
DEF_NUTRIENT_MOVE = 2


def calc_toxin(group, agent):
    """
    Calculate the strength of a toxin / nutrient field for an agent.
    We will use an inverse square law.
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

    toxin_level = calc_toxin(get_group(TOXINS), agent)
    nutrient_level = calc_nutrient(
        get_group(NUTRIENTS), agent)

    if agent["prev_toxicity"] is not None:
        toxin_change = toxin_level - agent["prev_toxicity"]
    else:
        toxin_change = sys.maxsize * (-1)

    if agent["prev_nutricity"] is not None:
        nutrient_change = nutrient_level - agent["prev_nutricity"]
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


def create_bacterium(name, i):
    """
    Create a baterium.
    """
    bacterium = Agent(name + str(i), action=bacterium_action)
    bacterium["prev_toxicity"] = None
    bacterium["prev_nutricity"] = None
    bacterium["angle"] = None
    bacterium["max_move"] = get_prop("bacterium_move",
                                     DEF_BACTERIUM_MOVE)
    return bacterium


def create_toxin(name, i):
    """
    Create a toxin.
    """
    toxin = Agent(name + str(i), action=toxin_action)
    toxin["max_move"] = get_prop("toxin_move", DEF_TOXIN_MOVE)
    return toxin


def create_nutrient(name, i):
    """
    Create a nutrient.
    """
    nutrient = Agent(name + str(i), action=nutrient_action)
    nutrient["max_move"] = get_prop("nutrient_move",
                                    DEF_NUTRIENT_MOVE)
    return nutrient


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    init_props(MODEL_NAME, props)

    toxins = Composite(TOXINS, {"color": RED},
                       member_creator=create_toxin,
                       num_members=get_prop('num_toxins', NUM_TOXINS))

    nutrients = Composite(NUTRIENTS, {"color": GREEN},
                          member_creator=create_nutrient,
                          num_members=get_prop('num_nutrients', NUM_TOXINS))

    bacteria = Composite("Bacteria", {"color": BLUE},
                         member_creator=create_bacterium,
                         num_members=get_prop('num_toxins',
                                              DEF_NUM_BACT))

    Env("Petrie dish",
        height=get_prop('grid_height', DEF_HEIGHT),
        width=get_prop('grid_width', DEF_WIDTH),
        members=[toxins, nutrients, bacteria])


def main():
    set_up()
    user_log("Setup complete for: " + MODEL_NAME + " model")
    get_env()()
    return 0


if __name__ == "__main__":
    main()
