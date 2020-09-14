"""
Panic model.
"""

from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import RED, BLUE
from indra.env import Env
from registry.execution_registry import CLI_EXEC_KEY, \
    EXEC_KEY, get_exec_key
from registry.registry import get_env, get_prop, set_env_attr
from registry.registry import run_notice
from indra.utils import init_props
from indra.space import neighbor_ratio

MODEL_NAME = "panic"
DEBUG = True  # Turns debugging code on or off
DEBUG2 = True  # Turns deeper debugging code on or off

NUM_CALM_AGENTS = 500
TOLERANCE = .5

NUM_PANIC_AGENTS = 10

DEF_CITY_DIM = 40

DEF_HOOD_SIZE = 1

PANIC_GRP_IDX = 0
CALM_GRP_IDX = 1

HOOD_SIZE = 4

NOT_ZERO = .001

CALM_AGENTS = "Calm agents"
PANIC_AGENTS = "Panic agents"
GRP_INDEX = "grp_index"
CALM = "Calm"
PANIC = "Panic"
STATES = "states"

group_names = [CALM_AGENTS, PANIC_AGENTS]

hood_size = None

opp_group = None


def panic_start(hood_ratio, my_tolerance):
    """
    Is the environment to our agent's liking or not??
    """
    return hood_ratio >= my_tolerance


def panic_agent_action(agent, **kwargs):
    """
    If the agent is surrounded by more "others" than it
    is comfortable with, the agent will move.
    The whole idea here is to count those in other group
    and those in my group, and get the ratio.
    """
    execution_key = get_exec_key(kwargs=kwargs)
    # agent_group = agent.group_name()
    agent_group = agent["state"]
    if agent_group == CALM:
        ratio_num = neighbor_ratio(agent,
                                   lambda agent: agent_group,
                                   size=agent['hood_size'],
                                   execution_key=execution_key)
        # the ratio is always 1
        print("the ration number is", ratio_num)
        if panic_start(ratio_num, TOLERANCE):
            print("Agents state is changed to panic")
            agent["state"] = PANIC
        if DEBUG2:
            print("ratio test" + str(ratio_num))
        return panic_start(ratio_num, TOLERANCE)


def create_resident(name, i, state=CALM, **kwargs):
    """
    Creates agent of specified color type
    """
    execution_key = get_exec_key(kwargs=kwargs)
    return Agent(name + str(i),
                 action=panic_agent_action,
                 attrs={"state": state,
                        "hood_size": get_prop('hood_size',
                                              DEF_HOOD_SIZE,
                                              execution_key=execution_key),
                        "save_neighbours": True}, execution_key=execution_key)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    init_props(MODEL_NAME, props)
    execution_key = int(props[EXEC_KEY].val) \
        if props is not None else CLI_EXEC_KEY
    calm = Composite(CALM, {"color": BLUE},
                     member_creator=create_resident,
                     num_members=get_prop('num_people',
                                          NUM_CALM_AGENTS,
                                          execution_key=execution_key),
                     group=BLUE, execution_key=execution_key)
    panic = Composite(PANIC, {"color": RED},
                      member_creator=create_resident,
                      num_members=NUM_PANIC_AGENTS,
                      group=RED, execution_key=execution_key)
    city = Env(MODEL_NAME, members=[calm, panic],
               height=get_prop('grid_height', DEF_CITY_DIM,
                               execution_key=execution_key),
               width=get_prop('grid_width', DEF_CITY_DIM,
                              execution_key=execution_key),
               execution_key=execution_key)
    set_env_attr(STATES, [CALM, PANIC], execution_key=execution_key)
    city.exclude_menu_item("line_graph")


def main():
    set_up()
    run_notice(MODEL_NAME)
    # get_env() returns a callable object:
    get_env()()
    return 0


if __name__ == "__main__":
    main()
