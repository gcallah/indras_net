
"""
    This is wolf-sheep re-written in indra2.
"""

import indra2.agent as agt
import indra2.composite as cmp
from itime import Time

DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

NUM_WOLVES = 10
NUM_SHEEP = 40

WOLF_LIFESPAN = 5
WOLF_REPRO_PERIOD = 6


def sheep_action(agent):
    print("I'm " + agent.name + " and I eat grass.")


def wolf_action(agent):
    agent["time_to_repr"] -= 1
    if agent["time_to_repr"] == 0:
        # reproduce!
        agent["time_to_repr"] = WOLF_REPRO_PERIOD
    print("I'm " + agent.name + " and my remaining life is: "
          + str(agent.duration))


def create_wolf(i):
    return agt.Agent("wolf" + str(i), duration=WOLF_LIFESPAN,
                     action=wolf_action,
                     attrs={"time_to_repr": WOLF_REPRO_PERIOD})


def create_sheep(i):
    return agt.Agent("sheep" + str(i), action=sheep_action)


wolves = cmp.Composite("wolves")
for i in range(NUM_WOLVES):
    wolves += create_wolf(i)

if DEBUG2:
    print(wolves.__repr__())

sheep = cmp.Composite("sheep")
for i in range(NUM_SHEEP):
    sheep += create_sheep(i)

if DEBUG2:
    print(sheep.__repr__())

meadow = Time("meadow")
meadow += wolves
meadow += sheep
if DEBUG2:
    print(meadow.__repr__())

meadow(10)
