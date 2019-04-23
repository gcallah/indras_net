"""
    This is wolf-sheep re-written in indra.
"""

from indra.agent import Agent
from indra.composite import Composite
from indra.space import in_hood
from indra.env import Env
from indra.display_methods import BLACK, GREEN

DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

NUM_WOLVES = 5
NUM_SHEEP = 20
SHEEP_WOLVES_RATIO = 2
HOOD_SIZE = 10

WOLF_LIFESPAN = 5
WOLF_REPRO_PERIOD = 6

SHEEP_LIFESPAN = 8
SHEEP_REPRO_PERIOD = 3

AGT_WOLF_NAME = "wolf"
AGT_SHEEP_NAME = "sheep"

COMP_WOLF_NAME = "wolves"
COMP_SHEEP_NAME = "sheep"

ERR_MSG = "Invalid agent name"


wolves = None
sheep = None
meadow = None
prey = None
create_wolf = None
create_sheep = None
wolves_created = 0
sheep_created = 0


def isactive(agent, *args):
    return agent.isactive()


# yet to discuss with Professor for refactoring
# don't do this recursively: instead add a filter in the action
# def rand_sheep(hood):
#     return hood.rand_member()

def eat(agent, prey):
    """
     Wolf's duration increases by sheep's duration
     """
    if DEBUG:
        print(str(agent) + " is eating " + str(prey))
    agent.duration += prey.duration
    prey.die()


def getPrey(agent, sheep):
    """
        Wolves eat active sheep from the neighbourhood
    """
    global prey
    hood = sheep.subset(in_hood, agent, HOOD_SIZE, name="hood")
    live_hood = hood.subset(isactive, agent, name="livehood")
    if len(live_hood) > 0:
        prey = live_hood.rand_member()
    return prey


def reproduce(agent):
    """
    Agents reproduce when "time_to_repr" reaches 0
    """
    if agent["time_to_repr"] == 0:
        meadow.add_child(create_wolf(wolves_created), wolves)
        agent["time_to_repr"] = WOLF_REPRO_PERIOD


def sheep_action(agent):
    global sheep
    global sheep_created

    agent["time_to_repr"] -= 1
    if agent["time_to_repr"] == 0:
        # reproduce
        meadow.add_child(create_sheep(sheep_created), sheep)
        agent["time_to_repr"] = SHEEP_REPRO_PERIOD
    return False


def wolf_action(agent):
    global wolves
    global wolves_created

    num_sheep = len(sheep)
    if DEBUG2:
        print("Num sheep = " + str(num_sheep))
    prey = getPrey(agent, sheep)
    if prey is not None:
        eat(agent, prey)
    agent["time_to_repr"] -= 1
    reproduce(agent)
    return False


def create_wolf(i):
    global wolves_created
    wolves_created += 1
    return Agent(AGT_WOLF_NAME + str(i), duration=WOLF_LIFESPAN,
                 action=wolf_action,
                 attrs={"time_to_repr": WOLF_REPRO_PERIOD})


def create_sheep(i):
    global sheep_created
    sheep_created += 1
    return Agent(AGT_SHEEP_NAME + str(i), duration=SHEEP_LIFESPAN,
                 action=sheep_action,
                 attrs={"time_to_repr": SHEEP_REPRO_PERIOD})


def set_up():
    """
    A func to set up run that can also be used by test code.
    """
    wolves = Composite(COMP_WOLF_NAME, {"color": BLACK})
    for i in range(NUM_WOLVES):
        wolves += create_wolf(i)

    if DEBUG2:
        print(wolves.__repr__())

    sheep = Composite(COMP_SHEEP_NAME, {"color": GREEN})
    for i in range(NUM_SHEEP):
        sheep += create_sheep(i)

    if DEBUG2:
        print(sheep.__repr__())

    meadow = Env("meadow", members=[wolves, sheep])
    return (wolves, sheep, meadow)


def main():
    global wolves
    global sheep
    global meadow

    (wolves, sheep, meadow) = set_up()

    if DEBUG2:
        print(meadow.__repr__())

    meadow()
    return 0


if __name__ == "__main__":
    main()
