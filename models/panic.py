"""
A model to simulate the spread of fire in a forest.
"""

from indra.agent import Agent, DONT_MOVE
from indra.composite import Composite
from indra.space import neighbor_ratio
from indra.display_methods import RED, GREEN
from indra.display_methods import TREE
from indra.env import Env
from registry.execution_registry import CLI_EXEC_KEY, \
    EXEC_KEY, get_exec_key
from registry.registry import get_env, get_prop, set_env_attr
from registry.registry import run_notice, user_log_notif
from indra.utils import init_props
import random

MODEL_NAME = "panic"
DEBUG = False  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

# agent groups
CALM = "Calm"
PANIC = "Panic"

DEF_DIM = 10
DEF_NUM_PEOPLE = DEF_DIM*2
DEF_PANIC = .1

AGENT_PREFIX = "Agent"
THRESHHOLD = 3


def is_calm(agent, *args):
    """
    Checking whether the state is healthy or not
    """
    return str(agent.primary_group()) == CALM


def is_panicking(agent, *args):
    """
    Checking whether the state is on fire or not
    """
    return str(agent.primary_group()) == PANIC


def agent_action(agent, **kwargs):
    """
    This is what trees do each turn in the forest.
    """
    execution_key = get_exec_key(kwargs=kwargs)
    print("The agent's position", agent.name)
    ratio = neighbor_ratio(agent, pred_one=is_calm, pred_two=is_panicking,
                           execution_key=execution_key)
    print("The ratio is", ratio)
    if ratio > THRESHHOLD:
        if DEBUG2:
            user_log_notif("Changing the agent's state to panic!")
        env = get_env(execution_key=execution_key)
        agent.has_acted = True
        env.add_switch(agent, CALM, PANIC)
    return DONT_MOVE


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
    per_panic = get_prop('per_panic', DEF_PANIC, execution_key=execution_key)
    per_panic = per_panic/100
    groups = []
    calm = Composite(CALM, {"color": GREEN, "marker": TREE},
                     execution_key=execution_key)
    groups.append(calm)
    panic = Composite(PANIC, {"color": RED, "marker": TREE},
                      execution_key=execution_key)
    groups.append(panic)

    Env(MODEL_NAME, height=grid_height,
        width=grid_width, members=groups,
        execution_key=execution_key)
    for x in range(grid_width):
        for y in range(grid_height):
            dist = random.random()
            if per_panic > dist:
                agent = Agent(name=("(%d,%d)" % (x, y)),
                              action=agent_action,
                              execution_key=execution_key)
                loc = eval(agent.name)
                panic += agent
                get_env().place_member(agent, xy=loc)
            else:
                agent = Agent(name=("(%d,%d)" % (x, y)),
                              action=agent_action,
                              execution_key=execution_key)
                loc = eval(agent.name)
                calm += agent
                get_env().place_member(agent, xy=loc)
    # whereas these settings must be re-done every API re-load:
    set_env_attr(execution_key, CLI_EXEC_KEY)


def main():
    set_up()
    run_notice(MODEL_NAME)
    get_env()()
    return 0


if __name__ == "__main__":
    main()
