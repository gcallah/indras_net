'''
Ava's Agent
'''
from indra.agent import Agent
from registry.registry import get_env, get_group, get_prop

MODEL_NAME = "ava_agent"
TRAINING_PERIOD = 100
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
    return buyer["maturality"] > get_prop('buyer_maturity', TRAINING_PERIOD)


def cal_from_buyer(buyer):  # testcase done
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
    if not is_mature(agent):
        print("I am an immature buyer.")
        print("I got a car life",
              str(my_dealer["avg_car_life"]),
              ", \nMy dealer's emoji(s) is/are: ",
              str(my_dealer["emojis"]))


def training_action(agent):
    print("_" * 20)
    print("Agent: " + agent.name)
    my_dealer = get_env().get_neighbor_of_groupX(agent,
                                                 get_group(DEALER_GRP),
                                                 hood_size=4)
    if my_dealer is None:
        print("No dealers nearby.")
    else:
        # unmature buyer learning
        buy_from_dealer(agent, my_dealer)
        # separate out calculations
        cal_from_buyer(agent)
    return False


def evaluate_dealer_emoji(buyer, dealer):
    # info buyer received from dealer
    received_emojis = dealer["emojis"]
    received_car = dealer["avg_car_life"]
    num_emojis = len(received_emojis)
    # calculate average life associate with emoji
    buyer_emojis_table = buyer["emoji_life_avg"]
    judge_car_life = 0
    for emoji in received_emojis:
        judge_car_life += buyer_emojis_table[emoji]
    judge_car_life /= num_emojis
    is_good_buy = received_car > judge_car_life
    return is_good_buy


def strategic_action(agent):
    my_dealer = get_env().get_neighbor_of_groupX(agent,
                                                 get_group(DEALER_GRP),
                                                 hood_size=4)
    if my_dealer is None:
        print("No dealers nearby.")
    else:
        # evaluate dealer and buy or not
        buy_flag = evaluate_dealer_emoji(agent, my_dealer)
        # predict if received emoji will give a bad car life
        if buy_flag:
            # store info on car life
            received_car_life = my_dealer["avg_car_life"]
            agent["strategy_car_life"].append(received_car_life)
            buy_from_dealer(agent, my_dealer)
    return False


def buyer_action(agent):  # how to write this testcase
    """
    This functions lets buyer
    to decides whether wants to buy a car or not
    """
    print("_" * 20)
    print("Agent: " + agent.name)
    if not is_mature(agent):
        training_action(agent)
    else:
        strategic_action(agent)
    car_lifes = agent["strategy_car_life"]
    if len(car_lifes) != 0:
        car_life_avg = sum(car_lifes) / len(car_lifes)
        print("I am a mature buyer!")
        print("I have bought", len(car_lifes), "cars")
        print("My average car life is", round(car_life_avg, 2))
    return False


def create_buyer_a(name, i, **kwargs):  # testcase done
    """
    Create an agent.
    """
    return Agent(name + str(i),
                 action=buyer_action,
                 attrs={"car_life": None,
                        "emoji_carlife_assoc": {},
                        "emoji_life_avg": {},
                        "maturality": 0,
                        "strategy_car_life": []
                        })
