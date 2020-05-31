"""
    This is wolf-sheep re-written in indra.
"""
from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import TAN, GRAY
from indra.env import Env
from registry.registry import get_prop, get_group, get_env
from registry.registry import user_tell, run_notice
from indra.space import in_hood
from indra.utils import init_props

MODEL_NAME = "wolfsheep"
DEBUG = False  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off
NUM_WOLVES = 8
NUM_SHEEP = 20
HOOD_SIZE = 3
MEADOW_HEIGHT = 10
MEADOW_WIDTH = 10

WOLF_LIFESPAN = 5
WOLF_REPRO_PERIOD = 6

SHEEP_LIFESPAN = 8
SHEEP_REPRO_PERIOD = 3

AGT_WOLF_NAME = "wolf"
AGT_SHEEP_NAME = "sheep"

WOLF_GROUP = "wolves"
SHEEP_GROUP = "sheep"

ERR_MSG = "Invalid agent name"

wolves_created = 0
sheep_created = 0


def isactive(agent, *args):
    """
    See if what wolf is going to eat is alive!
    """
    return agent.is_active()


def live_and_close(agent, *args):
    return in_hood(agent, *args) and isactive(agent, *args)


def eat(agent, prey):
    """
     Wolf's duration increases by sheep's duration
     """
    if DEBUG:
        user_tell("The prey is alive? " + str(isactive(prey)))
        user_tell(str(agent) + " is eating " + str(prey))
    agent.duration += prey.duration
    prey.die()


def get_prey(agent, sheep):
    """
        Wolves eat active sheep from the neighbourhood
    """
    prey = None
    hood = sheep.subset(in_hood, agent, HOOD_SIZE, name="hood")
    if len(hood) > 0:
        live_hood = hood.subset(isactive, agent, name="livehood")
        if len(live_hood) > 0:
            prey = live_hood.rand_member()
    return prey


def reproduce(agent, create_func, num_created, group):
    """
    Agents reproduce when "time_to_repr" reaches 0
    """
    if agent["time_to_repr"] == 0:
        get_env().add_child(group)
        agent["time_to_repr"] = agent["orig_repr_time"]
        return True
    else:
        return False


def sheep_action(agent):
    global sheep_created

    agent["time_to_repr"] -= 1
    reproduce(agent, create_sheep, sheep_created, get_group(SHEEP_GROUP))
    return False


def wolf_action(agent):
    global wolves_created

    prey = get_prey(agent, get_group(SHEEP_GROUP))
    if prey is not None:
        eat(agent, prey)
    agent["time_to_repr"] -= 1
    reproduce(agent, create_wolf, wolves_created, get_group(WOLF_GROUP))
    return False


def create_wolf(name, i):
    """
    Method to create wolf
    """
    global wolves_created

    wolves_created += 1
    return Agent(AGT_WOLF_NAME + str(i),
                 duration=WOLF_LIFESPAN,
                 action=wolf_action,
                 attrs={"time_to_repr": WOLF_REPRO_PERIOD,
                        "orig_repr_time": WOLF_REPRO_PERIOD})


def create_sheep(name, i):
    """
    Method to create sheep
    """
    global sheep_created

    sheep_created += 1
    return Agent(AGT_SHEEP_NAME + str(i),
                 duration=SHEEP_LIFESPAN,
                 action=sheep_action,
                 attrs={"time_to_repr": SHEEP_REPRO_PERIOD,
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
        height=get_prop('meadow_height', MEADOW_HEIGHT),
        width=get_prop('meadow_width', MEADOW_WIDTH))


def main():
    set_up()
    run_notice(MODEL_NAME)
    get_env()()
    return 0


if __name__ == "__main__":
    main()
