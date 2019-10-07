"""
    This is the fashion model re-written in indra.
"""

import math
from operator import gt, lt

import numpy as np

from indra.agent import Agent, X_VEC, Y_VEC, NEUTRAL
from indra.agent import ratio_to_sin
from indra.composite import Composite
from indra.display_methods import NAVY, DARKRED, RED, BLUE
from indra.env import Env
from indra.space import in_hood
from indra.utils import get_props

MODEL_NAME = "fashion"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

NUM_TSETTERS = 5
NUM_FOLLOWERS = 55

"""
Adding weighted average for having a sine curve
"""
ENV_WEIGHT = 0.6
weightings = [1.0, ENV_WEIGHT]

COLOR_PREF = "color_pref"
DISPLAY_COLOR = "display_color"

BLUE_SIN = 0.0
RED_SIN = 1.0

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
    """
    change agent's DISPLAY_COLOR to its opposite color
    """
    agent[DISPLAY_COLOR] = not agent[DISPLAY_COLOR]
    society.add_switch(agent, agent.primary_group(),
                       opp_group[str(agent.primary_group())])


def new_color_pref(old_pref, env_color):
    """
    Calculate new color pref with the formula below:
    new_color = sin(avg(asin(old_pref) + asin(env_color)))
    """
    me = math.asin(old_pref)
    env = math.asin(env_color)
    avg = np.average([me, env], weights=weightings)
    new_color = math.sin(avg)
    return new_color


def env_unfavorable(my_color, my_pref, op1, op2):
    # we're going to add a small value to NEUTRAL so we sit on fence
    # op1 and op2 should be greater than or less than comparisons
    if my_color == RED_SIN:
        return op1(my_pref, (NEUTRAL - TOO_SMALL))
    else:
        return op2(my_pref, (NEUTRAL + TOO_SMALL))


def follower_action(agent):
    return common_action(agent, red_tsetters, blue_tsetters, lt, gt)


def tsetter_action(agent):
    return common_action(agent, red_followers, blue_followers, gt, lt)


def common_action(agent, others_red, others_blue, op1, op2):
    num_others_red = len(others_red.subset(in_hood, agent, HOOD_SIZE))
    num_others_blue = len(others_blue.subset(in_hood, agent, HOOD_SIZE))
    total_others = num_others_red + num_others_blue
    if total_others <= 0:
        return False

    env_color = ratio_to_sin(num_others_red / total_others)

    agent[COLOR_PREF] = new_color_pref(agent[COLOR_PREF], env_color)
    if env_unfavorable(agent[DISPLAY_COLOR], agent[COLOR_PREF], op1, op2):
        change_color(agent, society, opp_group)
        return True
    else:
        return False


def create_tsetter(name, i, props=None, color=RED_SIN):
    """
    Create a trendsetter: all RED_SIN to start.
    """
    name = TSETTER_PRENM
    return Agent(name + str(i),
                 action=tsetter_action,
                 attrs={COLOR_PREF: color,
                        DISPLAY_COLOR: color})


def create_follower(name, i, props=None, color=BLUE_SIN):
    """
    Create a follower: all BLUE_SIN to start.
    """
    name = FOLLOWER_PRENM
    return Agent(name + str(i),
                 action=follower_action,
                 attrs={COLOR_PREF: color,
                        DISPLAY_COLOR: color})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    global red_tsetters
    global blue_tsetters
    global red_followers
    global blue_followers
    global society
    global opp_group

    pa = get_props(MODEL_NAME, props)

    blue_tsetters = Composite(BLUE_TSETTERS, {"color": NAVY})
    red_tsetters = Composite(RED_TSETTERS, {"color": DARKRED},
                             member_creator=create_tsetter, props=pa,
                             num_members=pa.get('num_tsetters',
                                                NUM_TSETTERS))
    # for i in range():
    #     red_tsetters += create_tsetter(i)

    if DEBUG2:
        print(red_tsetters.__repr__())

    red_followers = Composite(RED_FOLLOWERS, {"color": RED})
    blue_followers = Composite(BLUE_FOLLOWERS, {"color": BLUE},
                               props=pa, member_creator=create_follower,
                               num_members=pa.get('num_followers',
                                                  NUM_FOLLOWERS))
    # for i in range():
    #     blue_followers += create_follower(i)

    opp_group = {str(red_tsetters): blue_tsetters,
                 str(blue_tsetters): red_tsetters,
                 str(red_followers): blue_followers,
                 str(blue_followers): red_followers}

    if DEBUG2:
        print(blue_followers.__repr__())

    society = Env("Society",
                  members=[blue_tsetters, red_tsetters,
                           blue_followers, red_followers],
                  props=pa)
    return (society, blue_tsetters, red_tsetters, blue_followers,
            red_followers, opp_group)


def fs_unrestorable(env):
    global red_tsetters
    global blue_tsetters
    global red_followers
    global blue_followers
    global society
    global opp_group
    society = env
    blue_tsetters = env.registry[BLUE_TSETTERS]
    red_tsetters = env.registry[RED_TSETTERS]
    red_followers = env.registry[RED_FOLLOWERS]
    blue_followers = env.registry[BLUE_FOLLOWERS]
    opp_group = {str(red_tsetters): blue_tsetters,
                 str(blue_tsetters): red_tsetters,
                 str(red_followers): blue_followers,
                 str(blue_followers): red_followers}


def main():
    global red_tsetters
    global blue_tsetters
    global red_followers
    global blue_followers
    global society
    global opp_group

    (society, blue_tsetters, red_tsetters, blue_followers, red_followers,
     opp_group) = set_up()

    if DEBUG2:
        print(society.__repr__())

    society()
    return 0


if __name__ == "__main__":
    main()
