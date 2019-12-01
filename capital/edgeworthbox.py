"""
A edgeworthbox model.
Places two groups of agents in the enviornment randomly
and moves them around randomly.
"""

from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import RED, BLUE
from indra.env import Env
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.utils import get_props

MODEL_NAME = "edgeworthbox"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_CAGENTS = 1
DEF_NUM_WAGENTS = 1
DEF_NUM_CHEESE = 4
DEF_NUM_WINE = 4

DEF_MAX_UTIL = max(DEF_NUM_CHEESE, DEF_NUM_WINE)

wine_group = None
cheese_group = None
env = None
max_util = DEF_MAX_UTIL

ACCEPT = 1
INADEQ = 0
REJECT = -1

answer_dict = {
    1: " accept",
    0: "'m indifferent about",
    -1: " reject"
}


# take a goods dict to string
def goods_to_str(goods):
    string = ', '.join([str(goods[k]["endow"]) + " " + str(k)
                       for k in goods.keys()])
    return string


# convert integer value of ans to string
def int_to_str(ans):
    return answer_dict[ans]


def gen_util_func(qty):
    return max_util - qty


def seek_a_trade(agent):
    nearby_agent = env.get_neighbor_of_groupX(agent,
                                              cheese_group,
                                              hood_size=4)
    if nearby_agent is not None:
        env.user.tell("I'm " + agent.name + " and I find "
                      + nearby_agent.name)
        # this_good is a dict
        # better to just give each agent at least 0
        # of every good to start
        for this_good in agent["goods"]:
            amt = 1
            while agent["goods"][this_good]["endow"] >= amt:
                ans = rec_offer(nearby_agent, this_good, amt, agent)
                env.user.tell("I'm " + agent.name
                              + ", I " + int_to_str(ans) + " this offer")
                if ans == ACCEPT or ans == REJECT:
                    break
                amt += 1

    env.user.tell("I'm " + agent.name
                  + ". I have " + goods_to_str(agent["goods"]))

    # return False means to move
    return False


def rec_offer(agent, his_good, his_amt, counterparty):
    """
    Receive an offer: we don't need to ever change my_amt
    in this function, because if the counter-party can't bid enough
    for a single unit, no trade is possible.
    """
    my_amt = 1
    gain = utility_delta(agent, his_good, his_amt)
    for my_good in agent["goods"]:
        if my_good != his_good and agent["goods"][my_good]["endow"] > 0:
            loss = -utility_delta(agent, my_good, -my_amt)
            env.user.tell("my good: " + my_good + "; his good: " + his_good
                          + ", I gain: " + str(gain) +
                          " and lose: " + str(loss))
            if gain > loss:
                if rec_reply(counterparty, his_good, his_amt, my_good, my_amt):
                    trade(agent, my_good, my_amt,
                          counterparty, his_good, his_amt)
                    return ACCEPT
                else:
                    return INADEQ
    return REJECT


def rec_reply(agent, my_good, my_amt, his_good, his_amt):
    gain = utility_delta(agent, his_good, his_amt)
    loss = utility_delta(agent, my_good, -my_amt)
    print(agent.name, "receiving a reply: gain = ",
          gain, "and loss =", loss)
    if gain > abs(loss):
        return ACCEPT
    else:
        return INADEQ


def trade(agent, my_good, my_amt, counterparty, his_good, his_amt):
    adj_add_good(agent, my_good, -my_amt)
    adj_add_good(agent, his_good, his_amt)
    adj_add_good(counterparty, his_good, -his_amt)
    adj_add_good(counterparty, my_good, my_amt)


def utility_delta(agent, good, change):
    """
    We are going to determine the utility of goods gained
    (amt is positive) or lost (amt is negative).
    """
    curr_good = agent["goods"][good]
    curr_amt = curr_good["endow"]
    curr_util = curr_good["util_func"](curr_amt)
    new_util = curr_good["util_func"](curr_amt + change)
    return ((new_util + curr_util) / 2) * change


def adj_add_good(agent, good, amt):
    agent["util"] += utility_delta(agent, good, amt)
    agent["goods"][good]["endow"] += amt


def create_wagent(name, i, props=None):
    start_wine = DEF_NUM_WINE
    if props is not None:
        start_wine = props.get('start_wine',
                               DEF_NUM_WINE)
    return Agent(name + str(i), action=seek_a_trade,
                 attrs={"goods": {"wine": {"endow": start_wine,
                                           "util_func": gen_util_func,
                                           "incr": 0},
                                  "cheese": {"endow": 0,
                                             "util_func": gen_util_func,
                                             "incr": 0}
                                  },
                        "util": 0,
                        "pre_trade_util": 0})


def create_cagent(name, i, props=None):
    start_cheese = DEF_NUM_CHEESE
    if props is not None:
        start_cheese = props.get('start_cheese',
                                 DEF_NUM_CHEESE)
    return Agent(name + str(i), action=seek_a_trade,
                 attrs={"goods": {"cheese": {"endow": start_cheese,
                                             "util_func": gen_util_func,
                                             "incr": 0},
                                  "wine": {"endow": 0,
                                           "util_func": gen_util_func,
                                           "incr": 0}},
                        "util": 0,
                        "pre_trade_util": 0})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    pa = get_props(MODEL_NAME, props, model_dir="capital")
    cheese_group = Composite("Cheese holders", {"color": BLUE},
                             member_creator=create_cagent,
                             props=pa,
                             num_members=pa.get('num_cagents',
                                                DEF_NUM_CAGENTS))
    wine_group = Composite("Wine holders", {"color": RED},
                           member_creator=create_wagent,
                           props=pa,
                           num_members=pa.get('num_wagents',
                                              DEF_NUM_WAGENTS))

    env = Env("env",
              height=pa.get('grid_height', DEF_HEIGHT),
              width=pa.get('grid_width', DEF_WIDTH),
              members=[cheese_group, wine_group],
              props=pa)

    start_cheese = 0
    start_wine = 0
    if pa is not None:
        start_cheese = pa.get('start_cheese',
                              DEF_NUM_CHEESE)
        start_wine = pa.get('start_wine',
                            DEF_NUM_WINE)
        max_util = max(start_cheese, start_wine)
    else:
        props_max_util = max(start_cheese, start_wine)
        max_util = max(props_max_util, DEF_MAX_UTIL)

    return (env, cheese_group, wine_group, max_util)


def main():
    global wine_group
    global cheese_group
    global env
    global max_util

    (env, cheese_group, wine_group, max_util) = set_up()

    if DEBUG2:
        env.user.tell(env.__repr__())

    env()
    return 0


if __name__ == "__main__":
    main()
