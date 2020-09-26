"""
A model to simulate the spread of fire in a forest.
"""

from indra.agent import Agent
from indra.composite import Composite
from indra.space import neighbor_ratio
from indra.display_methods import RED, GREEN
from indra.display_methods import TREE
from indra.env import Env
from registry.execution_registry import CLI_EXEC_KEY, \
    EXEC_KEY, get_exec_key
from registry.registry import get_env, get_prop
from registry.registry import run_notice, user_log_notif
from indra.utils import init_props

MODEL_NAME = "panic"
DEBUG = False  # turns debugging code on or off
DEBUG2 = True  # turns deeper debugging code on or off

DEF_DIM = 30
DEF_NUM_PEOPLE = DEF_DIM*2
NUM_PANIC = 8

AGENT_PREFIX = "Agent"
THRESHHOLD = .5

# tree condition strings
CALM = "Clam"
PANIC = "Panic"

# state numbers: create as strings for JSON,
# convert to int when we need 'em that way
CM = "0"
PN = "1"


def is_calm(agent, *args):
    """
    Checking whether the state is healthy or not
    """
    return agent["state"] == CM


def is_in_panic(agent, *args):
    """
    Checking whether the state is on fire or not
    """
    return agent["state"] == PN


# we also need to set up a panic at some places on the map
def agent_action(agent, **kwargs):
    """
    This is what trees do each turn in the forest.
    """
    execution_key = get_exec_key(kwargs=kwargs)
    if is_calm(agent):
        # we need ration of panic neighbours to calm to be 1/2 in order for the
        # agent to start panicking
        if neighbor_ratio(agent, pred_one=is_calm, pred_two=is_in_panic,
                          execution_key=execution_key) > THRESHHOLD:
            if DEBUG2:
                user_log_notif("Changing the agent's state to panic!")
            agent["state"] = PN
    return True


# should we place panicking agents like in bigbox model after a certain period?
def place_agent(name, i, state=CALM, **kwargs):
    """
    Place a new agent.
    By default, they start out calm.
    """
    execution_key = get_exec_key(kwargs=kwargs)
    name = AGENT_PREFIX
    return Agent(name + str(i),
                 action=agent_action,
                 attrs={"state": state,
                        "save_neighbors": True}, execution_key=execution_key)


'''
def set_env_attrs(execution_key=CLI_EXEC_KEY):
    """
    I actually don't think we need to do this here!
    It can be done once in set_up().
    """
    user_log_notif("Setting env attrs for the panic model.")
    set_env_attr(GROUP_MAP,
                 {CM: CALM,
                  PN: PANIC}, execution_key)

'''


def set_up(props=None):
    """
    A func to set up a  run that can also be used by test code.
    """
    init_props(MODEL_NAME, props)

    execution_key = int(props[EXEC_KEY].val) \
        if props is not None else CLI_EXEC_KEY

    grid_height = get_prop('grid_height', DEF_DIM,
                           execution_key=execution_key)
    grid_width = get_prop('grid_width', DEF_DIM, execution_key=execution_key)
    people_count = int(grid_height * grid_width)
    groups = []
    groups.append(Composite(CALM, {"color": GREEN, "marker": TREE},
                            member_creator=place_agent,
                            num_members=people_count-60,
                            execution_key=execution_key))
    panic = Composite(PANIC, {"color": RED, "marker": TREE},
                      member_creator=place_agent,
                      num_members=60,
                      execution_key=execution_key))
    groups.append(panic)

    """
    for y in range(height):
        for x in range(width):
            rand_val = random.random()  # between 0 and 1?
            if rand_val < percent_panic:
                # place this agent in panic group
                panic += place_agent(x, y, execution_key)
            else:
                # place this agent in calm group
                calm += place_agent(x, y, execution_key)
    """
    Env(MODEL_NAME, height=grid_height, width=grid_width, members=groups,
        execution_key=execution_key)
    # whereas these settings must be re-done every API re-load:
    # set_env_attrs(execution_key="execution_key")


def main():
    set_up()
    run_notice(MODEL_NAME)
    get_env()()
    return 0


if __name__ == "__main__":
    main()
