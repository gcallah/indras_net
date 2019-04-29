"""
    This is the fashion model re-written in indra.
"""

from indra.agent import prob_state_trans
from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env
from indra.space import in_hood
from indra.display_methods import RED, GREEN, BLACK, CYAN, YELLOW

DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

FOREST_WIDTH = 40
FOREST_HEIGHT = 40
DENSITY = .22

NEARBY = 1.8

TREE_PREFIX = "Tree"

# tree condition strings
HEALTHY = "Healthy"
NEW_FIRE = "New Fire"
ON_FIRE = "On Fire"
BURNED_OUT = "Burned Out"
NEW_GROWTH = "New Growth"

# states numbers
HE = 0
NF = 1
OF = 2
BO = 3
NG = 4

NUM_STATES = 5

STATE_MAP = {HE: HEALTHY, NF: NEW_FIRE,
             OF: ON_FIRE, BO: BURNED_OUT, NG: NEW_GROWTH}

STATE_TRANS = [
    [.98, .02, 0.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, .99, .01],
    [1.0, 0.0, 0.0, 0.0, 0.0],
]

on_fire = None

group_map = {HE: None, NF: None, OF: None, BO: None, NG: None}


def get_new_state(old_state):
    return (old_state + 1) % NUM_STATES


def is_healthy(agent, *args):
    return agent["state"] == HE


def tree_action(agent):
    """
    This is what trees do each turn in the forest.
    """
    global on_fire
    old_state = agent["state"]
    if is_healthy(agent):
        nearby_fires = on_fire.subset(in_hood, agent, NEARBY)
        if len(nearby_fires) > 0:
            if DEBUG:
                print("Setting nearby tree on fire!")
            agent["state"] = NF

    # if we didn't catch on fire above, do probabilistic transition:
    if old_state == agent["state"]:
        agent["state"] = prob_state_trans(old_state, STATE_TRANS)

    if old_state != agent["state"]:
        agent.locator.add_switch(agent, group_map[old_state],
                                 group_map[agent["state"]])
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
    global on_fire
    healthy = Composite(HEALTHY, {"color": GREEN})
    new_fire = Composite(NEW_FIRE, {"color": YELLOW})
    on_fire = Composite(ON_FIRE, {"color": RED})
    burned_out = Composite(BURNED_OUT, {"color": BLACK})
    new_growth = Composite(NEW_GROWTH, {"color": CYAN})
    for i in range(int(FOREST_HEIGHT * FOREST_WIDTH * DENSITY)):
        healthy += plant_tree(i)

    forest = Env("Forest", height=FOREST_HEIGHT, width=FOREST_WIDTH,
                 members=[healthy, new_fire, on_fire, burned_out, new_growth])
    global group_map
    group_map = {HE: healthy, NF: new_fire,
                 OF: on_fire, BO: burned_out, NG: new_growth}
    return (forest, group_map)


def main():
    (forest, group_map) = set_up()

    if DEBUG2:
        print(forest.__repr__())

    forest()
    return 0


if __name__ == "__main__":
    main()
