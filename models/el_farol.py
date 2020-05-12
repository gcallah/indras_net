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
from indra.user import user_tell, run_notice, user_log_notif
from indra.utils import init_props

DEBUG = False

MODEL_NAME = "el_farol"
DRINKERS = "At bar"
NON_DRINKERS = "At home"
BAR_ATTEND = "Bar attendees"
ATTENDANCE = "attendance"
AGENTS_DECIDED = "agents_decided"
OPT_OCCUPANCY = "opt_occupancy"

DEF_POPULATION = 10
DEF_OPTIMAL_OCCUPANCY = int(0.6 * DEF_POPULATION)
MOTIVATION = [0.6] * DEF_POPULATION
NUM_DRINKERS = DEF_POPULATION // 2
NUM_NON_DRINKERS = DEF_POPULATION - NUM_DRINKERS


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


def drinker_action(agent):
    drinkers = get_group(DRINKERS)
    non_drinkers = get_group(NON_DRINKERS)

    changed = True
    decision = get_decision(agent)
    bar = get_env()
    bar.attrs[AGENTS_DECIDED] += 1

    attendance = bar.get_attr(ATTENDANCE, 0)
    opt_occupancy = bar.get_attr(OPT_OCCUPANCY)
    agents_decided = bar.get_attr(AGENTS_DECIDED)
    if agents_decided == bar.get_attr("population", 0):
        if attendance > opt_occupancy:
            extras = attendance - opt_occupancy
            discourage(extras)
        bar.set_attr(AGENTS_DECIDED, 0)
        bar.set_attr(ATTENDANCE, 0)

    if decision:
        bar.set_attr(ATTENDANCE, attendance + 1)
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


def setup_attendance(pop_hist):
    """
    Set up our pop hist object to record exchanges per period.
    """
    pop_hist.record_pop(BAR_ATTEND, 0)


def attendance(pop_hist):
    pop_hist.record_pop(BAR_ATTEND,
                        get_env().attrs[ATTENDANCE])


def attendance_report(env):
    return("Attendance this period: "
           + env.attrs[ATTENDANCE])


def set_env_attrs():
    user_log_notif("Setting env attrs for " + MODEL_NAME)
    env = get_env()
    env.set_attr("pop_hist_func", attendance)
    env.set_attr("census_func", attendance_report)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    init_props(MODEL_NAME, props)

    drinkers = Composite(DRINKERS, {"color": RED},
                         member_creator=create_drinker,
                         num_members=get_prop('population',
                                              DEF_POPULATION) // 2)

    non_drinkers = Composite(NON_DRINKERS, {"color": BLUE},
                             member_creator=create_non_drinker,
                             num_members=get_prop('population',
                                                  DEF_POPULATION) // 2)
    bar = Env("el_farol",
              height=get_prop('grid_height', DEF_HEIGHT),
              width=get_prop('grid_width', DEF_WIDTH),
              members=[drinkers, non_drinkers],
              pop_hist_setup=setup_attendance)
    population = len(drinkers) + len(non_drinkers)
    bar.set_attr("population", population)
    bar.set_attr(OPT_OCCUPANCY, int(population * 0.6))
    bar.set_attr(AGENTS_DECIDED, 0)
    bar.set_attr(ATTENDANCE, 0)


def main():
    set_up()
    run_notice(MODEL_NAME)
    get_env()()
    return 0


if __name__ == "__main__":
    main()
