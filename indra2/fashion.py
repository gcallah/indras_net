
"""
    This is the fashion model re-written in indra2.
"""

from indra2.agent import Agent
from indra2.composite import Composite
# from indra2.space import in_hood
from indra2.itime import Time

DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

NUM_TSETTERS = 3
NUM_FOLLOWERS = 10

BLUE = 0
RED = 1

tsetters = None
followers = None


def is_red(agent):
    color = agent["color"]
    if DEBUG2:
        print("in is_red(); agent " + agent.name
              + "'s color is " + str(color))
    return color == RED


def is_blue(agent):
    color = agent["color"]
    return color == BLUE


def follower_action(agent):
    # hood = tsetters.subset(in_hood, agent, 3, name="hood")
    # num_tsetters = len(hood)
    # red_tsetters = hood.subset(is_red, name="TREDS")
    num_tsetters = len(tsetters)
    red_tsetters = tsetters.subset(is_red, name="TREDS")
    print("I'm " + agent.name + " and I saw " + str(len(red_tsetters))
          + " red out of " + str(num_tsetters) + ".")


def tsetter_action(agent):
    num_followers = len(followers)
    blue_followers = followers.subset(is_blue, name="FBLUES")
    print("I'm " + agent.name + " and I saw " + str(len(blue_followers))
          + " blue out of " + str(num_followers) + ".")


def create_tsetter(i):
    return Agent("tsetter" + str(i),
                 action=tsetter_action,
                 attrs={"color": RED})


def create_follower(i):
    return Agent("follower" + str(i),
                 action=follower_action,
                 attrs={"color": BLUE})


tsetters = Composite("tsetters")
for i in range(NUM_TSETTERS):
    tsetters += create_tsetter(i)

if DEBUG2:
    print(tsetters.__repr__())

followers = Composite("follower")
for i in range(NUM_FOLLOWERS):
    followers += create_follower(i)

if DEBUG2:
    print(followers.__repr__())

society = Time("society")
society += tsetters
society += followers
if DEBUG2:
    print(society.__repr__())

society(10)

if DEBUG2:
    print(society.__repr__())
