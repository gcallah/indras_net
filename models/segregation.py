"""
    This is Schelling's segregation model re-written in indra V2.
"""
import random

from propargs.propargs import PropArgs
from indra.agent import Agent
from indra.composite import Composite
from indra.space import in_hood
from indra.env import Env
from indra.display_methods import RED, BLUE

DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

NUM_RED = 250
NUM_BLUE = 250

DEF_CITY_DIM = 40

TOLERANCE = "tolerance"
DEVIATION = "deviation"
COLOR = "color"

DEF_TOLERANCE = .5
DEF_SIGMA = .2

BLUE_TEAM = 0
RED_TEAM = 1

HOOD_SIZE = 4

NOT_ZERO = .001

group_names = ["Blue Agent", "Red Agent"]

reds = None
blues = None
city = None

opp_group = None

red_agents = None
blue_agents = None


def get_tolerance(default_tolerance, sigma):
    tol = random.gauss(default_tolerance, sigma)
    tol = max(tol, 0.0)
    tol = min(tol, 1.0)
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


def agent_action(agent):
    """
    If the agent is surrounded by more "others" than it is comfortable
    with, the agent will move.
    """
    num_red = max(len(red_agents.subset(in_hood, agent, HOOD_SIZE)),
                  NOT_ZERO)   # prevent div by zero!

    num_blue = max(len(blue_agents.subset(in_hood, agent, HOOD_SIZE)),
                   NOT_ZERO)   # prevent div by zero!
    total_neighbors = num_red + num_blue

    groups_count = [num_blue, num_red]

    if groups_count[other_group_index(agent)] <= 0:
        return False

    hood_ratio = groups_count[my_group_index(agent)] / total_neighbors
    return env_favorable(hood_ratio, agent[TOLERANCE])


def create_agent(i, mean_tol, dev, color):
    """
    Creates agent of specified color type
    """
    this_tolerance = get_tolerance(mean_tol,
                                   dev)
    return Agent(group_names[color] + str(i),
                 action=agent_action,
                 attrs={TOLERANCE: this_tolerance,
                        COLOR: color})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    if props is None:
        pa = PropArgs.create_props('fashion_props',
                                   ds_file='props/segregation.props.json')
    else:
        pa = PropArgs.create_props('fashion_props',
                                   prop_dict=props)

    blue_agents = Composite(group_names[BLUE_TEAM] + " group", {"color": BLUE})
    red_agents = Composite(group_names[RED_TEAM] + " group", {"color": RED})
    for i in range(pa.get('num_red', NUM_RED)):
        red_agents += create_agent(i,
                                   pa.get('mean_tol', DEF_TOLERANCE),
                                   pa.get('deviation', DEF_SIGMA),
                                   color=RED_TEAM)

    if DEBUG2:
        print(red_agents.__repr__())

    for i in range(pa.get('num_blue', NUM_BLUE)):
        blue_agents += create_agent(i,
                                    pa.get('mean_tol', DEF_TOLERANCE),
                                    pa.get('deviation', DEF_SIGMA),
                                    color=BLUE_TEAM)
    if DEBUG2:
        print(blue_agents.__repr__())

    city = Env("A city", members=[blue_agents, red_agents],
               height=pa.get('grid_height', DEF_CITY_DIM),
               width=pa.get('grid_width', DEF_CITY_DIM))
    return (city, blue_agents, red_agents)


def main():
    global blue_agents
    global red_agents
    global city
    (city, blue_agents, red_agents) = set_up()

    if DEBUG2:
        print(city.__repr__())

    city()
    return 0


if __name__ == "__main__":
    main()
