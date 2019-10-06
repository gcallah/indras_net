"""
A used cars model.
Places two groups of agents in the enviornment randomly
and moves them around randomly.
"""

import random

from indra.utils import get_props
from indra.agent import Agent
from indra.composite import Composite
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.env import Env
from indra.display_methods import RED, BLUE

MODEL_NAME = "used cars"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_BLUE = 10
DEF_NUM_RED = 10

MIN_CAR_LIFE = 1
MAX_CAR_LIFE = 5

DEALERS = "Dealers"

buyer_grp = None
dealer_grp = None
env = None


def bought_info(agent, dealer):
    msg = "My dealer is: " + dealer + "\nReceived a car with a life of " + str(agent["car_life"])
    msg += "\nMy dealer" + dealer + "has an avg car life of" + str(dealer["avg_car_life_sold"])
    msg += ". And sold "+ str(dealer["num_sales"]+" cars.")

    return msg

def is_dealer(agent):
    return dealer_grp.ismember(agent)


def get_car_life(dealer):
    print("Getting car from dealer", dealer)
    return random.randint(MIN_CAR_LIFE, MAX_CAR_LIFE)


def dealer_action(agent):
    env.user.tell("I'm " + agent.name + " and I'm a dealer.")
    # return False means to move
    return False

def calculate_avg_car_life_sold(dealer, new_car_life):
    return (dealer["avg_car_life_sold"] * dealer["num_sales"] + new_car_life) / (dealer["num_sales"] + 1)

def buyer_action(agent):
    if not agent["has_car"]:
        my_dealer = env.get_neighbor_of_groupX(agent, dealer_grp,
                                               hood_size=1)
        if my_dealer is not None:
            agent["has_car"] = True
            received_car_life = get_car_life(my_dealer)
            agent["car_life"] = received_car_life
            my_dealer["avg_car_life_sold"] = calculate_avg_car_life_sold(my_dealer, received_car_life)
            my_dealer["num_sales"] += 1
            print(bought_info(agent, my_dealer))
            print("Dealer", my_dealer, "has an avg car life of", my_dealer["avg_car_life_sold"])
        else:
            print("No dealers nearby.")
    else:
        print("I have a car!")
        agent["car_life"] -= 1
        if agent["car_life"] <= 0:
            agent["has_car"] = False

    # return False means to move
    return False


def create_dealer(name, i, props=None):
    """
    Create an agent.
    """
    return Agent(name + str(i),
                 action=dealer_action,
                 attrs = {"num_sales": 0, "num_returns": 0, "avg_car_life_sold": MIN_CAR_LIFE})


def create_buyer(name, i, props=None):
    """
    Create an agent.
    """
    return Agent(name + str(i),
                 action=buyer_action,
                 attrs = {"has_car": False, "car_life": MAX_CAR_LIFE})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    pa = get_props(MODEL_NAME, props)
    dealer_grp = Composite(DEALERS, {"color": BLUE},
                           member_creator=create_dealer,
                           num_members=pa.get('num_sellers', DEF_NUM_BLUE))
    buyer_grp = Composite("Buyers", {"color": RED},
                          member_creator=create_buyer,
                          num_members=pa.get('num_buyers', DEF_NUM_RED))

    env = Env("env",
              height=pa.get('grid_height', DEF_HEIGHT),
              width=pa.get('grid_width', DEF_WIDTH),
              members=[dealer_grp, buyer_grp],
              props=pa)

    return (env, dealer_grp, buyer_grp)


def main():
    global buyer_grp
    global dealer_grp
    global env

    (env, dealer_grp, buyer_grp) = set_up()

    if DEBUG2:
        print(env.__repr__())

    env()
    return 0


if __name__ == "__main__":
    main()
