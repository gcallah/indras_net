"""
A model to simulate the spread of fire in a forest.
"""

from indra.agent import Agent
from indra.agent import prob_state_trans, set_trans
from indra.composite import Composite
from indra.space import exists_neighbor
from indra.display_methods import RED, GREEN, BLACK
from indra.display_methods import SPRINGGREEN, TOMATO, TREE
from indra.env import Env
from registry.execution_registry import CLI_EXEC_KEY, \
    EXEC_KEY, get_exec_key
from registry.registry import get_env, get_prop, set_env_attr, get_env_attr
from registry.registry import user_log_err, run_notice, user_log_notif
from indra.utils import init_props

MODEL_NAME = "forestfire"
DEBUG = False  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

NEARBY = 1.8

DEF_DIM = 30
DEF_DENSITY = .44
DEF_NEW_FIRE = .01

TREE_PREFIX = "Tree"

# tree condition strings
HEALTHY = "Healthy"
NEW_FIRE = "New Fire"
ON_FIRE = "On Fire"
BURNED_OUT = "Burned Out"
NEW_GROWTH = "New Growth"

# state numbers: create as strings for JSON,
# convert to int when we need 'em that way
HE = "0"
NF = "1"
OF = "2"
BO = "3"
NG = "4"

TRANS_TABLE = "trans_table"
state_trans = [
    [1 - DEF_NEW_FIRE, DEF_NEW_FIRE, 0.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, .99, .01],
    [1.0, 0.0, 0.0, 0.0, 0.0],
]

GROUP_MAP = "group_map"


def is_healthy(agent, *args):
    """
    Checking whether the state is healthy or not
    """
    return agent["state"] == HE


def is_on_fire(agent, *args):
    """
    Checking whether the state is on fire or not
    """
    return agent["state"] == OF


def tree_action(agent, **kwargs):
    """
    This is what trees do each turn in the forest.
    """
    execution_key = get_exec_key(kwargs=kwargs)
    old_state = agent["state"]
    if is_healthy(agent):
        if exists_neighbor(agent, pred=is_on_fire,
                           execution_key=execution_key):
            if DEBUG2:
                user_log_notif("Setting nearby tree on fire!")
            agent["state"] = NF
    # if we didn't catch on fire above, do probabilistic transition:
    if old_state == agent["state"]:
        # we gotta do these str/int shenanigans with state cause
        # JSON only allows strings as dict keys
        agent["state"] = \
            str(prob_state_trans(int(old_state),
                                 get_env_attr(TRANS_TABLE,
                                              execution_key=execution_key)))
        if DEBUG2:
            if agent["state"] == NF:
                user_log_notif("Tree spontaneously catching fire.")

    if old_state != agent["state"]:
        # if we entered a new state, then...
        env = get_env(execution_key=execution_key)
        group_map = get_env_attr(GROUP_MAP, execution_key=execution_key)
        if group_map is None:
            user_log_err("group_map is None!")
            return True
        agent.has_acted = True
        env.add_switch(agent,
                       group_map[old_state],
                       group_map[agent["state"]])
    return True


def plant_tree(name, i, state=HE, **kwargs):
    """
    Plant a new tree!
    By default, they start out healthy.
    """
    execution_key = get_exec_key(kwargs=kwargs)
    name = TREE_PREFIX
    return Agent(name + str(i),
                 action=tree_action,
                 attrs={"state": state,
                        "save_neighbors": True}, execution_key=execution_key)


def set_env_attrs(execution_key=CLI_EXEC_KEY):
    """
    I actually don't think we need to do this here!
    It can be done once in set_up().
    """
    user_log_notif("Setting env attrs for forest fire.")
    set_env_attr(GROUP_MAP,
                 {HE: HEALTHY,
                  NF: NEW_FIRE,
                  OF: ON_FIRE,
                  BO: BURNED_OUT,
                  NG: NEW_GROWTH}, execution_key)


def set_up(props=None):
    """
    A func to set up a  run that can also be used by test code.
    """
    init_props(MODEL_NAME, props)

    execution_key = int(props[EXEC_KEY].val) \
        if props is not None else CLI_EXEC_KEY

    forest_height = get_prop('grid_height', DEF_DIM,
                             execution_key=execution_key)
    forest_width = get_prop('grid_width', DEF_DIM, execution_key=execution_key)
    new_fire = get_prop('new_fire', DEF_NEW_FIRE, execution_key=execution_key)
    set_trans(state_trans, HE, NF, float(new_fire), HE)
    forest_density = get_prop('density', DEF_DENSITY,
                              execution_key=execution_key)
    tree_cnt = int(forest_height * forest_width * forest_density)
    groups = []
    groups.append(Composite(HEALTHY, {"color": GREEN, "marker": TREE},
                            member_creator=plant_tree,
                            num_members=tree_cnt, execution_key=execution_key))
    groups.append(Composite(NEW_FIRE, {"color": TOMATO, "marker": TREE},
                            execution_key=execution_key))
    groups.append(Composite(ON_FIRE, {"color": RED, "marker": TREE},
                            execution_key=execution_key))
    groups.append(Composite(BURNED_OUT, {"color": BLACK, "marker": TREE},
                            execution_key=execution_key))
    groups \
        .append(Composite(NEW_GROWTH, {"color": SPRINGGREEN, "marker": TREE},
                          execution_key=execution_key))

    Env(MODEL_NAME, height=forest_height, width=forest_width, members=groups,
        execution_key=execution_key)
    # the next set should just be done once:
    set_env_attr(TRANS_TABLE, state_trans, execution_key=execution_key)
    # whereas these settings must be re-done every API re-load:
    set_env_attrs(execution_key=execution_key)


def main():
    set_up()
    run_notice(MODEL_NAME)
    get_env()()
    return 0


if __name__ == "__main__":
    main()
