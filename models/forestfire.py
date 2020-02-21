"""
A model to simulate the spread of fire in a forest.
"""

from indra.agent import Agent
from indra.agent import prob_state_trans
from indra.composite import Composite
from indra.display_methods import RED, GREEN, BLACK
from indra.display_methods import SPRINGGREEN, TOMATO, TREE
from indra.env import Env
from indra.registry import get_env, get_prop
from indra.utils import init_props

MODEL_NAME = "forestfire"
DEBUG = False  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

NEARBY = 1.8

DEF_DIM = 30
DEF_DENSITY = .44

TREE_PREFIX = "Tree"

# tree condition strings
HEALTHY = "Healthy"
NEW_FIRE = "New Fire"
ON_FIRE = "On Fire"
BURNED_OUT = "Burned Out"
NEW_GROWTH = "New Growth"

# state numbers
HE = 0
NF = 1
OF = 2
BO = 3
NG = 4

NUM_STATES = 5

STATE_MAP = {HE: HEALTHY, NF: NEW_FIRE,
             OF: ON_FIRE, BO: BURNED_OUT, NG: NEW_GROWTH}

STATE_TRANS = [
    [.985, .015, 0.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, .99, .01],
    [1.0, 0.0, 0.0, 0.0, 0.0],
]

group_map = {HE: None, NF: None, OF: None, BO: None, NG: None}


def is_healthy(agent, *args):
    """
    Checking whether the state is healthy or not
    """
    return agent["state"] == HE


def is_on_fire(agent, *args):
    """
    Checking whether the state is healthy or not
    """
    return agent["state"] == OF


def tree_action(agent):
    """
    This is what trees do each turn in the forest.
    """
    global on_fire

    old_state = agent["state"]
    if is_healthy(agent):
        nearby_fires = Composite(agent.name + "'s nearby fires")
        neighbors = agent.locator.get_moore_hood(agent)
        if neighbors is not None:
            nearby_fires = neighbors.subset(is_on_fire, agent)
        if len(nearby_fires) > 0:
            if DEBUG2:
                print("Setting nearby tree on fire!")
            agent["state"] = NF

    # if we didn't catch on fire above, do probabilistic transition:
    if old_state == agent["state"]:
        agent["state"] = prob_state_trans(old_state, STATE_TRANS)

    if old_state != agent["state"]:
        agent.has_acted = True
        agent.locator.add_switch(agent, group_map[old_state],
                                 group_map[agent["state"]])
    return True


def plant_tree(name, i, state=HE):
    """
    Plant a new tree!
    By default, they start out healthy.
    """
    name = TREE_PREFIX
    return Agent(name + str(i),
                 action=tree_action,
                 attrs={"state": state,
                        "save_neighbors": True})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    init_props(MODEL_NAME, props)

    forest_height = get_prop('grid_height', DEF_DIM)
    forest_width = get_prop('grid_width', DEF_DIM)
    forest_density = get_prop('density', DEF_DENSITY)
    tree_cnt = int(forest_height * forest_width * forest_density)
    groups = []
    groups.append(Composite(HEALTHY, {"color": GREEN, "marker": TREE},
                  member_creator=plant_tree,
                  num_members=tree_cnt))
    groups.append(Composite(NEW_FIRE, {"color": TOMATO, "marker": TREE}))
    groups.append(Composite(ON_FIRE, {"color": RED, "marker": TREE}))
    groups.append(Composite(BURNED_OUT, {"color": BLACK, "marker": TREE}))
    groups.append(Composite(NEW_GROWTH, {"color": SPRINGGREEN, "marker":
                                         TREE}))

    Env("Forest", height=forest_height, width=forest_width, members=groups)

    global group_map
    group_map = {HE: groups[HE], NF: groups[NF],
                 OF: groups[OF], BO: groups[BO], NG: groups[NG]}


def main():
    set_up()
    get_env()()
    return 0


if __name__ == "__main__":
    main()
