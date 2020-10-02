#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
"""
    active: true,
    doc: A toy model to test the system.,
    graph: scatter,
    name: Basic,
    props: models/props/basic.props.json,
    run: basic,
    source: https://github.com/gcallah/indras_net/blob/master/models/basic.py
"""

from indra.agent import Agent, MOVE
from indra.composite import Composite
from indra.display_methods import RED, BLUE
from indra.env import Env
from registry.execution_registry import CLI_EXEC_KEY, \
    EXEC_KEY
from registry.registry import get_env, get_prop
from registry.registry import user_tell, run_notice
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.utils import init_props

MODEL_NAME = "basic"
DEBUG = False  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_BLUE = 10

DEF_NUM_RED = 10


def agent_action(agent, **kwargs):
    """
    Just a silly agent action function for basic model.
    """
    user_tell("I'm " + agent.name + " and I'm acting.")
    # return False means to move
    return MOVE


def create_agent(name, i, **kwargs):
    """
    Create an agent.
    """
    return Agent(name + str(i), action=agent_action, kwargs=kwargs)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    init_props(MODEL_NAME, props)
    execution_key = int(props[EXEC_KEY].val) \
        if props is not None else CLI_EXEC_KEY

    blue_group = Composite("Blues", {"color": BLUE},
                           member_creator=create_agent,
                           num_members=get_prop('num_blue', DEF_NUM_BLUE,
                                                execution_key=execution_key),
                           execution_key=execution_key)
    red_group = Composite("Reds", {"color": RED},
                          member_creator=create_agent,
                          num_members=get_prop('num_red', DEF_NUM_RED,
                                               execution_key=execution_key),
                          execution_key=execution_key)

    Env(MODEL_NAME,
        height=get_prop('grid_height', DEF_HEIGHT,
                        execution_key=execution_key),
        width=get_prop('grid_width', DEF_WIDTH, execution_key=execution_key),
        members=[blue_group, red_group], execution_key=execution_key)


def main():
    set_up()
    run_notice(MODEL_NAME)
    get_env()()
    return 0


if __name__ == "__main__":
    main()
