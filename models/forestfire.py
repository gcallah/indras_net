"""
A model to simulate the spread of fire in a forest.
"""

from indra.agent import Agent
from indra.agent import prob_state_trans
from indra.composite import Composite
from indra.display_methods import RED, GREEN, BLACK, SPRINGGREEN, TOMATO, TREE
from indra.env import Env
from indra.utils import get_props

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

on_fire = None
healthy = None

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


def plant_tree(name, i, props=None, state=HE):
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
    global on_fire
    global healthy

    pa = get_props(MODEL_NAME, props)

    forest_height = pa.get('grid_height', DEF_DIM)
    forest_width = pa.get('grid_width', DEF_DIM)
    forest_density = pa.get('density', DEF_DENSITY)
    num = int(forest_height * forest_width * forest_density)
    healthy = Composite(HEALTHY, {"color": GREEN, "marker": TREE},
                        member_creator=plant_tree, props=pa,
                        num_members=num)
    new_fire = Composite(NEW_FIRE, {"color": TOMATO, "marker": TREE})
    on_fire = Composite(ON_FIRE, {"color": RED, "marker": TREE})
    burned_out = Composite(BURNED_OUT, {"color": BLACK, "marker": TREE})
    new_growth = Composite(NEW_GROWTH, {"color": SPRINGGREEN, "marker": TREE})
    # for i in range():
    #     healthy += plant_tree(i)

    forest = Env("Forest", height=forest_height, width=forest_width,
                 members=[healthy, new_fire, on_fire, burned_out,
                          new_growth], props=pa)

    global group_map
    group_map = {HE: healthy, NF: new_fire,
                 OF: on_fire, BO: burned_out, NG: new_growth}
    return forest, group_map


def main():
    (forest, group_map) = set_up()

    if DEBUG2:
        print(forest.__repr__())

    forest()
    return 0


if __name__ == "__main__":
    main()
