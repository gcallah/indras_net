"""
Schelling's segregation model.
"""

import random
from indra.utils import get_props
from indra.agent import Agent
from indra.composite import Composite
# from indra.space import in_hood
from indra.env import Env
from indra.display_methods import RED, BLUE

MODEL_NAME = "segregation"
DEBUG = True  # Turns debugging code on or off
DEBUG2 = False  # Turns deeper debugging code on or off

NUM_RED = 250
NUM_BLUE = 250

DEF_CITY_DIM = 40

TOLERANCE = "tolerance"
DEVIATION = "deviation"
COLOR = "color"

DEF_HOOD_SIZE = 1
DEF_TOLERANCE = .5
DEF_SIGMA = .2

MAX_TOL = 0.1
MIN_TOL = 0.9

BLUE_TEAM = 0
RED_TEAM = 1

HOOD_SIZE = 4

NOT_ZERO = .001

group_names = ["Blue Agent", "Red Agent"]

group_suffix = "s"

reds = None
blues = None
city = None
hood_size = None

opp_group = None

red_agents = None
blue_agents = None

fetched_moore_hood = 0


def get_tolerance(default_tolerance, sigma):
    tol = random.gauss(default_tolerance, sigma)
    # a low tolerance number here means high tolerance!
    tol = max(tol, MAX_TOL)
    tol = min(tol, MIN_TOL)
    return tol


def my_group_index(agent):
    return int(agent[COLOR])


def other_group_index(agent):
    return not my_group_index(agent)


def env_favorable(hood_ratio, my_tolerance):
    """
    Is the environment to our agent's liking or not??
    """
    return hood_ratio >= my_tolerance


def seg_agent_action(agent):
    """
    If the agent is surrounded by more "others" than it is comfortable
    with, the agent will move.
    """
    global city
    global red_agents
    global blue_agents
    global fetched_moore_hood

    stay_put = True
    if agent["hood_changed"]:
        agent_group = agent.primary_group()
        ratio_same = 0
        neighbors = city.get_moore_hood(agent, hood_size=agent['hood_size'])
        if DEBUG2:
            print("hood size = ", agent['hood_size'])
        fetched_moore_hood += 1
        num_same = 0
        for neighbor in neighbors:
            if neighbors[neighbor].primary_group() == agent_group:
                num_same += 1
            if agent["just_moved"] is True:
                neighbors[neighbor]["hood_changed"] = True
        agent["just_moved"] = False
        if len(neighbors) != 0:
            ratio_same = num_same / len(neighbors)
        stay_put = env_favorable(ratio_same, agent[TOLERANCE])
        if stay_put:
            agent["hood_changed"] = False
        else:
            agent["just_moved"] = True
            for neighbor in neighbors:
                neighbors[neighbor]["hood_changed"] = True
    return stay_put


def create_agent(name, i, props=None):
    """
    Creates agent of specified color type
    """

    if "Blue" in name:
        color = 0
        mean_tol = props.get('mean_tol', DEF_TOLERANCE)
    else:
        color = 1
        mean_tol = -props.get('mean_tol', DEF_TOLERANCE)
    dev = props.get('deviation', DEF_SIGMA)
    this_tolerance = get_tolerance(mean_tol,
                                   dev)

    hood_size = props.get('hood_size', DEF_HOOD_SIZE)

    return Agent(name + str(i),
                 action=seg_agent_action,
                 attrs={TOLERANCE: this_tolerance,
                        COLOR: color, "hood_changed": True,
                        "just_moved": False,
                        "hood_size": hood_size
                        },)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    global blue_agents
    global red_agents
    global city
    global fetched_moore_hood

    pa = get_props(MODEL_NAME, props)
    blue_agents = Composite(group_names[BLUE_TEAM] + group_suffix,
                            {"color": BLUE},
                            props=pa, member_creator=create_agent,
                            num_members=pa.get('num_blue', NUM_BLUE))
    red_agents = Composite(group_names[RED_TEAM] + group_suffix,
                           {"color": RED},
                           props=pa, member_creator=create_agent,
                           num_members=pa.get('num_red', NUM_RED))
    if DEBUG2:
        print(red_agents.__repr__())
    if DEBUG2:
        print(blue_agents.__repr__())
    city = Env("A city", members=[blue_agents, red_agents],
               height=pa.get('grid_height', DEF_CITY_DIM),
               width=pa.get('grid_width', DEF_CITY_DIM),
               props=pa)
    city.exclude_menu_item("line_graph")
    return (city, blue_agents, red_agents)


def sg_unrestorable(env):
    """
    This handles are unrestorable from JSON data.
    """
    global blue_agents
    global red_agents
    global city
    global fetched_moore_hood
    city = env
    blue_agents = env.registry[group_names[BLUE_TEAM] + group_suffix]
    red_agents = env.registry[group_names[RED_TEAM] + group_suffix]


def main():
    global blue_agents
    global red_agents
    global city
    global fetched_moore_hood
    (city, blue_agents, red_agents) = set_up()

    if DEBUG2:
        print(city.__repr__())

    city()
    print("We fetched moore hoods ", fetched_moore_hood, " times")
    return 0


if __name__ == "__main__":
    main()
