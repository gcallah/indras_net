"""
This is the Adam Smith fashion model.
"""

import math
from operator import gt, lt

import numpy as np

from indra.agent import Agent, X_VEC, Y_VEC, NEUTRAL
from indra.agent import ratio_to_sin
from indra.composite import Composite
from indra.display_methods import NAVY, DARKRED, RED, BLUE
from indra.env import Env
from registry.execution_registry import CLI_EXEC_KEY, \
    EXEC_KEY, get_exec_key
from registry.registry import get_env, get_group, get_prop
from registry.registry import run_notice, user_log_notif
from indra.space import in_hood
from indra.utils import init_props

MODEL_NAME = "fashion"
DEBUG = False  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

NUM_TSETTERS = 5
NUM_FOLLOWERS = 55

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

OPP_GROUP = "opp_group"

opp_group = {RED_TSETTERS: BLUE_TSETTERS,
             BLUE_TSETTERS: RED_TSETTERS,
             RED_FOLLOWERS: BLUE_FOLLOWERS,
             BLUE_FOLLOWERS: RED_FOLLOWERS}


def get_opp_group(grp):
    return get_group(get_env()[OPP_GROUP][grp])


def change_color(agent, society, opp_group):
    """
    change agent's DISPLAY_COLOR to its opposite color
    """
    if DEBUG2:
        user_log_notif("Agent " + agent.name + " is changing colors"
                       + "; its prim group is "
                       + agent.prim_group_nm())
    agent[DISPLAY_COLOR] = not agent[DISPLAY_COLOR]
    society.add_switch(agent, agent.prim_group_nm(),
                       opp_group[agent.prim_group_nm()])


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


def follower_action(agent, **kwargs):
    execution_key = get_exec_key(kwargs=kwargs)
    return common_action(agent,
                         get_group(RED_TSETTERS, execution_key=execution_key),
                         get_group(BLUE_TSETTERS, execution_key=execution_key),
                         lt, gt, **kwargs)


def tsetter_action(agent, **kwargs):
    execution_key = get_exec_key(kwargs=kwargs)
    return common_action(agent,
                         get_group(RED_FOLLOWERS, execution_key=execution_key),
                         get_group(BLUE_FOLLOWERS,
                                   execution_key=execution_key),
                         gt,
                         lt, **kwargs)


def common_action(agent, others_red, others_blue, op1, op2, **kwargs):
    """
    The actions for both followers and trendsetters
    """
    execution_key = get_exec_key(kwargs=kwargs)
    num_others_red = len(others_red.subset(in_hood, agent, HOOD_SIZE))
    num_others_blue = len(others_blue.subset(in_hood, agent, HOOD_SIZE))
    total_others = num_others_red + num_others_blue
    if total_others <= 0:
        return False

    env_color = ratio_to_sin(num_others_red / total_others)

    agent[COLOR_PREF] = new_color_pref(agent[COLOR_PREF], env_color)
    if env_unfavorable(agent[DISPLAY_COLOR], agent[COLOR_PREF], op1, op2):
        change_color(agent, get_env(execution_key=execution_key), opp_group)
        return True
    else:
        return False


def create_tsetter(name, i, props=None, color=RED_SIN, **kwargs):
    """
    Create a trendsetter: all RED to start.
    """
    execution_key = get_exec_key(kwargs=kwargs)
    return Agent(TSETTER_PRENM + str(i),
                 action=tsetter_action,
                 attrs={COLOR_PREF: color,
                        DISPLAY_COLOR: color}, execution_key=execution_key)


def create_follower(name, i, props=None, color=BLUE_SIN, **kwargs):
    """
    Create a follower: all BLUE to start.
    """
    execution_key = get_exec_key(kwargs=kwargs)
    return Agent(FOLLOWER_PRENM + str(i),
                 action=follower_action,
                 attrs={COLOR_PREF: color,
                        DISPLAY_COLOR: color}, execution_key=execution_key)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    init_props(MODEL_NAME, props)
    execution_key = int(props[EXEC_KEY].val) \
        if props is not None else CLI_EXEC_KEY
    groups = []

    groups.append(
        Composite(BLUE_TSETTERS, {"color": NAVY}, execution_key=execution_key))
    groups.append(Composite(RED_TSETTERS, {"color": DARKRED},
                            member_creator=create_tsetter,
                            num_members=get_prop('num_tsetters',
                                                 NUM_TSETTERS,
                                                 execution_key=execution_key),
                            execution_key=execution_key))

    groups.append(
        Composite(RED_FOLLOWERS, {"color": RED}, execution_key=execution_key))
    groups.append(Composite(BLUE_FOLLOWERS, {"color": BLUE},
                            member_creator=create_follower,
                            num_members=get_prop('num_followers',
                                                 NUM_FOLLOWERS,
                                                 execution_key=execution_key),
                            execution_key=execution_key))

    Env(MODEL_NAME, members=groups, attrs={OPP_GROUP: opp_group},
        execution_key=execution_key)


def main():
    set_up()

    run_notice(MODEL_NAME)
    # get_env() returns a callable object:
    get_env()()
    return 0


if __name__ == "__main__":
    main()
