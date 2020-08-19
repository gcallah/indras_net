"""
Schelling's segregation model.
"""

import random

from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import RED, BLUE
from indra.env import Env
from registry.execution_registry import CLI_EXEC_KEY, \
    EXEC_KEY, get_exec_key
from registry.registry import get_env, get_prop
from registry.registry import run_notice
from indra.utils import init_props
from indra.space import neighbor_ratio

MODEL_NAME = "segregation"
DEBUG = False  # Turns debugging code on or off
DEBUG2 = False  # Turns deeper debugging code on or off

NUM_RED = 250
NUM_BLUE = 250

DEF_CITY_DIM = 40

TOLERANCE = "tolerance"
DEVIATION = "deviation"
GRP_INDEX = "grp_index"

DEF_HOOD_SIZE = 1
DEF_TOLERANCE = .5
DEF_SIGMA = .2

MIN_TOL = 0.1
MAX_TOL = 0.9

BLUE_GRP_IDX = 0
RED_GRP_IDX = 1

HOOD_SIZE = 4

NOT_ZERO = .001

BLUE_AGENTS = "Blue agents"
RED_AGENTS = "Red agents"

group_names = [BLUE_AGENTS, RED_AGENTS]

hood_size = None

opp_group = None


def get_tolerance(default_tolerance, sigma):
    """
    `tolerance` measures how *little* of one's own group one will
    tolerate being among.
    """
    tol = random.gauss(default_tolerance, sigma)
    # a low tolerance number here means high tolerance!
    tol = min(tol, MAX_TOL)
    tol = max(tol, MIN_TOL)
    return tol


def env_favorable(hood_ratio, my_tolerance):
    """
    Is the environment to our agent's liking or not??
    """
    return hood_ratio >= my_tolerance


def seg_agent_action(agent, **kwargs):
    """
    If the agent is surrounded by more "others" than it
    is comfortable with, the agent will move.
    The whole idea here is to count those in other group
    and those in my group, and get the ratio.
    """
    execution_key = get_exec_key(kwargs=kwargs)
    agent_group = agent.group_name()
    ratio_num = neighbor_ratio(agent,
                               lambda agent: agent.group_name() == agent_group,
                               size=agent['hood_size'],
                               execution_key=execution_key)
    if DEBUG2:
        print("ratio test" + str(ratio_num))
    return env_favorable(ratio_num, agent[TOLERANCE])


def create_resident(name, i, group=BLUE, **kwargs):
    """
    Creates agent of specified color type
    """
    execution_key = get_exec_key(kwargs=kwargs)
    if group == BLUE:
        grp_idx = BLUE_GRP_IDX
        mean_tol = get_prop('mean_tol', DEF_TOLERANCE,
                            execution_key=execution_key)
    else:
        grp_idx = RED_GRP_IDX
        mean_tol = -get_prop('mean_tol', DEF_TOLERANCE,
                             execution_key=execution_key)
    dev = get_prop('deviation', DEF_SIGMA, execution_key=execution_key)
    this_tolerance = get_tolerance(mean_tol,
                                   dev)
    return Agent(name + str(i),
                 action=seg_agent_action,
                 attrs={TOLERANCE: this_tolerance,
                        GRP_INDEX: grp_idx, "hood_changed": True,
                        "just_moved": False,
                        "hood_size": get_prop('hood_size',
                                              DEF_HOOD_SIZE,
                                              execution_key=execution_key)
                        }, execution_key=execution_key)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    init_props(MODEL_NAME, props)
    execution_key = int(props[EXEC_KEY].val) \
        if props is not None else CLI_EXEC_KEY
    blue_agents = Composite(group_names[BLUE_GRP_IDX],
                            {"color": BLUE},
                            member_creator=create_resident,
                            num_members=get_prop('num_blue',
                                                 NUM_BLUE,
                                                 execution_key=execution_key),
                            group=BLUE, execution_key=execution_key)
    red_agents = Composite(group_names[RED_GRP_IDX],
                           {"color": RED},
                           member_creator=create_resident,
                           num_members=get_prop('num_red', NUM_RED,
                                                execution_key=execution_key),
                           group=RED, execution_key=execution_key)
    city = Env(MODEL_NAME, members=[blue_agents, red_agents],
               height=get_prop('grid_height', DEF_CITY_DIM,
                               execution_key=execution_key),
               width=get_prop('grid_width', DEF_CITY_DIM,
                              execution_key=execution_key),
               execution_key=execution_key)
    city.exclude_menu_item("line_graph")


def main():
    set_up()
    run_notice(MODEL_NAME)
    # get_env() returns a callable object:
    get_env()()
    return 0


if __name__ == "__main__":
    main()
