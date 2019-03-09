"""
    This is wolf-sheep re-written in indra2.
"""

from indra2.agent import Agent
from indra2.composite import Composite
from indra2.space import in_hood
from env import Env

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

wolves = None
sheep = None

create_wolf = None
create_sheep = None
wolves_created = 0


def sheep_action(agent):
    print("I'm " + agent.name + " and I eat grass.")


def wolf_action(agent):
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
        meadow.add_child(Agent("wolf" + str(wolves_created),
                               duration=WOLF_LIFESPAN,
                               action=wolf_action,
                               attrs={"time_to_repr": WOLF_REPRO_PERIOD}))
        wolves_created += 1
        # wolves += create_wolf(1)
        agent["time_to_repr"] = WOLF_REPRO_PERIOD
    print("I'm " + agent.name + " and my remaining life is: "
          + str(agent.duration))


def create_wolf(i):
    global wolves_created
    wolves_created += 1
    return Agent("wolf" + str(i), duration=WOLF_LIFESPAN,
                 action=wolf_action,
                 attrs={"time_to_repr": WOLF_REPRO_PERIOD})


def create_sheep(i):
    return Agent("sheep" + str(i), duration=SHEEP_LIFESPAN,
                 action=sheep_action,
                 attrs={"time_to_repr": SHEEP_REPRO_PERIOD})


wolves = Composite("wolves")
for i in range(NUM_WOLVES):
    wolves += create_wolf(i)

if DEBUG2:
    print(wolves.__repr__())

sheep = Composite("sheep")
for i in range(NUM_SHEEP):
    sheep += create_sheep(i)

if DEBUG2:
    print(sheep.__repr__())

meadow = Env("meadow", members=[wolves, sheep])
if DEBUG2:
    print(meadow.__repr__())

meadow()
