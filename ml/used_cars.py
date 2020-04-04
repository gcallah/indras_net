'''
Goal:
    1. training period:
    - make a list of good dealer and bad dealer
    - buy from anyone;
    - add dealer ratings to attribute
    - agent try to multilinear regression
    2. see emojis (from Prof); then see rating factor
    3. Multi regression line for ML
    4. Bank and sugeron examples doing machine learning
    on training - then on test set.
    5. contest period - new set of dealers following the
    same rules;
'''
import random
import sys

from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import RED, BLUE
from indra.env import Env
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.registry import get_env, get_group, get_prop
from indra.utils import init_props

MODEL_NAME = "used_cars"
GENERATOR_NAME = "dealer_car_generator"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_BLUE = 10
DEF_NUM_RED = 10

MIN_CAR_LIFE = 1
MAX_BAD_CAR_LIFE = 4
MIN_GOOD_CAR_LIFE = 3
MAX_CAR_LIFE = 5

MATURE_BOUND = 100

MEDIUM_CAR_LIFE = (MIN_CAR_LIFE + MAX_CAR_LIFE) // 2

# categorized emojis reflects trend of dealer's respond
POS_EMOJIS = ["smiley", "laughing", "relaxing", "wink"]
NEG_EMOJIS = ["unnatural", "ambiguous", "hesitate", "eye rolling"]
CHARACTERISTIC = ["good", "bad"]

BUYER_GRP = "Buyer_group"
DEALER_GRP = "Dealer_group"
strategies = {}


def buy_till_1bad(buyer, dealer):  # testcase needed!
    '''
    mature buyers take cars from good dealer til get 1 bad car
    '''
    buy_from_dealer(buyer, dealer)
    curr_dealer_life = dealer["curr_car_life"]
    # update strategy s1's car life
    strategies["s1"]["car_life"].append(curr_dealer_life)
    # bad car life is define as less than buyer's avg car life
    while curr_dealer_life >= MEDIUM_CAR_LIFE:
        buy_from_dealer(buyer, dealer)
        strategies["s1"]["car_life"].append(curr_dealer_life)
        curr_dealer_life = dealer["curr_car_life"]


def buy_till_2bad(buyer, dealer):  # testcase needed!
    '''mature buyers take cars from good dealer til get 2 bad car'''
    buy_from_dealer(buyer, dealer)
    curr_dealer_life = dealer["curr_car_life"]
    # update strategy s2's car life
    strategies["s2"]["car_life"].append(curr_dealer_life)
    # buyer's own car life history
    dealer_emj = dealer["emoji_used"]
    buyer_emj_lst = buyer["emoji_life_avg"]
    curr_buyer_life = buyer_emj_lst[dealer_emj]
    bad_car_count = 0
    # bad car define as less than buyer's avg car life
    while bad_car_count < 2:
        if curr_dealer_life >= curr_buyer_life:
            bad_car_count += 1
        # update buyer and dealer info
        buy_from_dealer(buyer, dealer)
        curr_dealer_life = dealer["curr_car_life"]
        # update strategy s2's car life
        strategies["s2"]["car_life"].append(curr_dealer_life)
        # update buyer's own car life history
        dealer_emj = dealer["emoji_used"]
        buyer_emj_lst = buyer["emoji_life_avg"]
        curr_buyer_life = buyer_emj_lst[dealer_emj]


def buy_till_3bad(buyer, dealer):  # testcases needed!
    '''mature buyers take cars from good dealer til get 3 bad car'''
    buy_from_dealer(buyer, dealer)
    curr_dealer_life = dealer["curr_car_life"]
    # update strategy s3's car life
    strategies["s3"]["car_life"].append(curr_dealer_life)
    # buyer's own car life history
    dealer_emj = dealer["emoji_used"]
    buyer_emj_lst = buyer["emoji_life_avg"]
    curr_buyer_life = buyer_emj_lst[dealer_emj]
    bad_car_count = 0
    # bad car define as less than buyer's avg car life
    while bad_car_count < 3:
        if curr_dealer_life >= curr_buyer_life:
            bad_car_count += 1
        # update buyer and dealer info
        buy_from_dealer(buyer, dealer)
        curr_dealer_life = dealer["curr_car_life"]
        # update strategy s3's car life
        strategies["s3"]["car_life"].append(curr_dealer_life)
        # update buyer's own car life history
        dealer_emj = dealer["emoji_used"]
        buyer_emj_lst = buyer["emoji_life_avg"]
        curr_buyer_life = buyer_emj_lst[dealer_emj]


# different strategies
strategies = {"s1": {"func": buy_till_1bad,
                     "car_life": []
                     },
              "s2": {"func": buy_till_2bad,
                     "car_life": []
                     },
              "s3": {"func": buy_till_3bad,
                     "car_life": []
                     }
              }


def get_car_life_json(json_file, dealer_name):  # testcase needed!
    """
    get car life randomly from a json file
    """
    emoji_dic = json_file[dealer_name]
    selected_emoji = list(emoji_dic.keys())[0]
    avg_life = emoji_dic[selected_emoji]
    selected_avg_life = list(avg_life.keys())[0]
    life_lst = avg_life[selected_avg_life]
    selected_index = random.randint(0, len(life_lst) - 1)
    return life_lst[selected_index]


def get_emoji_json(json_file, dealer_name):  # testcase needed!
    """
    get dealer's from a json file
    """
    emoji_dic = json_file[dealer_name]
    selected_emoji = list(emoji_dic.keys())[0]
    return selected_emoji


