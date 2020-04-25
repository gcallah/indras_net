'''
Goal:
    1. see emojis (from Prof); then see rating factor
    2. Multi regression line for ML
    3. contest period - new set of dealers following the
    same rules;
'''
import random
import sys

from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import RED, BLUE
from indra.env import Env
from indra.space import DEF_HEIGHT, DEF_WIDTH
from registry.registry import get_env, get_group, get_prop
from indra.utils import init_props
from ml.dealer_factory import generate_dealer

MODEL_NAME = "used_cars"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_BLUE = 10
DEF_NUM_RED = 10

MATURE_BOUND = 100

BUYER_GRP = "Buyer_group"
DEALER_GRP = "Dealer_group"
strategies = {}


def buy_till_1bad(buyer, dealer):
    '''
    mature buyers take cars from good dealer til get 1 bad car
    '''
    # info buyer received from dealer
    received_car_life = dealer["avg_car_life"]
    received_emojis = dealer["emojis"]
    num_emojis = len(received_emojis)
    # emoji, carlife from buyer's history
    buyer_emojis_table = buyer["emoji_life_avg"]
    judge_car_life = 0
    for emoji in received_emojis:
        judge_car_life += buyer_emojis_table[emoji]
    judge_car_life /= num_emojis
    # judge if received emoji will give a bad car
    if received_car_life > judge_car_life:
        # update strategy s1's car life
        strategies["s1"]["car_life"].append(received_car_life)
        buy_from_dealer(buyer, dealer)
    else:
        buyer["dealer"] = None


# different strategies
strategies = {"s1": {"func": buy_till_1bad,
                     "car_life": []
                     }
              }


def is_dealer(agent):  # testcase need changes
    return get_group(DEALER_GRP).ismember(agent)


def get_car_life(dealer):  # testcase done
    """
    Display dealer's information and car
    for debug purpose
    """
    print("Getting car from dealer", dealer)
    return dealer["curr_car_life"]


def is_mature(buyer):  # testcase done
    """
    check if buyer has enough experience
    to make its own decision
    """
    return buyer["maturality"] > MATURE_BOUND


def cal_avg_life(buyer):  # testcase done
    """
    Each emoji associate with list of car lifes
    this function calculates average car life of a emoji
    and map it to the corresponding emoji
    """
    assoc = buyer["emoji_carlife_assoc"]
    emo_life_avg = buyer["emoji_life_avg"]
    for key in assoc:
        num = len(assoc[key])
        avg = round(sum(assoc[key]) / num, 2)
        emo_life_avg[key] = avg


def buy_from_dealer(agent, my_dealer):
    """
    When buyer buys a car from the dealer
    Update all dealer and buyer's attributes
    """
    agent["maturality"] += 1
    agent["has_car"] = True
    received_car_life = my_dealer["avg_car_life"]
    agent["car_life"] = received_car_life
    received_emojis = my_dealer["emojis"]
    # map each emoji to a carlife in the table
    assoc = agent["emoji_carlife_assoc"]
    for emoji in received_emojis:
        if emoji not in assoc:
            assoc[emoji] = [received_car_life]
        else:
            assoc[emoji].append(received_car_life)
        print("My emoji car association:", assoc)
        cal_avg_life(agent)


def has_car_update(agent):
    print("I have a car!")
    agent["car_life"] -= 1
    if agent["car_life"] <= 0:
        agent["has_car"] = False


def buyer_action(agent):  # how to write this testcase
    """
    This functions lets buyer
    to decides whether wants to buy a car or not
    """
    print("_" * 20)
    print("Agent: " + agent.name)
    if not agent["has_car"]:
        my_dealer = get_env().get_neighbor_of_groupX(agent,
                                                     get_group(DEALER_GRP),
                                                     hood_size=4)
        if my_dealer is None:
            print("No dealers nearby.")
        elif not is_mature(agent):
            # unmature buyer learning
            buy_from_dealer(agent, my_dealer)
        else:
            # mature buyer strategy
            agent["strategy"]["func"]()
            print("Agent strategy =", agent["strategy"])
    else:
        # return False means to move
        has_car_update(agent)
    return False


def create_dealer(name, i, props=None):  # testcase done
    """
    Create an agent.
    """
    return generate_dealer()


def create_buyer(name, i, props=None):  # testcase done
    """
    Create an agent.
    """
    return Agent(name + str(i),
                 action=buyer_action,
                 attrs={"has_car": False,
                        "dealer": None,
                        "car_life": None,
                        "emoji_carlife_assoc": {},
                        "emoji_life_avg": {},
                        "maturality": 0,
                        "strategy": random.choice(list(strategies.keys()))
                        })


def set_up(num_dealers, props=None):  # testcase???
    """
    A func to set up run that can also be used by test code.
    """
    init_props(MODEL_NAME, props)
    group = []
    group.append(Composite(DEALER_GRP, {"color": BLUE},
                           member_creator=create_dealer,
                           num_members=num_dealers))
    group.append(Composite(BUYER_GRP, {"color": RED},
                           member_creator=create_buyer,
                           num_members=get_prop('num_buyers', DEF_NUM_RED)))

    Env("Car market",
        height=get_prop('grid_height', DEF_HEIGHT),
        width=get_prop('grid_width', DEF_WIDTH),
        members=group)


def main():
    num_dealers = int(sys.argv[1])
    if num_dealers == 0:
        num_dealers = 6
    set_up(num_dealers)
    get_env()()
    return 0


if __name__ == "__main__":
    main()
