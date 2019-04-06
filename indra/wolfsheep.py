"""
    This is wolf-sheep re-written in indra.
"""

from indra.agent import Agent
from indra.composite import Composite
from indra.space import in_hood
from indra.env import Env

DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

NUM_WOLVES = 3
NUM_SHEEP = 10
SHEEP_WOLVES_RATIO = 2
HOOD_SIZE = 4

WOLF_LIFESPAN = 5
WOLF_REPRO_PERIOD = 6

SHEEP_LIFESPAN = 8
SHEEP_REPRO_PERIOD = 6

AGT_WOLF_NAME = "wolf"
AGT_SHEEP_NAME = "sheep"

COMP_WOLF_NAME = "wolves"
COMP_SHEEP_NAME = "sheep"

ERR_MSG = "Invalid agent name"


wolves = None
sheep = None
meadow = None

create_wolf = None
create_sheep = None
wolves_created = 0
sheep_created = 0


def sheep_action(agent):

    if AGT_SHEEP_NAME in agent.name:
        global sheep_created
        print("I'm " + agent.name + " and I eat grass.")

        # make sheep wander in the meadow
        meadow.move(agent, HOOD_SIZE)
        agent["time_to_repr"] -= 1
        if agent["time_to_repr"] == 0:
            # reproduce
            # print("hi")
            meadow.add_child(create_sheep(sheep_created), sheep)
            agent["time_to_repr"] = SHEEP_REPRO_PERIOD
        print("I'm " + agent.name + " and my remaining life is: "
              + str(agent.duration))
    else:
        return ERR_MSG


def wolf_action(agent):
    if AGT_WOLF_NAME in agent.name:
        global wolves
        global wolves_created

        num_sheep = len(sheep)
        if DEBUG2:
            print("Num sheep = " + str(num_sheep))

        # Wolves eat close sheep instead of ratio
        hood = sheep.subset(in_hood, agent, HOOD_SIZE, name="hood")
        if len(hood) > 0:
            prey = hood.rand_member()
            if DEBUG:
                print(str(agent) + " is eating " + str(prey))
            agent.duration += prey.duration
            prey.die()
        agent["time_to_repr"] -= 1
        if agent["time_to_repr"] == 0:
            # reproduce
            meadow.add_child(create_wolf(wolves_created), wolves)
            # wolves += create_wolf(wolves_created)
            agent["time_to_repr"] = WOLF_REPRO_PERIOD
        print("I'm " + agent.name + " and my remaining life is: "
              + str(agent.duration))

    else:
        return ERR_MSG


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

#
# wolves = Composite("wolves")
# for i in range(NUM_WOLVES):
#     wolves += create_wolf(i)
#
# if DEBUG2:
#     print(wolves.__repr__())
#
# sheep = Composite("sheep")
# for i in range(NUM_SHEEP):
#     sheep += create_sheep(i)
#
# if DEBUG2:
#     print(sheep.__repr__())
#
# meadow = Env("meadow", members=[wolves, sheep])
# if DEBUG2:
#     print(meadow.__repr__())
#
# meadow()


def set_up():
    """
    A func to set up run that can also be used by test code.
    """
    wolves = Composite(COMP_WOLF_NAME)
    for i in range(NUM_WOLVES):
        wolves += create_wolf(i)

    if DEBUG2:
        print(wolves.__repr__())

    sheep = Composite(COMP_SHEEP_NAME)
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
