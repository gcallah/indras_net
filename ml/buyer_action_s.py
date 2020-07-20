from indra.agent import Agent
from registry.registry import get_group, get_env, get_prop
import numpy


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
    matrix, res = agent["strategy"]["data_collection"](agent)
    col = len(matrix[0])
    if col > len(matrix):  # not enought for matrix reduction
        return -1
    i = 0
    x = []
    while i < len(matrix) and len(x) == 0:
        A = numpy.array(matrix[i:i + col])
        b = numpy.array(res[i:i + col])
        try:
            x = numpy.linalg.solve(A, b)
        except numpy.linalg.LinAlgError:
            i += 1
    if len(x) == 0:
        return -1
    else:
        for emoji in agent["emoji_experienced"]:
            index = agent["emoji_experienced"][emoji]
            agent["emoji_scores"][emoji] = round(x[index][0], 2)
        agent["predicted_base_line"] = round(x[-1][0], 2)
        return 0


def correlation_detection(agent):
    ''' First calculate the avg difference of every single set of
    for every emoji, then, according to the length of emoji set, the
    shorter the set is, the stronger the emoji's correlation with
    current car life. The shortest emoji set's correlation is 1/2,
    the second is 1/4 and 1/8.... geometic series will add up to 1'''

    base_factor = .5
    emoji_dic = strategies["s2"]["data_collection"](agent)
    for emoji in emoji_dic:
        score = 0
        length = len(emoji_dic[emoji])
        for i in range(length):
            if len(emoji_dic[emoji][i]) == 0:
                emoji_dic[emoji][i] = 0
            else:
                res = sum(emoji_dic[emoji][i]) / length
                emoji_dic[emoji][i] = round(res, 2)
            if emoji_dic[emoji][i] != 0:
                score += base_factor * emoji_dic[emoji][i]
                base_factor *= .5
        left_fraction = 1 - base_factor
        score *= 1/left_fraction
        score = round(score, 2)
        agent["emoji_scores"][emoji] = score
        base_factor = .5
    return 0


def s1_data_collection(agent):
    '''Organize the potential matrix rows for the matrix reduction
    an dictionary of emoji with the corresponding purchase set it is in.
    If the emoji is presented in one of the purchase sets, it will be 1
    unpresented will be 0
    Example:  with the key "happy", the values will be list of lists
          happy sad angry base-line(always 1)
    x = [[  1    0    0      1    ]
         [  1    0    1      1    ]]
    y = [all the car lifes ...]'''
    x = []
    y = []
    for purchase in agent["purchase_hist"]:
        y.append([purchase["car_life"]])
        row = [0] * (len(agent["emoji_experienced"]))
        for emoji in purchase["emojis"]:
            row[agent["emoji_experienced"][emoji]] = 1
        row.append(1)  # stands for the constant base-line
        x.append(row)
    return (x, y)


def s2_data_collection(agent):
    '''Map every emoji to the (mean - scores) differences according to
    the length of the set that contains the emoji.
    Example, if there are two set {happy, clean} and {happy, tired, dirty}
    with corresponding scores 7 and 4, the data will be:
                 0     1  2    3
    {"happy": [[],[],[2],[-1]] ...}'''
    dic = {}
    for emoji in agent["emoji_experienced"]:
        dic[emoji] = [[] for x in range(len(agent["emoji_experienced"])+1)]
    for purchase in agent["purchase_hist"]:
        diff = purchase["car_life"] - MEDIUM_CAR_LIFE
        for emoji in purchase["emojis"]:
            dic[emoji][len(purchase["emojis"])].append(diff)
    return dic


def is_dealer(agent):
    return get_group(DEALER_GRP).ismember(agent)


def is_mature(buyer):
    '''check if buyer has enough experience
    to make its own decision'''
    return buyer["maturity"] > get_prop('buyer_maturity', TEST_PERIOD)


def buy_w_experience(agent, dealer):
    ''' used for mature buyers.
    Supervised learnig predicting period'''
    print("I am a mature buyer!")
    res_score = agent["predicted_base_line"]
    for emoji in dealer["emojis"]:
        if emoji in agent["emoji_scores"]:
            res_score += agent["emoji_scores"][emoji]
    if res_score >= MEDIUM_CAR_LIFE:
        agent["matured_car_num"] += 1
        agent["matured_car_lives"] += dealer["avg_car_life"]
        agent["avg"] = agent["matured_car_lives"]/agent["matured_car_num"]
        agent["avg"] = round(agent["avg"], 2)
    print("I have bought", agent["matured_car_num"], "cars")
    print("My current average car life is", agent["avg"])
    return False


def buy_from_dealer(agent, dealer):
    ''' used for immature buyers.
    Supervised learnig data collection period'''
    print("I am an immature buyer. \nI got a car life",
          str(dealer["avg_car_life"]),
          ", \nMy dealer's emoji(s) is/are: ",
          str(dealer["emojis"]))
    curr_purchase = {"car_life": dealer["avg_car_life"],
                     "emojis": dealer["emojis"]}
    for emoji in dealer["emojis"]:
        if emoji not in agent["emoji_experienced"]:
            length = len(agent["emoji_experienced"])
            agent["emoji_experienced"][emoji] = length
    agent["purchase_hist"].append(curr_purchase)
    agent["car_life"] = dealer["avg_car_life"]


def buyer_action(agent, **kwargs):
    '''This functions lets buyer
    to decides whether wants to buy a car or not'''
    print("_" * 20)
    print("Agent: " + agent.name)
    agent["maturity"] += 1
    my_dealer = get_env().get_neighbor_of_groupX(agent,
                                                 get_group(DEALER_GRP),
                                                 hood_size=300)
    if my_dealer is None:
        print("No dealers nearby.")
    elif not is_mature(agent):
        buy_from_dealer(agent, my_dealer)
    else:
        if(not agent["learnt"]):
            success = agent["strategy"]["func"](agent)
            if success == -1:
                strategies["s2"]["func"](agent)
            agent["learnt"] = True
        buy_w_experience(agent, my_dealer)
    return False


def create_buyer_s(name, i, **kwargs):
    '''Create a buyer agent.'''
    return Agent(name + str(i),
                 action=buyer_action,
                 attrs={"maturity": 0,
                        "purchase_hist": [],  # list of purchase for learning
                        "emoji_experienced": {},  # emojis when immature
                        "learnt": False,
                        "strategy": strategies["s1"],
                        "car_life": 0,
                        "emoji_scores": {},
                        "predicted_base_line": MEDIUM_CAR_LIFE,
                        "matured_car_num": 0,
                        "matured_car_lives": 0,
                        "avg": 0
                        })


strategies = {"s1": {"func": matrix_reduction,
                     "data_collection": s1_data_collection},
              "s2": {"func": correlation_detection,
                     "data_collection": s2_data_collection}}
