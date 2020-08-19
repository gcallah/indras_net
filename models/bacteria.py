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
from registry.registry import get_env, get_group, get_prop
from registry.registry import user_tell, run_notice
from registry.execution_registry import \
    EXEC_KEY, CLI_EXEC_KEY, \
    get_exec_key
from indra.space import DEF_HEIGHT, DEF_WIDTH, distance
from indra.utils import init_props

MODEL_NAME = "bacteria"
DEBUG = False  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

BACTERIA = "Bacteria"
NUTRIENTS = "Nutrients"
TOXINS = "Toxins"

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
        user_tell("I'm " + agent.name + " and I'm hungry.")

    execution_key = CLI_EXEC_KEY
    if EXEC_KEY in kwargs:
        execution_key = kwargs[EXEC_KEY]

    toxin_level = calc_toxin(get_group(TOXINS, execution_key=execution_key),
                             agent)
    nutrient_level = calc_nutrient(
        get_group(NUTRIENTS, execution_key=execution_key), agent)
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
        user_tell("I'm " + agent.name + " and I'm poisonous.")
    # return False means to move
    return False


def nutrient_action(agent, **kwargs):
    if DEBUG:
        user_tell("I'm " + agent.name + " and I'm nutrious.")
    # return False means to move
    return False


def create_bacterium(name, i, **kwargs):
    """
    Create a baterium.
    """
    execution_key = get_exec_key(kwargs=kwargs)
    bacterium = Agent(name + str(i), action=bacterium_action,
                      execution_key=execution_key)
    bacterium["prev_toxicity"] = None
    bacterium["prev_nutricity"] = None
    bacterium["angle"] = None
    bacterium["max_move"] = get_prop("bacterium_move",
                                     DEF_BACTERIUM_MOVE,
                                     execution_key=execution_key)
    return bacterium


def create_toxin(name, i, **kwargs):
    """
    Create a toxin.
    """
    execution_key = get_exec_key(kwargs=kwargs)
    toxin = Agent(name + str(i), action=toxin_action,
                  execution_key=execution_key)
    toxin["max_move"] = get_prop("toxin_move", DEF_TOXIN_MOVE,
                                 execution_key=execution_key)
    return toxin


def create_nutrient(name, i, **kwargs):
    """
    Create a nutrient.
    """
    execution_key = get_exec_key(kwargs=kwargs)
    nutrient = Agent(name + str(i), action=nutrient_action,
                     execution_key=execution_key)
    nutrient["max_move"] = get_prop("nutrient_move",
                                    DEF_NUTRIENT_MOVE,
                                    execution_key=execution_key)
    return nutrient


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    init_props(MODEL_NAME, props)
    execution_key = int(props[EXEC_KEY].val) \
        if props is not None else CLI_EXEC_KEY
    toxins = Composite(TOXINS, {"color": RED},
                       member_creator=create_toxin,
                       num_members=get_prop('num_toxins', NUM_TOXINS,
                                            execution_key=execution_key),
                       execution_key=execution_key)

    nutrients = Composite(NUTRIENTS, {"color": GREEN},
                          member_creator=create_nutrient,
                          num_members=get_prop('num_nutrients', NUM_TOXINS,
                                               execution_key=execution_key),
                          execution_key=execution_key)

    bacteria = Composite(BACTERIA, {"color": BLUE},
                         member_creator=create_bacterium,
                         num_members=get_prop('num_toxins',
                                              DEF_NUM_BACT,
                                              execution_key=execution_key),
                         execution_key=execution_key)

    Env(MODEL_NAME,
        height=get_prop('grid_height', DEF_HEIGHT,
                        execution_key=execution_key),
        width=get_prop('grid_width', DEF_WIDTH, execution_key=execution_key),
        members=[toxins, nutrients, bacteria], execution_key=execution_key)


def main():
    set_up()
    run_notice(MODEL_NAME)
    get_env()()
    return 0


if __name__ == "__main__":
    main()
