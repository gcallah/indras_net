
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

FOLLOWER_PRENM = "follower"
TSETTER_PRENM="tsetter"
RED_FOLLOWERS = "Red Followers"
BLUE_FOLLOWERS = "Blue Followers"
RED_TSETTERS = "Red Trendsetters"
BLUE_TSETTERS = "Blue Trendsetters"

red_tsetters = None
blue_tsetters = None
red_followers = None
blue_followers = None
society = None

opp_group = None


def change_color(agent, society, opp_group):
    if DEBUG:
        print("Agent " + str(agent) + " is changing colors from "
              + str(agent.primary_group()) + " to "
              + str(opp_group[str(agent.primary_group())]))
    society.add_switch(agent, agent.primary_group(),
                       opp_group[str(agent.primary_group())])


def follower_action(agent):
    num_red_ts = max(len(red_tsetters.subset(in_hood, agent, HOOD_SIZE)),
                     NOT_ZERO)   # prevent div by zero!
    num_blue_ts = max(len(blue_tsetters.subset(in_hood, agent, HOOD_SIZE)),
                      NOT_ZERO)   # prevent div by zero!
    ratio = 1
    if DEBUG:
        print("In follower action, we get num_red_ts = " + str(int(num_red_ts))
              + " and num_blue_ts = " + str(int(num_blue_ts)))
    if agent.primary_group() == red_followers:
        ratio = num_blue_ts / num_red_ts
    else:
        ratio = num_red_ts / num_blue_ts

    if ratio > 1:
        change_color(agent, society, opp_group)


def tsetter_action(agent):
    # pass
    num_red_fs = max(len(red_followers.subset(in_hood, agent, HOOD_SIZE)),
                     NOT_ZERO)   # prevent div by zero!
    num_blue_fs = max(len(blue_followers.subset(in_hood, agent, HOOD_SIZE)),
                      NOT_ZERO)   # prevent div by zero!
    ratio = 1
    if DEBUG:
        print("In trendsetter action, we get num_red_fs = "
              + str(int(num_red_fs))
              + " and num_blue_fs = " + str(int(num_blue_fs)))
    if agent.primary_group() == blue_tsetters:
        ratio = num_blue_fs / num_red_fs
    else:
        ratio = num_red_fs / num_blue_fs

    if ratio < 1:
        change_color(agent, society, opp_group)


def create_tsetter(i, color=RED):
    """
    Create a trendsetter: all RED to start.
    """
    return Agent(TSETTER_PRENM + str(i),
                 action=tsetter_action,
                 attrs={"color": color})


def create_follower(i, color=BLUE):
    """
    Create a follower: all BLUE to start.
    """
    return Agent(FOLLOWER_PRENM + str(i),
                 action=follower_action,
                 attrs={"color": color})


def set_up():
    """
    A func to set up run that can also be used by test code.
    """
    blue_tsetters = Composite(BLUE_TSETTERS)
    red_tsetters = Composite(RED_TSETTERS)
    for i in range(NUM_TSETTERS):
        red_tsetters += create_tsetter(i)

    if DEBUG2:
        print(red_tsetters.__repr__())

    red_followers = Composite(RED_FOLLOWERS)
    blue_followers = Composite(BLUE_FOLLOWERS)
    for i in range(NUM_FOLLOWERS):
        blue_followers += create_follower(i)

    opp_group = {str(red_tsetters): blue_tsetters,
                 str(blue_tsetters): red_tsetters,
                 str(red_followers): blue_followers,
                 str(blue_followers): red_followers}

    if DEBUG2:
        print(blue_followers.__repr__())

    society = Env("society", members=[blue_tsetters, red_tsetters,
                                      blue_followers, red_followers])
    return (blue_tsetters, red_tsetters, blue_followers, red_followers,
            opp_group, society)


def main():
    global red_tsetters
    global blue_tsetters
    global red_followers
    global blue_followers
    global society
    global opp_group

    (blue_tsetters, red_tsetters, blue_followers, red_followers, opp_group,
     society) = set_up()

    if DEBUG2:
        print(society.__repr__())

    society()


if __name__ == "__main__":
    main()
