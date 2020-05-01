'''
Ava's Agent
'''
import random
from indra.agent import Agent
from registry.registry import get_env, get_group

MODEL_NAME = "ava_agent"
TRAINING_PERIOD = 100
strategies = {}
DEALER_GRP = "Dealer_group"


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
    return buyer["maturality"] > TRAINING_PERIOD


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


def training_buyers(agent):
    while not is_mature(agent):
        print("_" * 20)
        print("Agent: " + agent.name)
        if not agent["has_car"]:
            my_dealer = get_env().get_neighbor_of_groupX(agent,
                                                         get_group(DEALER_GRP),
                                                         hood_size=4)
            if my_dealer is None:
                print("No dealers nearby.")
            else:
                # unmature buyer learning
                buy_from_dealer(agent, my_dealer)
        else:
            # return False means to move
            has_car_update(agent)
    return False


def learn_with_strategy(agent):
    '''
    mature buyers take cars from good dealer til get 1 bad car
    '''
    bad_flag = False
    while not bad_flag:
        print("_" * 20)
        print("Agent: " + agent.name)
        if not agent["has_car"]:
            my_dealer = get_env().get_neighbor_of_groupX(agent,
                                                         get_group(DEALER_GRP),
                                                         hood_size=4)
            if my_dealer is None:
                print("No dealers nearby.")
            else:
                # info buyer received from dealer
                received_car_life = my_dealer["avg_car_life"]
                received_emojis = my_dealer["emojis"]
                num_emojis = len(received_emojis)
                # calculate average life associate with emoji
                buyer_emojis_table = agent["emoji_life_avg"]
                judge_car_life = 0
                for emoji in received_emojis:
                    judge_car_life += buyer_emojis_table[emoji]
                judge_car_life /= num_emojis
                # judge if received emoji will give a bad car
                if received_car_life > judge_car_life:
                    # update strategy s1's car life
                    strategies["s1"]["car_life"].append(received_car_life)
                    buy_from_dealer(agent, my_dealer)
                else:
                    bad_flag = True
        else:
            # return False means to move
            has_car_update(agent)
    return False


# different strategies
strategies = {"s1": {"func": learn_with_strategy,
                     "car_life": []
                     }
              }


def buyer_action(agent):  # how to write this testcase
    """
    This functions lets buyer
    to decides whether wants to buy a car or not
    """
    if not is_mature(agent):
        training_buyers(agent)
    else:
        learn_with_strategy(agent)
    life_from_stategy = strategies["car_life"]
    print("Car life received from using strategy:", life_from_stategy)
    print("Avergae life is", life_from_stategy/len(life_from_stategy))
    return False


def create_buyer_a(name, i, props=None):  # testcase done
    """
    Create an agent.
    """
    return Agent(name + str(i),
                 action=buyer_action,
                 attrs={"has_car": False,
                        "car_life": None,
                        "emoji_carlife_assoc": {},
                        "emoji_life_avg": {},
                        "maturality": 0,
                        "strategy": random.choice(list(strategies.keys()))
                        })
