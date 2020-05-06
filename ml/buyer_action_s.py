import random
from indra.agent import Agent
from registry.registry import get_group, get_env, get_prop
from sympy.matrices import Matrix


DEF_NUM_BUYER = 10
DEF_NUM_SELLER = 10
MIN_CAR_LIFE = .2
MEDIUM_CAR_LIFE = 5
MAX_CAR_LIFE = 10
TEST_PERIOD = 100
BUYER_GRP = "Buyer_group"
DEALER_GRP = "Dealer_group"
strategies = {}


def matrix_reduction(agent):
    matrix = Matrix(agent["purchase_hist"])
    print(matrix.shape)


def positive_negative_relation(agent):
    pass


def s1_data_collection(agent):
    pass


def s2_data_collection(agent):
    pass


def is_dealer(agent):
    return get_group(DEALER_GRP).ismember(agent)


def is_mature(buyer):
    """
    check if buyer has enough experience
    to make its own decision
    """
    return buyer["maturity"] > get_prop('buyer_maturity', TEST_PERIOD)


def buy_w_experience(agent, dealer):
    ''' used for mature buyers.
    Supervised learnig predicting period'''
    print("I am an mature buyer!")
    res_score = agent["predicted_base_line"]
    for emoji in dealer["emojis"]:
        if emoji in agent["emoji_scores"]:
            res_score += agent["emoji_scores"][emoji]
    if res_score >= MEDIUM_CAR_LIFE:
        print("I think this dealer is trustworthy")
        agent["car_life"] = dealer["avg_car_life"]
    else:
        print("I think this dealer is unreliable")
    print("I predicted the car life is ",
          str(res_score),
          ", and the actual car life is: ",
          str(dealer["avg_car_life"]))
    return False


def buy_from_dealer(agent, dealer):
    ''' used for immature buyers.
    Supervised learnig data collection period'''
    print("I am an immature buyer. I got a car that last ",
          str(dealer["avg_car_life"]),
          ", and my dealer's emoji(s) is/are: ",
          str(dealer["emojis"]))
    curr_purchase = {"car_life": dealer["avg_car_life"],
                     "emojis": dealer["emojis"]}
    for emoji in dealer["emojis"]:
        if emoji in agent["emoji_experienced"]:
            length = len(agent["emoji_experienced"])
            agent["emoji_experienced"][emoji] = length
    agent["purchase_hist"].append(curr_purchase)
    agent["car_life"] = dealer["avg_car_life"]


def buyer_action(agent):
    """
    This functions lets buyer
    to decides whether wants to buy a car or not
    """
    print("_" * 20)
    print("Agent: " + agent.name)
    agent["maturity"] += 1
    my_dealer = get_env().get_neighbor_of_groupX(agent,
                                                 get_group(DEALER_GRP),
                                                 hood_size=15)
    if my_dealer is None:
        print("No dealers nearby.")
    elif not is_mature(agent):
        buy_from_dealer(agent, my_dealer)
    else:
        if(not agent["learnt"]):
            print("Investigating, buyer strategy =", agent["strategy"])
            print(agent["strategy"])
            print(type(agent["strategy"]))
            agent["strategy"]["data_collection"](agent)
            agent["strategy"]["func"](agent)
            agent["learnt"] = True
        buy_w_experience(agent, my_dealer)
    return False


def create_buyer_s(name, i, **kwargs):
    """
    Create a buyer agent.
    """
    return Agent(name + str(i),
                 action=buyer_action,
                 attrs={"maturity": 0,
                        "purchase_hist": [],  # list of purchase for learning
                        "emoji_experienced": {},  # emojis when immature
                        "learnt": False,
                        "strategy": strategies[random.choice(
                                               list(strategies.keys()))],
                        "car_life": 0,
                        "emoji_scores": {},
                        "predicted_base_line": MEDIUM_CAR_LIFE
                        })


strategies = {"s1": {"func": matrix_reduction,
                     "data_collection": s1_data_collection},
              "s2": {"func": positive_negative_relation,
                     "data_collection": s2_data_collection}}
