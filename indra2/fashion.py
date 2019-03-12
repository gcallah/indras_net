
"""
    This is the fashion model re-written in indra2.
"""

from indra2.agent import Agent
from indra2.composite import Composite
from indra2.space import in_hood
from indra2.env import Env

DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

NUM_TSETTERS = 5
NUM_FOLLOWERS = 10

BLUE = 0
RED = 1

HOOD_SIZE = 4

tsetters = None
followers = None


def is_red(agent):
    return agent["color"] == RED


def is_blue(agent):
    return agent["color"] == BLUE


def change_color(agent):
    if is_red(agent):
        agent["color"] = BLUE
    else:
        agent["color"] = RED


def follower_action(agent):
    hood = tsetters.subset(in_hood, agent, HOOD_SIZE, name="hood")
    num_tsetters = len(hood)
    filter = is_blue
    if is_blue(agent):
        filter = is_red
    opp_tsetters = len(hood.subset(filter, name="TREDS"))
    if (opp_tsetters > 0) and (opp_tsetters > (num_tsetters // 2)):
        change_color(agent)
        if DEBUG:
            print(agent.name + " changed color!")
    print("I'm " + agent.name + " and I saw "
          + str(opp_tsetters)
          + " opposites out of " + str(num_tsetters) + ".")


def tsetter_action(agent):
    hood = followers.subset(in_hood, agent, HOOD_SIZE, name="hood")
    num_followers = len(hood)
    filter_t = is_blue
    if is_red(agent):
        filter_t = is_red
    same_followers = len(hood.subset(filter_t, name="FREDS"))
    if (same_followers > 0) and (same_followers > (num_followers // 2)):
        change_color(agent)
        if DEBUG:
            print(agent.name + " changed color!")
    print("I'm " + agent.name + " and I saw "
          + str(same_followers)
          + " similar out of " + str(same_followers) + ".")
    # red_followers = hood.subset(is_blue, name="FREDS")
    # print("I'm " + agent.name + " and I saw " + str(len(red_followers))
    #       + " blue out of " + str(num_followers) + ".")


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

society = Env("society", members=[tsetters, followers])
if DEBUG2:
    print(society.__repr__())

society()

if DEBUG2:
    print(society.__repr__())
