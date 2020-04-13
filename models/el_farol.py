"""
El Farol Bar Problem
What happens when patrons want to go to the bar up to
60% occupancy, but don't beyond that point.
Yogi Berra: "That place is so popular, no one goes there
any more."
"""

import random

from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import BLUE, RED
from indra.env import Env
from registry.registry import get_env, get_group, get_prop
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.user import user_tell, run_notice
from indra.utils import init_props

DEBUG = False

MODEL_NAME = "el_farol"
DRINKERS = "At bar"
NON_DRINKERS = "At home"

DEF_POPULATION = 10
DEF_OPTIMAL_OCCUPANCY = int(0.6 * DEF_POPULATION)
MOTIVATION = [0.6] * DEF_POPULATION
NUM_DRINKERS = DEF_POPULATION // 2
NUM_NON_DRINKERS = DEF_POPULATION - NUM_DRINKERS

population = 0
optimal_occupancy = 0
attendance_record = []
attendance = 0
agents_decided = 0


def get_decision(agent):
    """
    Makes a decision randomly for the agent whether or not to go to the bar
    """
    random_num = random.random()
    if random_num <= agent["motivation"]:
        return True

    return False


def discourage(unwanted):
    """
    Discourages extra drinkers from going to the bar by decreasing motivation.
    Chooses drinkers randomly from the drinkers that went to the bar.
    """
    discouraged = 0
    drinkers = get_group(DRINKERS)
    while unwanted:
        if DEBUG:
            user_tell("The members are: " + drinkers.members)
        random_drunk = random.choice(list(drinkers.members))

        if DEBUG:
            user_tell("drinker ", random_drunk, " = "
                      + repr(drinkers[random_drunk]))

        drinkers[random_drunk]["motivation"] -= 0.05
        discouraged += 1
        unwanted -= 1

    return discouraged


def get_avg_attend(record):
    return sum(record) / len(record)


def drinker_action(agent):
    global attendance
    global attendance_record
    global agents_decided

    drinkers = get_group(DRINKERS)
    non_drinkers = get_group(NON_DRINKERS)

    changed = True
    decision = get_decision(agent)
    agents_decided += 1

    if agents_decided == population:
        attendance_record.append(attendance)
        if attendance > optimal_occupancy:
            extras = attendance - optimal_occupancy
            discourage(extras)

        agents_decided = 0
        attendance = 0
        user_tell("Avg attendance so far: "
                  + str(get_avg_attend(attendance_record)))

    if decision:
        attendance += 1
        if agent.primary_group() == non_drinkers:
            changed = False
            get_env().add_switch(agent, non_drinkers,
                                 drinkers)

    else:
        if agent.primary_group() == drinkers:
            changed = False
            get_env().add_switch(agent, drinkers,
                                 non_drinkers)

    # return False means to move
    return changed


def create_drinker(name, i, props=None):
    """
    Create an agent.
    """
    return Agent(name + str(i), action=drinker_action,
                 attrs={"motivation": 0.6})


def create_non_drinker(name, i, props=None):
    """
    Create an agent.
    """
    return Agent(name + str(i), action=drinker_action,
                 attrs={"motivation": 0.6})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    global population
    global optimal_occupancy
    global agents_decided

    init_props(MODEL_NAME, props)
    agents_decided = 0

    drinkers = Composite(DRINKERS, {"color": RED},
                         member_creator=create_drinker,
                         num_members=get_prop('population',
                                              DEF_POPULATION) // 2)

    non_drinkers = Composite(NON_DRINKERS, {"color": BLUE},
                             member_creator=create_non_drinker,
                             num_members=get_prop('population',
                                                  DEF_POPULATION) // 2)

    population = len(drinkers) + len(non_drinkers)
    optimal_occupancy = int(population * 0.6)

    Env("bar",
        height=get_prop('grid_height', DEF_HEIGHT),
        width=get_prop('grid_width', DEF_WIDTH),
        members=[drinkers, non_drinkers])


def main():
    set_up()
    run_notice(MODEL_NAME)
    get_env()()
    return 0


if __name__ == "__main__":
    main()
