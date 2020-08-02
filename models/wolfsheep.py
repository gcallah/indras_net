"""
    This is wolf-sheep re-written in indra.
"""
from random import randint

from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import TAN, GRAY
from indra.env import Env
from registry.registry import get_prop, get_group, get_env, get_env_attr
from registry.registry import user_tell, run_notice, user_debug
from indra.utils import init_props

MODEL_NAME = "wolfsheep"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

# some default values:
NUM_WOLVES = 8
NUM_SHEEP = 28
PREY_DIST = 3
MEADOW_HEIGHT = 10
MEADOW_WIDTH = 10

WOLF_LIFESPAN = 5
WOLF_REPRO_PERIOD = 11

SHEEP_LIFESPAN = 8
SHEEP_REPRO_PERIOD = 3

AGT_WOLF_NAME = "wolf"
AGT_SHEEP_NAME = "sheep"

WOLF_GROUP = "wolves"
SHEEP_GROUP = "sheep"

ERR_MSG = "Invalid agent name"


def isactive(agent, *args):
    """
    See if what wolf is going to eat is alive!
    """
    return agent.is_active()


def eat(agent, prey):
    """
     Wolf's duration increases by sheep's duration
     """
    if DEBUG:
        user_tell(str(agent) + " is eating " + str(prey))
    agent.duration += prey.duration
    prey.die()


def get_prey(agent, sheep):
    """
        Wolves eat active sheep from the neighbourhood
    """
    return get_env().get_neighbor_of_groupX(agent,
                                            SHEEP_GROUP,
                                            hood_size=get_env_attr(
                                                "prey_dist"))


def reproduce(agent, create_func, group):
    """
    Agents reproduce when "time_to_repr" reaches 0
    """
    if agent["time_to_repr"] == 0:
        if DEBUG2:
            user_debug(str(agent) + " is having a baby!")
        get_env().add_child(group)
        agent["time_to_repr"] = agent["orig_repr_time"]
        return True
    else:
        return False


def sheep_action(agent, **kwargs):
    agent["time_to_repr"] -= 1
    reproduce(agent, create_sheep, get_group(SHEEP_GROUP))
    return False


def wolf_action(agent, **kwargs):
    prey = get_prey(agent, get_group(SHEEP_GROUP))
    if prey is not None:
        eat(agent, prey)
    agent["time_to_repr"] -= 1
    reproduce(agent, create_wolf, get_group(WOLF_GROUP))
    return False


def create_wolf(name, i):
    """
    Method to create wolf
    """
    time_to_repro = randint(1, WOLF_REPRO_PERIOD)
    return Agent(AGT_WOLF_NAME + str(i),
                 duration=WOLF_LIFESPAN,
                 action=wolf_action,
                 attrs={"time_to_repr": time_to_repro,
                        "orig_repr_time": WOLF_REPRO_PERIOD})


def create_sheep(name, i):
    """
    Method to create sheep
    """
    time_to_repro = randint(1, SHEEP_REPRO_PERIOD)
    return Agent(AGT_SHEEP_NAME + str(i),
                 duration=SHEEP_LIFESPAN,
                 action=sheep_action,
                 attrs={"time_to_repr": time_to_repro,
                        "orig_repr_time": SHEEP_REPRO_PERIOD})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    init_props(MODEL_NAME, props)

    members = []
    members.append(Composite(WOLF_GROUP,
                   attrs={"color": TAN},
                   member_creator=create_wolf,
                   num_members=get_prop('num_wolves', NUM_WOLVES)))

    members.append(Composite(SHEEP_GROUP,
                   attrs={"color": GRAY},
                   member_creator=create_sheep,
                   num_members=get_prop('num_sheep', NUM_SHEEP)))

    Env(MODEL_NAME,
        members=members,
        attrs={"prey_dist": get_prop("prey_dist", PREY_DIST)},
        height=get_prop('grid_height', MEADOW_HEIGHT),
        width=get_prop('grid_width', MEADOW_WIDTH))


def main():
    set_up()
    run_notice(MODEL_NAME)
    get_env()()
    return 0


if __name__ == "__main__":
    main()
