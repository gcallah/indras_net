"""
A used cars model.
Places two groups of agents in the enviornment randomly
and moves them around randomly.
Stage 1
Two goals:
1. Associate Emoji with car life buyer get
2. Associate buyer with all past interaction with particular dealer
"""

import random

from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import RED, BLUE
from indra.env import Env
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.utils import get_props

MODEL_NAME = "used_cars"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_BLUE = 10
DEF_NUM_RED = 10

MIN_CAR_LIFE = 1
MAX_BAD_CAR_LIFE = 4
MIN_GOOD_CAR_LIFE = 5
MAX_CAR_LIFE = 5

MATURE_BOUND = 100

MEDIUM_CAR_LIFE = (MIN_CAR_LIFE + MAX_CAR_LIFE) // 2

# categorized emojis reflects trend of dealer's respond
POS_EMOJIS = ["smiley", "laughing", "relaxing", "wink"]
NEG_EMOJIS = ["unnatural", "ambiguous", "hesitate", "eye rolling"]
CHARACTERISTIC = ["good", "bad"]

DEALERS = "Dealers"

buyer_grp = None
dealer_grp = None
car_market = None


def bought_info(agent, dealer):
    '''
    Debug messages to show dealer's informationsss
    '''
    msg = "My dealer is: " + dealer.name
    msg += "\nReceived a car with a life of " + str(agent["car_life"])
    msg += "\nMy dealer " + dealer.name
    msg += " has an avg car life of " + str(dealer["avg_car_life_sold"])
    msg += ". And he/she sold " + str(dealer["num_sales"]) + " cars."
    msg += "\nMy dealer " + dealer.name
    msg += " shows an emoji of " + agent["interaction_res"]
    return msg


def is_dealer(agent, dealer_grp):  # testcase done
    return dealer_grp.ismember(agent)


def get_car_life(dealer):  # testcase done
    '''
    Display dealer's information and car
    for debug purpose
    '''
    print("Getting car from dealer", dealer)
    return dealer["curr_car_life"]


def get_dealer_car(dealer_characteristc):  # testcase done
    '''
    Based on dealer's characteristics
    this function returns a random car life to dealer object
    to sell to the buyer
    '''
    if dealer_characteristc == "good":
        return random.randint(MIN_GOOD_CAR_LIFE, MAX_CAR_LIFE)
    else:  # dealer characteristic == bad
        return random.randint(MIN_CAR_LIFE, MAX_BAD_CAR_LIFE)


def dealer_action(agent):
    '''
    Display debug statements
    '''
    car_market.user.tell("I'm " + agent.name + " and I'm a dealer.")
    dealer_characteristic = get_dealer_characteristic()
    agent["dealer_characteristic"] = dealer_characteristic
    agent["emoji_used"] = get_dealer_emoji(dealer_characteristic)
    agent["curr_car_life"] = get_dealer_car(dealer_characteristic)
    # return False means to move
    return False


def get_dealer_characteristic():
    return CHARACTERISTIC[random.randint(0, 1)]


def set_emoji_indicator(agent):
    '''
    when a buyer becomes mature
    he/she can judge based on their past buying experience
    '''
    mp = agent["emoji_life_avg"]
    for i in mp:
        if mp[i] >= MIN_GOOD_CAR_LIFE:
            agent["emoji_indicator"] = "good"
        else:
            agent["emoji_indicator"] = "bad"


def get_dealer_emoji(dealer_characteristic):
    '''
    This function returns a random emoji based on
    dealer's characteristics
    '''
    if dealer_characteristic == "good":
        return POS_EMOJIS[random.randint(0, 3)]
    else:  # dealer characteristic == bad
        return NEG_EMOJIS[random.randint(0, 3)]


def update_dealer_sale(dealer, new_car_life):
    '''
    A helper function to update attributes in dealer agent
    When buyer and dealer interaction happens
    '''
    dealer["num_sales"] += 1
    if dealer["avg_car_life_sold"] is None:
        dealer["avg_car_life_sold"] = new_car_life
    else:
        avg_car_life = (dealer["avg_car_life_sold"]
                        + new_car_life) / dealer["num_sales"]
        dealer["avg_car_life_sold"] = round(avg_car_life, 2)


def is_mature(agent):
    '''
    check if buyer has enough experience
    to make its own decision
    '''
    return MATURE_BOUND <= len(agent["dealer_hist"])


