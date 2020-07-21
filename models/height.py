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
from registry.registry import get_env, get_prop
from registry.registry import user_tell, run_notice
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.utils import init_props

MODEL_NAME = "height"
DEBUG = False  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_BLUE = 10

DEF_NUM_RED = 10

DEF_DURATION = 5


def geneng_action(agent, **kwargs):
    """
    Just a silly agent action function for basic model.
    """
    user_tell("I'm " + agent.name + " and I'm genetic engineering.")
    # return False means to move
    return MOVE


def natural_action(agent, **kwargs):
    """
    Just a silly agent action function for basic model.
    """
    user_tell("I'm " + agent.name + " and I'm all natural.")
    # return False means to move
    return MOVE


def create_geneng(name, i, props=None):
    """
    Create an agent.
    """
    return Agent(name + str(i), action=geneng_action,
                 duration=DEF_DURATION)


def create_natural(name, i, props=None):
    """
    Create an agent.
    """
    return Agent(name + str(i), action=natural_action,
                 duration=DEF_DURATION)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    init_props(MODEL_NAME, props)
    geneng_group = Composite("Genetic Engineering", {"color": BLUE},
                             member_creator=create_geneng,
                             num_members=get_prop('num_blue', DEF_NUM_BLUE))
    natural_group = Composite("Natural", {"color": RED},
                              member_creator=create_natural,
                              num_members=get_prop('num_red', DEF_NUM_RED))

    Env(MODEL_NAME,
        height=get_prop('grid_height', DEF_HEIGHT),
        width=get_prop('grid_width', DEF_WIDTH),
        members=[geneng_group, natural_group])


def main():
    set_up()
    run_notice(MODEL_NAME)
    get_env()()
    return 0


if __name__ == "__main__":
    main()
