"""
    This is the fashion model re-written in indra.
"""


from indra.agent import Agent, X_VEC, Y_VEC
from indra.composite import Composite
from indra.env import Env
from indra.display_methods import NAVY, DARKRED, SPRINGGREEN, GRAY
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

NUM_TSETTERS = 5
NUM_FOLLOWERS = 55
"""
Adding weighted average for having a sine curve
"""
ENV_WEIGHT = 0.6
weightings = [1.0, ENV_WEIGHT]

COLOR_PREF = "color_pref"
DISPLAY_COLOR = "display_color"

BLUE = 0.0
RED = 1.0

# for future use as we move to vector representation:
BLUE_VEC = X_VEC
RED_VEC = Y_VEC

NOT_ZERO = .001

TOO_SMALL = .01
BIG_ENOUGH = .03

HOOD_SIZE = 4

FOLLOWER_PRENM = "follower"
TSETTER_PRENM = "tsetter"
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


def create_tsetter(i, color=RED):
    """
    Create a trendsetter: all RED to start.
    """
    return Agent(TSETTER_PRENM + str(i))


def create_follower(i, color=BLUE):
    """
    Create a follower: all BLUE to start.
    """
    return Agent(FOLLOWER_PRENM + str(i))


def set_up():
    """
    A func to set up run that can also be used by test code.
    """
    blue_tsetters = Composite(BLUE_TSETTERS, {"color": NAVY})
    red_tsetters = Composite(RED_TSETTERS, {"color": DARKRED})
    for i in range(NUM_TSETTERS):
        red_tsetters += create_tsetter(i)

    if DEBUG2:
        print(red_tsetters.__repr__())

    red_followers = Composite(RED_FOLLOWERS, {"color": SPRINGGREEN})
    blue_followers = Composite(BLUE_FOLLOWERS, {"color": GRAY})
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
    return 0


if __name__ == "__main__":
    main()
