"""
    This is the fashion model re-written in indra.
"""

from indra.agent import prob_state_trans
from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env
# from indra.space import in_hood
from indra.display_methods import RED, GREEN, BLACK, CYAN

DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

FOREST_WIDTH = 100
FOREST_HEIGHT = 100
DENSITY = .44

TREE_PREFIX = "Tree"

# tree condition strings
HEALTHY = "Healthy"
ON_FIRE = "On Fire"
BURNED_OUT = "Burned Out"
NEW_GROWTH = "New Growth"

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


def get_new_state(old_state):
    return (old_state + 1) % NUM_STATES


def tree_action(agent):
    old_state = agent["state"]
    agent["state"] = prob_state_trans(old_state, STATE_TRANS)
    if old_state != agent["state"]:
        agent.locator.add_switch(agent, group_map[old_state],
                                 group_map[agent["state"]])
    return True


def isHealthy(agent):
    return True


def isOnfire(agent):
    return True


def plant_tree(i, state=HE):
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
        healthy += plant_tree(i)

    forest = Env("Forest", height=FOREST_HEIGHT, width=FOREST_WIDTH,
                 members=[healthy, on_fire, burned_out, new_growth])
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
