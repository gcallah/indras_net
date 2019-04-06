"""
    This is the fashion model re-written in indra.
"""

import math
from operator import gt, lt

from indra.agent import Agent, X_VEC, Y_VEC, NEUTRAL
from indra.agent import ratio_to_sin
from indra.composite import Composite
from indra.space import in_hood
from indra.env import Env
import numpy as np

DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

NUM_TSETTERS = 5
NUM_FOLLOWERS = 10
"""
Adding weighted average for having a sine curve 

"""
ENV_WEIGHT = 0.9
weightings = [1.0, ENV_WEIGHT]

COLOR_PREF = "color_pref"
DISPLAY_COLOR = "display_color"

BLUE = 0.0
RED = 1.0

# for future use as we move to vector representation:
BLUE_VEC = X_VEC
RED_VEC = Y_VEC

NOT_ZERO = .001

TOO_SMALL = .01
BIG_ENOUGH = .03

HOOD_SIZE = 4

FOLLOWER_PRENM = "follower"
TSETTER_PRENM = "tsetter"
RED_FOLLOWERS = "Red Followers"
BLUE_FOLLOWERS = "Blue Followers"
RED_TSETTERS = "Red Trendsetters"
BLUE_TSETTERS = "Blue Trendsetters"

red_tsetters = None
blue_tsetters = None
red_followers = None
blue_followers = None
society = None

opp_group = None


def change_color(agent, society, opp_group):
    if DEBUG:
        print("Agent " + str(agent) + " is changing colors from "
              + str(agent.primary_group()) + " to "
              + str(opp_group[str(agent.primary_group())]))
    society.add_switch(agent, agent.primary_group(),
                       opp_group[str(agent.primary_group())])


def new_color_pref(old_pref, env_color):
    me = math.asin(old_pref)
    env = math.asin(env_color)
    avg = np.average([me,env], weights=weightings)   # noqa: E231
    new_color = math.sin(avg)
    return new_color


def env_unfavorable(my_color, my_pref, op1, op2):
    # we're going to add a small value to NEUTRAL so we sit on fence
    # op1 and op2 should be greater than or less than comparisons
    if my_color == RED:
        return op1(my_pref, (NEUTRAL - TOO_SMALL))
    else:
        return op2(my_pref, (NEUTRAL + TOO_SMALL))


def follower_action(agent):
    changed = False
    num_red_ts = max(len(red_tsetters.subset(in_hood, agent, HOOD_SIZE)),
                     NOT_ZERO)   # prevent div by zero!
    num_blue_ts = max(len(blue_tsetters.subset(in_hood, agent, HOOD_SIZE)),
                      NOT_ZERO)   # prevent div by zero!
    total_ts = num_red_ts + num_blue_ts
    if total_ts <= 0:
        return False

    env_color = ratio_to_sin(num_red_ts / total_ts)

    agent[COLOR_PREF] = new_color_pref(agent[COLOR_PREF], env_color)
    if env_unfavorable(agent[DISPLAY_COLOR], agent[COLOR_PREF], lt, gt):
        changed = True
        agent[DISPLAY_COLOR] = not agent[DISPLAY_COLOR]
        change_color(agent, society, opp_group)
    return changed


def tsetter_action(agent):
    changed = False
    num_red_fs = max(len(red_followers.subset(in_hood, agent, HOOD_SIZE)),
                     NOT_ZERO)   # prevent div by zero!
    num_blue_fs = max(len(blue_followers.subset(in_hood, agent, HOOD_SIZE)),
                      NOT_ZERO)   # prevent div by zero!
    total_fs = num_red_fs + num_blue_fs
    if total_fs <= 0:
        return False

    env_color = ratio_to_sin(num_red_fs / total_fs)

    agent[COLOR_PREF] = new_color_pref(agent[COLOR_PREF], env_color)
    if env_unfavorable(agent[DISPLAY_COLOR], agent[COLOR_PREF], gt, lt):
        changed = True
        agent[DISPLAY_COLOR] = not agent[DISPLAY_COLOR]
        change_color(agent, society, opp_group)
    return changed


def create_tsetter(i, color=RED):
    """
    Create a trendsetter: all RED to start.
    """
    return Agent(TSETTER_PRENM + str(i),
                 action=tsetter_action,
                 attrs={COLOR_PREF: color,
                        DISPLAY_COLOR: color})


def create_follower(i, color=BLUE):
    """
    Create a follower: all BLUE to start.
    """
    return Agent(FOLLOWER_PRENM + str(i),
                 action=follower_action,
                 attrs={COLOR_PREF: color,
                        DISPLAY_COLOR: color})


def set_up():
    """
    A func to set up run that can also be used by test code.
    """
    blue_tsetters = Composite(BLUE_TSETTERS)
    red_tsetters = Composite(RED_TSETTERS)
    for i in range(NUM_TSETTERS):
        red_tsetters += create_tsetter(i)

    if DEBUG2:
        print(red_tsetters.__repr__())

    red_followers = Composite(RED_FOLLOWERS)
    blue_followers = Composite(BLUE_FOLLOWERS)
    for i in range(NUM_FOLLOWERS):
        blue_followers += create_follower(i)

    opp_group = {str(red_tsetters): blue_tsetters,
                 str(blue_tsetters): red_tsetters,
                 str(red_followers): blue_followers,
                 str(blue_followers): red_followers}

    if DEBUG2:
        print(blue_followers.__repr__())

    society = Env("society", members=[blue_tsetters, red_tsetters,
                                      blue_followers, red_followers])
    return (blue_tsetters, red_tsetters, blue_followers, red_followers,
            opp_group, society)


def main():
    global red_tsetters
    global blue_tsetters
    global red_followers
    global blue_followers
    global society
    global opp_group

    (blue_tsetters, red_tsetters, blue_followers, red_followers, opp_group,
     society) = set_up()

    if DEBUG2:
        print(society.__repr__())

    society()
    return 0


if __name__ == "__main__":
    main()