def is_credible(dealer, buyer):
    '''
    See if this dealer looks good... right now, only useful for
    mature buyers.
    '''
    if is_mature(buyer):
        set_emoji_indicator(buyer)
        # judge base on buyer's own past experience
        received_emoji = dealer["emoji_used"]
        past_exp = buyer["emoji_indicator"]
        if buyer[received_emoji] == "good":
            return emoji_life[received_emoji]
    # immature buyers are gullible!
    return True


def cal_avg_life(agent):
    '''
    Each emoji associate with list of car lifes
    this function calculates average car life of a emoji
    and map it to the corresponding emoji
    '''
    assoc = agent["emoji_carlife_assoc"]
    emo_life_avg = agent["emoji_life_avg"]
    for key in assoc:
        num = len(assoc[key])
        avg = sum(assoc[key]) / num
        emo_life_avg[key] = avg


def buy_from_dealer(agent, my_dealer):
    '''
    When buyer buys a car from the dealer
    Update all dealer and buyer's attributes
    '''
    agent["has_car"] = True
    agent["dealer_hist"].append(my_dealer)
    rec_carlife = get_car_life(my_dealer)
    agent["car_life"] = rec_carlife
    rec_emoji = my_dealer["emoji_used"]
    agent["interaction_res"] = rec_emoji
    # map each emoji associate with different
    # car lives for ML prediction
    assoc = agent["emoji_carlife_assoc"]
    if rec_emoji not in assoc:
        assoc[rec_emoji] = [rec_carlife]
    else:
        assoc[rec_emoji].append(rec_carlife)
    print("My emoji car association:", assoc)
    cal_avg_life(agent)
    update_dealer_sale(my_dealer, rec_carlife)
    print(bought_info(agent, my_dealer))


def buyer_action(agent):  # how to write this testcase
    '''
    This functions lets buyer
    to decides whether wants to buy a car or not
    '''
    print("_" * 20)
    print("Agent: " + agent.name)
    agent["age"] += 1
    if not agent["has_car"]:
        my_dealer = car_market.get_neighbor_of_groupX(agent,
                                                      dealer_grp,
                                                      hood_size=4)
        if my_dealer is None:
            print("No dealers nearby.")
        elif is_credible(my_dealer, agent):
            buy_from_dealer(agent, my_dealer)
        else:
            print("I found a rotten dealer: ", str(my_dealer))
    else:
        print("I have a car!")
        agent["car_life"] -= 1
        if agent["car_life"] <= 0:
            agent["has_car"] = False
    # return False means to move
    return False


def create_dealer(name, i, props=None):  # testcase done
    """
    Create an agent.
    """
    return Agent(name + str(i),
                 action=dealer_action,
                 attrs={"num_sales": 0,
                        "avg_car_life_sold": None,
                        "curr_car_life": 0,
                        "num_completed_services": 0,
                        "emoji_used": None,
                        "dealer_characteristic": None,
                        "respond_to_return": False,
                        "return_rate": 0
                        })


def create_buyer(name, i, props=None):  # testcase done
    """
    Create an agent.
    """
    return Agent(name + str(i),
                 action=buyer_action,
                 attrs={"has_car": False,
                        "car_life": None,
                        "interaction_res": None,
                        "age": 0,
                        "dealer_hist": [],
                        "emoji_carlife_assoc": {},
                        "emoji_life_avg": {},
                        "emoji_indicator": {},
                        "want_to_return": False
                        })


def set_up(props=None):  # testcase done
    """
    A func to set up run that can also be used by test code.
    """
    pa = get_props(MODEL_NAME, props, model_dir="ml")
    dealer_grp = Composite("Dealers", {"color": BLUE},
                           member_creator=create_dealer,
                           num_members=pa.get('num_sellers', DEF_NUM_BLUE))
    buyer_grp = Composite("Buyers", {"color": RED},
                          member_creator=create_buyer,
                          num_members=pa.get('num_buyers', DEF_NUM_RED))

    car_market = Env("Car market",
                     height=pa.get('grid_height', DEF_HEIGHT),
                     width=pa.get('grid_width', DEF_WIDTH),
                     members=[dealer_grp, buyer_grp],
                     props=pa)

    return (car_market, dealer_grp, buyer_grp)


def main():
    global buyer_grp
    global dealer_grp
    global car_market

    (car_market, dealer_grp, buyer_grp) = set_up()

    if DEBUG2:
        print(car_market.__repr__())

    car_market()
    return 0


if __name__ == "__main__":
    main()