def map_json_to_attributes(json_file, dealer_name):
    """
    map every information from json file to a dealer's
    existing attributes
    """
    emoji_dic = json_file[dealer_name]
    selected_emoji = list(emoji_dic.keys())[0]
    # need to be verified here: Is dealer_name an agent
    if selected_emoji in POS_EMOJIS:
        dealer_name["dealer_characteristic"] = "good"
    else:
        dealer_name["dealer_characteristic"] = "bad"
    dealer_name["emoji_used"] = selected_emoji
    avg_life = emoji_dic[selected_emoji]
    selected_avg_life = list(avg_life.keys())[0]
    # need to be verified
    dealer_name["avg_car_life_sold"] = selected_avg_life
    life_lst = avg_life[selected_avg_life]
    dealer_name["num_sales"] = len(life_lst)


def is_dealer(agent):  # testcase need changes
    return get_group(DEALER_GRP).ismember(agent)


def get_car_life(dealer):  # testcase done
    """
    Display dealer's information and car
    for debug purpose
    """
    print("Getting car from dealer", dealer)
    return dealer["curr_car_life"]


def get_dealer_car(dealer_characteristc):  # testcase done
    """
    Based on dealer's characteristics
    this function returns a random car life to dealer object
    to sell to the buyer
    """
    if dealer_characteristc == "good":
        return random.randint(MIN_GOOD_CAR_LIFE, MAX_CAR_LIFE)
    else:  # dealer characteristic == bad
        return random.randint(MIN_CAR_LIFE, MAX_BAD_CAR_LIFE)


def dealer_action(dealer):  # testcase??
    """
    Display debug statements
    """
    get_env().user.tell("I'm " + dealer.name + " and I'm a dealer.")
    dealer_characteristic = get_dealer_characteristic()
    dealer["dealer_characteristic"] = dealer_characteristic
    dealer["emoji_used"] = get_dealer_emoji(dealer_characteristic)
    dealer["curr_car_life"] = get_dealer_car(dealer_characteristic)
    # return False means to move
    return False


def get_dealer_characteristic():  # testcase done
    return CHARACTERISTIC[random.randint(0, 1)]


def set_emoji_indicator(buyer):
    """
    when a buyer becomes mature
    he/she can judge based on their
     past buying experience
    """
    mp = buyer["emoji_life_avg"]
    for key in mp:
        if mp[key] >= MIN_GOOD_CAR_LIFE:
            buyer["emoji_indicator"][key] = "good"
        else:
            buyer["emoji_indicator"][key] = "bad"


def get_dealer_emoji(dealer_characteristic):  # testcase done
    """
    return random emojis from two categories.
    depending on dealer characteristics
    """
    if dealer_characteristic == "good":
        return POS_EMOJIS[random.randint(0, 3)]
    else:
        return NEG_EMOJIS[random.randint(0, 3)]


def update_dealer_sale(dealer, new_car_life):  # testcase done
    """
    A helper function to update attributes in dealer agent
    When buyer and dealer interaction happens
    """
    dealer["num_sales"] += 1
    if dealer["avg_car_life_sold"] is None:
        dealer["avg_car_life_sold"] = new_car_life
    else:
        avg_car_life = (dealer["avg_car_life_sold"]
                        + new_car_life) / dealer["num_sales"]
        dealer["avg_car_life_sold"] = round(avg_car_life, 2)


def is_mature(buyer):  # testcase done
    """
    check if buyer has enough experience
    to make its own decision
    """
    if not buyer["can_mature"]:
        if MATURE_BOUND <= len(buyer["dealer_hist"]):
            buyer["can_mature"] = True
            return True
        else:
            return False
    else:
        return True


def is_credible(dealer, buyer):  # testcase done
    """
    See if this dealer looks good... right now, only useful for
    mature buyers.
    """
    if is_mature(buyer):
        set_emoji_indicator(buyer)
        # judge base on buyer's own past experience
        received_emoji = dealer["emoji_used"]
        past_exp = buyer["emoji_indicator"]
        judgement = past_exp[received_emoji]
        # if buyer's judgement is not good
        # make him immature and learn more data
        if judgement != dealer["dealer_characteristic"]:
            buyer["can_mature"] = False
        return judgement == "good"
    # immature buyers are gullible!
    return True


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


def buyer_action(agent):  # how to write this testcase
    """
    This functions lets buyer
    to decides whether wants to buy a car or not
    """
    print("_" * 20)
    print("Agent: " + agent.name)
    agent["age"] += 1
    if not agent["has_car"]:
        my_dealer = get_env().get_neighbor_of_groupX(agent,
                                                     get_group(DEALER_GRP),
                                                     hood_size=4)
        if my_dealer is None:
            print("No dealers nearby.")
        elif is_credible(my_dealer, agent):
            buy_from_dealer(agent, my_dealer)
        else:
            print("I found a rotten dealer: ", str(my_dealer))
    else:
        # return False means to move
        print("I have a car!")
        agent["car_life"] -= 1
        if agent["car_life"] <= 0:
            agent["has_car"] = False
    # call strategy function to update the data
    agent["strategy"]["func"]()
    print("Agent strategy =", agent["strategy"])
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
                        "dealer_characteristic": None
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
                        "can_mature": False,
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
    if len(sys.argv) < 2:
        print("datafile name missing")
        print("USAGE: used_cars.py [datafile]")
        exit(1)
    pathname = sys.argv[1]
    filename = pathname.split("/")[1]
    info = filename.split("_")[0]
    num_dealers = int(info)
    set_up(num_dealers)

    get_env()()
    return 0


if __name__ == "__main__":
    main()
