
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

NOT_ZERO = .001

HOOD_SIZE = 4

red_tsetters = None
blue_tsetters = None
red_followers = None
blue_followers = None
society = None

opp_group = None


def change_color(agent):
    if DEBUG:
        print("Agent " + str(agent) + " is changing colors.")
    society.add_switch(agent, agent.primary_group(),
                       opp_group[str(agent.primary_group())])


def follower_action(agent):
    num_red_ts = max(len(red_tsetters.subset(in_hood, agent, HOOD_SIZE)),
                     NOT_ZERO)   # prevent div by zero!
    num_blue_ts = max(len(blue_tsetters.subset(in_hood, agent, HOOD_SIZE)),
                      NOT_ZERO)   # prevent div by zero!
    ratio = 1
    if DEBUG:
        print("In follower action, we get num_red_ts = " + str(num_red_ts)
              + " and num_blue_ts = " + str(num_blue_ts))
    if agent.primary_group() == red_followers:
        ratio = num_blue_ts / num_red_ts
    else:
        ratio = num_red_ts / num_blue_ts

    if ratio > 1:
        change_color(agent)


def tsetter_action(agent):
    pass


def create_tsetter(i, color=RED):
    """
    Create a trendsetter: all RED to start.
    """
    return Agent("tsetter" + str(i),
                 action=tsetter_action,
                 attrs={"color": color})


def create_follower(i, color=BLUE):
    """
    Create a follower: all BLUE to start.
    """
    return Agent("follower" + str(i),
                 action=follower_action,
                 attrs={"color": color})


blue_tsetters = Composite("blue_tsetters")
red_tsetters = Composite("red_tsetters")
for i in range(NUM_TSETTERS):
    red_tsetters += create_tsetter(i)

if DEBUG2:
    print(red_tsetters.__repr__())

red_followers = Composite("red_followers")
blue_followers = Composite("blue_followers")
for i in range(NUM_FOLLOWERS):
    blue_followers += create_follower(i)

opp_group = {str(red_tsetters): blue_tsetters,
             str(blue_tsetters): red_tsetters,
             str(red_followers): blue_followers,
             str(blue_followers): red_followers}

if DEBUG2:
    print(blue_followers.__repr__())

society = Env("society", members=[blue_tsetters, red_tsetters, blue_followers,
                                  red_followers])
if DEBUG2:
    print(society.__repr__())

society()
