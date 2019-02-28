
"""
    This is the fashion model re-written in indra2.
"""

from indra2.agent import Agent
from indra2.composite import Composite
from indra2.space import in_hood
from indra2.env import Env

DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

NUM_TSETTERS = 3
NUM_FOLLOWERS = 10

BLUE = 0
RED = 1

HOOD_SIZE = 4

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
    hood = tsetters.subset(in_hood, agent, HOOD_SIZE, name="hood")
    num_tsetters = len(hood)
    red_tsetters = hood.subset(is_red, name="TREDS")
    if len(red_tsetters) == num_tsetters:
        agent["color"] = RED
        print("I'm " + agent.name + " and I saw " + str(len(red_tsetters))
              + " red out of " + str(num_tsetters) + ".")


def tsetter_action(agent):
    hood = followers.subset(in_hood, agent, HOOD_SIZE, name="hood")
    num_followers = len(hood)
    red_followers = hood.subset(is_blue, name="FREDS")
    print("I'm " + agent.name + " and I saw " + str(len(red_followers))
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

society = Env("society")
society += tsetters
society += followers
if DEBUG2:
    print(society.__repr__())

society()

if DEBUG2:
    print(society.__repr__())
