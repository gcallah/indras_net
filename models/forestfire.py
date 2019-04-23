"""
    This is the fashion model re-written in indra.
"""

# import math
import random
# from operator import gt, lt

from indra.agent import Agent
# from indra.agent import ratio_to_sin
from indra.composite import Composite
# from indra.space import in_hood
from indra.env import Env
# import numpy as np
from indra.display_methods import RED, GREEN, BLACK, CYAN

DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

FOREST_WIDTH = 10
FOREST_HEIGHT = 10
DENSITY = .40

TREE_PREFIX = "Tree"

# tree condition strings
HEALTHY = "Healthy"
ON_FIRE = "On Fire"
BURNED_OUT = "Burned Out"
NEW_GROWTH = "New Growth"

opp_group = None
# states numbers
HE = 0
OF = 1
BO = 2
NG = 3

NUM_STATES = 4

STATE_MAP = {HE: HEALTHY, OF: ON_FIRE, BO: BURNED_OUT, NG: NEW_GROWTH}

STATE_TRANS = [
    [.98, .02, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, .96, .04],
    [1.0, 0.0, 0.0, 0.0],
]


group_map = {HE: None, OF: None, BO: None, NG: None}


def change_state(agent):
    new_state = (agent["state"] + 1) % NUM_STATES
    agent.locator.add_switch(agent, group_map[agent["state"]],
                             group_map[new_state])
    agent["state"] = new_state


def tree_action(agent):
    if random.random() > .5:
        change_state(agent)
    return True


def create_tree(i, state=HE):
    """
    Create a trendsetter: all RED to start.
    """
    return Agent(TREE_PREFIX + str(i),
                 action=tree_action,
                 attrs={"state": state})


def set_up():
    """
    A func to set up run that can also be used by test code.
    """
    healthy = Composite(HEALTHY, {"color": GREEN})
    on_fire = Composite(ON_FIRE, {"color": RED})
    burned_out = Composite(BURNED_OUT, {"color": BLACK})
    new_growth = Composite(NEW_GROWTH, {"color": CYAN})
    for i in range(int(FOREST_HEIGHT * FOREST_WIDTH * DENSITY)):
        healthy += create_tree(i)

    forest = Env("Forest", members=[healthy, on_fire, burned_out, new_growth])
    global group_map
    group_map = {HE: healthy, OF: on_fire, BO: burned_out, NG: new_growth}
    return (forest, group_map)


def main():
    (forest, group_map) = set_up()

    if DEBUG2:
        print(forest.__repr__())

    forest()
    return 0


if __name__ == "__main__":
    main()
