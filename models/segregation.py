"""
    This is the segregation model re-written in indra.
    It is starting life as a clone of the fashion model.
"""

import math
import statistics as sts
from operator import gt, lt

from indra.agent import Agent
from indra.composite import Composite
from indra.space import in_hood
from indra.env import Env

DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

NUM_AGENT = 5

TOLERANCE = "tolerance"
COLOR = "color"

DEF_TOLERANCE = .5

BLUE = 0
RED = 1

HOOD_SIZE = 4

NOT_ZERO = .001

group_names = ["Red Agent", "Blue Agent"]


reds = None
blues = None
city = None

opp_group = None


def env_unfavorable(my_hood, my_tolerance):
    """
    Is the environment to our agent's liking or not??
    """
    return True


def agent_action(agent):
    changed = False
    num_red = max(len(red_agents.subset(in_hood, agent, HOOD_SIZE)),
                     NOT_ZERO)   # prevent div by zero!

    num_blue = max(len(blue_agents.subset(in_hood, agent, HOOD_SIZE)),
                      NOT_ZERO)   # prevent div by zero!
    total_neighbors = num_red + num_blue
    if total_neighbors <= 0:
        return False

    hood_ratio = 1  # calculate based on others / total

    if DEBUG:
        print("Something about action")

    return not env_unfavorable(agent[TOLERANCE], hood_ratio)


def create_agent(i, color):
    """
    Creates agent of specified color type
    """
    return Agent(group_names[color] + str(i),
                 action=agent_action,
                 attrs={TOLERANCE: DEF_TOLERANCE,
                        COLOR: color})

def set_up():
    """
    A func to set up run that can also be used by test code.
    """
    blue_agents = Composite(group_names[BLUE] + " group")
    red_agents = Composite(group_names[RED] + " group")
    for i in range(NUM_AGENT):
        red_agents += create_agent(i, color=RED)

    if DEBUG2:
        print(red_agents.__repr__())

    for i in range(NUM_AGENT):
        blue_agents += create_agent(i, color=BLUE)

    if DEBUG2:
        print(blue_agents.__repr__())

    city = Env("A city", members=[blue_agents, red_agents])
    return (blue_agents, red_agents, city)


def main():

    global blue_agents
    global red_agents
    global city
    (blue_agents, red_agents, city) = set_up()

    if DEBUG2:
        print(city.__repr__())

    city()
    return 0


if __name__ == "__main__":
    main()
