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
from registry.execution_registry import CLI_EXEC_KEY, \
    EXEC_KEY, get_exec_key
from registry.registry import get_env, get_group, get_prop, set_env_attr, \
    get_env_attr
from registry.registry import user_tell, run_notice, user_log_notif
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.utils import init_props

DEBUG = False

MODEL_NAME = "el_farol"
DRINKERS = "At bar"
NON_DRINKERS = "At home"
BAR_ATTEND = "Bar attendees"
POPULATION = "population"
ATTENDANCE = "attendance"
AGENTS_DECIDED = "agents_decided"
OPT_OCCUPANCY = "opt_occupancy"
MOTIV = "motivation"

DEF_POPULATION = 10
DEF_MOTIV = 0.6
DISC_AMT = .01
MIN_MOTIV = 0.05
DEF_OPTIMAL_OCCUPANCY = int(DEF_MOTIV * DEF_POPULATION)
NUM_DRINKERS = DEF_POPULATION // 2
NUM_NON_DRINKERS = DEF_POPULATION - NUM_DRINKERS


def get_decision(agent):
    """
    Makes a decision for the agent whether or not to go to the bar
    """
    return random.random() <= agent[MOTIV]


def discourage(unwanted, **kwargs):
    """
    Discourages extra drinkers from going to the bar by decreasing motivation.
    Chooses drinkers randomly from the drinkers that went to the bar.
    """
    execution_key = get_exec_key(kwargs=kwargs)
    discouraged = 0
    drinkers = get_group(DRINKERS, execution_key=execution_key)
    while unwanted:
        if DEBUG:
            user_tell("The members are: " + drinkers.members)
        rand_name = random.choice(list(drinkers.members))
        rand_agent = drinkers[rand_name]

        if DEBUG:
            user_tell("drinker ", rand_agent, " = "
                      + repr(drinkers[rand_agent]))

        rand_agent[MOTIV] = max(rand_agent[MOTIV] - DISC_AMT,
                                MIN_MOTIV)
        discouraged += 1
        unwanted -= 1
    return discouraged


def drinker_action(agent, **kwargs):
    execution_key = get_exec_key(kwargs=kwargs)

    drinkers = get_group(DRINKERS, execution_key=execution_key)
    non_drinkers = get_group(NON_DRINKERS, execution_key=execution_key)

    changed = True
    decision = get_decision(agent)
    bar = get_env(execution_key=execution_key)
    bar.attrs[AGENTS_DECIDED] += 1
    attendance = get_env_attr(key=ATTENDANCE, execution_key=execution_key,
                              default_value=0)
    opt_occupancy = get_env_attr(OPT_OCCUPANCY, execution_key=execution_key)
    agents_decided = get_env_attr(AGENTS_DECIDED, execution_key=execution_key)
    if agents_decided == get_env_attr(POPULATION, execution_key=execution_key,
                                      default_value=0):
        if attendance > opt_occupancy:
            extras = attendance - opt_occupancy
            discourage(extras, **kwargs)
        set_env_attr(AGENTS_DECIDED, 0, execution_key=execution_key)
        set_env_attr(ATTENDANCE, 0, execution_key=execution_key)

    if decision:
        set_env_attr(ATTENDANCE, attendance + 1, execution_key=execution_key)
        if agent.primary_group() == non_drinkers:
            changed = False
            get_env(execution_key=execution_key).add_switch(agent,
                                                            non_drinkers,
                                                            drinkers)
    else:
        if agent.primary_group() == drinkers:
            changed = False
            get_env(execution_key=execution_key).add_switch(agent, drinkers,
                                                            non_drinkers)

    # return False means to move
    return changed


def create_drinker(name, i, **kwargs):
    """
    Create an agent.
    """
    execution_key = get_exec_key(kwargs=kwargs)
    return Agent(name + str(i), action=drinker_action,
                 attrs={MOTIV: DEF_MOTIV}, execution_key=execution_key)


def create_non_drinker(name, i, **kwargs):
    """
    Create an agent.
    """
    execution_key = get_exec_key(kwargs=kwargs)
    return Agent(name + str(i), action=drinker_action,
                 attrs={MOTIV: DEF_MOTIV}, execution_key=execution_key)


def setup_attendance(pop_hist):
    """
    Set up our pop hist object to record exchanges per period.
    """
    pop_hist.record_pop(BAR_ATTEND, 0)


def attendance(pop_hist, execution_key=CLI_EXEC_KEY):
    pop_hist.record_pop(BAR_ATTEND,
                        get_env(execution_key=execution_key).attrs[ATTENDANCE])


def attendance_report(env, execution_key=CLI_EXEC_KEY):
    return ("El Farol attendees on day "
            + str(env.get_periods())
            + ": " + str(env.attrs[ATTENDANCE]))


def set_env_attrs(execution_key=CLI_EXEC_KEY):
    user_log_notif("Setting env attrs for " + MODEL_NAME)
    set_env_attr("pop_hist_func", attendance, execution_key)
    set_env_attr("census_func", attendance_report, execution_key)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    init_props(MODEL_NAME, props)
    execution_key = int(props[EXEC_KEY].val) \
        if props is not None else CLI_EXEC_KEY

    population_prop = \
        get_prop('population', DEF_POPULATION, execution_key=execution_key)
    drinkers = Composite(DRINKERS, {"color": RED},
                         member_creator=create_drinker,
                         num_members=population_prop // 2,
                         execution_key=execution_key)

    non_drinkers = Composite(NON_DRINKERS, {"color": BLUE},
                             member_creator=create_non_drinker,
                             num_members=population_prop // 2,
                             execution_key=execution_key)
    Env(MODEL_NAME,
        height=get_prop('grid_height', DEF_HEIGHT,
                        execution_key=execution_key),
        width=get_prop('grid_width', DEF_WIDTH,
                       execution_key=execution_key),
        members=[drinkers, non_drinkers],
        pop_hist_setup=setup_attendance,
        execution_key=execution_key)

    population = len(drinkers) + len(non_drinkers)
    set_env_attr(POPULATION, population, execution_key=execution_key)
    set_env_attr(OPT_OCCUPANCY, int(population * DEF_MOTIV),
                 execution_key=execution_key)
    set_env_attr(AGENTS_DECIDED, 0, execution_key=execution_key)
    set_env_attr(ATTENDANCE, 0, execution_key=execution_key)
    set_env_attrs(execution_key=execution_key)


def main():
    set_up()
    run_notice(MODEL_NAME)
    get_env()()
    return 0


if __name__ == "__main__":
    main()
