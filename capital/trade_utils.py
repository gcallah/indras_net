"""
This file contains general functions useful in trading goods.
"""
from indra.user import user_tell
from indra.registry import get_env
import random

ACCEPT = 1
INADEQ = 0
REJECT = -1

answer_dict = {
    1: "I accept",
    0: "I'm indifferent about",
    -1: "I reject"
}

DEF_MAX_UTIL = 20  # this should be set by the models that use this module

max_util = DEF_MAX_UTIL


def initial_endowment(trader, avail_goods):
    """
    This function is going to pick a good at random, and give the
    trader all of it, by default. We will write partial distributions
    later.
    """
    # goods will be a dictionary: {"good_name": {"amt_vailable": amt, ...}
    # pick an item at random
    # stick all of it in trader's goods dictionar
    rand_good = random.choice(avail_goods.keys())
    # get a random good_nam
    trader["goods"][rand_good]["endow"] = (
        avail_goods[rand_good]["amt_vailable"]
    )


def goods_to_str(goods):
    """
    take a goods dict to string
    """
    string = ', '.join([str(goods[k]["endow"]) + " " + str(k)
                       for k in goods.keys()])
    return string


def answer_to_str(ans):
    """
    convert integer value of ans to string
    """
    return answer_dict[ans]


def gen_util_func(qty):
    return max_util - qty


def seek_a_trade(agent):
    nearby_agent = get_env().get_neighbor_of_groupX(agent,
                                                    agent["trades_with"],
                                                    hood_size=4)
    if nearby_agent is not None:
        user_tell("I'm " + agent.name + " and I find "
                  + nearby_agent.name)
        # this_good is a dict
        # better to just give each agent at least 0
        # of every good to start
        for this_good in agent["goods"]:
            amt = 1
            while agent["goods"][this_good]["endow"] >= amt:
                ans = rec_offer(nearby_agent, this_good, amt, agent)
                user_tell("I'm " + agent.name
                          + ", " + answer_to_str(ans) + " this offer")
                if ans == ACCEPT or ans == REJECT:
                    break
                amt += 1

    user_tell("I'm " + agent.name
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
            # user_tell("my good: " + my_good + "; his good: " + his_good
            #           + ", I gain: " + str(gain) +
            #           " and lose: " + str(loss))
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
          gain, "and loss =", abs(loss))
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
