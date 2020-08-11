"""
    active: true,
    doc: A toy model to test the system.,
    graph: scatter,
    name: Basic,
    props: models/props/basic.props.json,
    run: basic,
    source: https://github.com/gcallah/indras_net/blob/master/models/basic.py
"""
from random import gauss

from indra.agent import Agent, MOVE
from indra.composite import Composite
from indra.display_methods import RED, BLUE
from indra.env import Env
from registry.registry import get_env, get_prop, get_registration
from registry.registry import set_env_attr, get_group
from registry.registry import user_tell, run_notice, user_log_notif
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.utils import init_props

MODEL_NAME = "height"
DEBUG = False  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

NATURAL = "Natural"
GENENG = "Genetically Engineered"

START_HEIGHT = 1.0
DEF_SIGMA = .1

DEF_NUM_GENENG = 10
DEF_NUM_NATURAL = 10

DEF_DURATION = 2


def geneng_action(agent, **kwargs):
    """
    Action for genetically engineered agent.
    """
    get_env().add_child(GENENG)
    return MOVE


def natural_action(agent, **kwargs):
    """
    Action for natural agent.
    """
    get_env().add_child(NATURAL)
    return MOVE


def create_geneng(name, i, **kwargs):
    """
    Create an agent.
    """
    dur = get_prop("lifespan", DEF_DURATION)
    return Agent(name + str(i), action=geneng_action,
                 duration=dur, attrs={"height": START_HEIGHT})


def create_natural(name, i, **kwargs):
    """
    Create an agent.
    """
    dur = get_prop("lifespan", DEF_DURATION)
    height = gauss(START_HEIGHT, DEF_SIGMA)
    return Agent(name + str(i), action=natural_action,
                 duration=dur, attrs={"height": height})


def height_rpt(env, **kwargs):
    natural = get_group(NATURAL)
    geneng = get_group(GENENG)
    num_natural = len(natural)
    num_geneng = len(geneng)
    total_nat_height = 0
    # total_gen_height = 0
    for agent_nm in natural:
        agent = get_registration(agent_nm)
        total_nat_height += agent["height"]
    user_tell("\n**************")
    user_tell("Height Report:")
    user_tell("**************")
    user_tell(f"For the {num_natural} people in the natural group,")
    user_tell("we have an average height of: "
              + f"{total_nat_height / num_natural}")
    user_tell(f"For the {num_geneng} people in the gen eng group,")
    user_tell("we have an average height of:")


def set_env_attrs():
    user_log_notif("Setting env attrs for " + MODEL_NAME)
    set_env_attr("census_func", height_rpt)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    init_props(MODEL_NAME, props)
    geneng_group = Composite(GENENG, {"color": BLUE},
                             member_creator=create_geneng,
                             num_members=get_prop('num_geneng',
                                                  DEF_NUM_GENENG))
    natural_group = Composite(NATURAL, {"color": RED},
                              member_creator=create_natural,
                              num_members=get_prop('num_natural',
                                                   DEF_NUM_NATURAL))

    Env(MODEL_NAME,
        height=get_prop('grid_height', DEF_HEIGHT),
        width=get_prop('grid_width', DEF_WIDTH),
        members=[geneng_group, natural_group])
    set_env_attrs()


def main():
    set_up()
    run_notice(MODEL_NAME)
    get_env()()
    return 0


if __name__ == "__main__":
    main()
