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

NUM_TSETTERS = 5
NUM_FOLLOWERS = 10

COLOR_PREF = "color_pref"
DISPLAY_COLOR = "display_color"

BLUE = 0.0
RED = 1.0

HOOD_SIZE = 4

FOLLOWER_PRENM = "follower"
TSETTER_PRENM = "tsetter"

RED_AGENT = "Red Agent"
BLUE_AGENT = "Blue Agent"

red_tsetters = None
blue_tsetters = None
red_followers = None
blue_followers = None
society = None

opp_group = None


def change_position(agent, society, opp_group):
    if DEBUG:
        print("Agent " + str(agent) + " is changing position from "
              + str(agent.primary_group()) + " to "
              + str(opp_group[str(agent.primary_group())]))


def env_unfavorable(my_hood, my_tolerance):
    """
    Is the environment to our agent's liking or not??
    """
    return False


def agent_action(agent):
    changed = False
    num_red = max(len(red_agents.subset(in_hood, agent, HOOD_SIZE)),
                     NOT_ZERO)   # prevent div by zero!
    num_blue = max(len(blue_agents.subset(in_hood, agent, HOOD_SIZE)),
                      NOT_ZERO)   # prevent div by zero!
    total_neighbors = num_red + num_blue
    if total_neighbors <= 0:
        return False

    ratio = 1  # calculate based on others / total

    print("in action new color = " + str(ncp))
    agent[COLOR_PREF] = ncp
    if DEBUG:
        print("In action, we get new pref = " + str(agent[COLOR_PREF])
              + " display color = " + str(agent[DISPLAY_COLOR])
              + " env color = " + str(env_color))
    if env_unfavorable(agent[TOLERANCE], hood_ratio):
        changed = True
        change_position(agent, society)
    return changed


def create_agent(i, color=RED):
    """
    Creates agent of specified color type
    """
    return Agent(TSETTER_PRENM + str(i),
                 action=tsetter_action,
                 attrs={COLOR_PREF: color,
                        DISPLAY_COLOR: color})


def set_up():
    """
    A func to set up run that can also be used by test code.
    """
    blue_agents = Composite(BLUE_AGENT)
    red_agents = Composite(RED_AGENT)
    for i in range(NUM_TSETTERS):
        red_agents += create_agent(i, color=RED)

    if DEBUG2:
        print(red_tsetters.__repr__())

    for i in range(NUM_FOLLOWERS):
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
