"""
This file contains general functions useful in trading goods.
"""
from indra.user import user_debug
from indra.registry import get_env
import random

ACCEPT = 1
INADEQ = 0
REJECT = -1

AMT_AVAILABLE = "amt_available"
GOODS = "goods"

answer_dict = {
    1: "I accept",
    0: "I'm indifferent about",
    -1: "I reject"
}

DEF_MAX_UTIL = 20  # this should be set by the models that use this module

max_util = DEF_MAX_UTIL


"""
All utility functions must be registered here!
"""
UTIL_FUNC = "util_func"
GEN_UTIL_FUNC = "gen_util_func"


def gen_util_func(qty):
    return max_util - qty


def penguin_util_func(qty):
    return 25 - qty


def cat_util_func(qty):
    return 10 - qty


def bear_util_func(qty):
    return 15 - qty


util_funcs = {
    GEN_UTIL_FUNC: gen_util_func,
    "penguin_util_func": penguin_util_func,
    "cat_util_func": cat_util_func,
    "bear_util_func": bear_util_func
}


def get_util_func(fname):
    return util_funcs[fname]


"""
    We expect goods dictionaries to look like:
        goods = {
            "houses": { AMT_AVAILABLE: int, "maybe more fields": vals ... },
            "trucks": { AMT_AVAILABLE: int, "maybe more fields": vals ... },
            "etc.": { AMT_AVAILABLE: int, "maybe more fields": vals ... },
        }
    A trader is an object that can be indexed to yield a goods dictionary.
"""


def is_depleted(goods_dict):
    """
    See if `goods_dict` has any non-zero amount of goods in it.
    """
    for good in goods_dict:
        if goods_dict[good][AMT_AVAILABLE] > 0:
            return False
    # if all goods are 0 (or less) dict is empty:
    return True


def transfer(to_goods, from_goods, good_nm, amt=None):
    """
    Transfer goods between two goods dicts.
    Use `amt` if it is not None.
    """
    if not amt:
        amt = from_goods[good_nm][AMT_AVAILABLE]
    if good_nm not in to_goods:
        to_goods[good_nm] = {AMT_AVAILABLE: 0}
    to_goods[good_nm][AMT_AVAILABLE] += amt
    from_goods[good_nm][AMT_AVAILABLE] -= amt


def get_rand_good(goods_dict, nonzero=False):
    """
    What should this do with empty dict?
    """
    print("Calling get_rand_good()")
    if goods_dict is None or not len(goods_dict):
        return None
    else:
        if nonzero and is_depleted(goods_dict):
            # we can't allocate what we don't have!
            print("Goods are depleted!")
            return None

        goods_list = list(goods_dict.keys())
        good = random.choice(goods_list)
        if nonzero:
            # pick again if the goods is endowed (amt is 0)
            # if we get big goods dicts, this could be slow:
            while goods_dict[good][AMT_AVAILABLE] == 0:
                good = random.choice(goods_list)
        return good


def endow(trader, avail_goods, equal_dist=False, rand_dist=False):
    """
    This function is going to pick a good at random, and give the
    trader all of it, by default. We will write partial distributions
    later.
    """
    if equal_dist:
        # each trader get equal amount of good
        equal_dist()
    elif rand_dist:
        # each trader get random amt of good
        rand_dist()
    else:
        # pick an item at random
        # stick all of it in trader's goods dictionary
        good2acquire = get_rand_good(avail_goods, nonzero=True)
        if good2acquire is not None:
            # get some of the good
            transfer(trader[GOODS], avail_goods, good2acquire)


def equal_dist():
    return


def rand_dist():
    return


def goods_to_str(goods):
    """
    take a goods dict to string
    """
    string = ', '.join([str(goods[k][AMT_AVAILABLE]) + " " + str(k)
                       for k in goods.keys()])
    return string


def answer_to_str(ans):
    """
    convert integer value of ans to string
    """
    return answer_dict[ans]


def negotiate(trader1, trader2):
    # this_good is a dict
    for this_good in trader1["goods"]:
        amt = 1
        while trader1["goods"][this_good][AMT_AVAILABLE] >= amt:
            ans = rec_offer(trader2, this_good, amt, trader1)
            user_debug("I'm " + trader1.name
                       + ", " + answer_to_str(ans) + " this offer")
            if ans == ACCEPT or ans == REJECT:
                break
            amt += 1


def seek_a_trade(agent):
    nearby_agent = get_env().get_closest_agent(agent)
    if nearby_agent is not None:
        negotiate(agent, nearby_agent)

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
        if my_good != his_good and agent["goods"][my_good][AMT_AVAILABLE] > 0:
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
    ufunc_name = curr_good[UTIL_FUNC]
    curr_amt = curr_good[AMT_AVAILABLE]
    curr_util = get_util_func(ufunc_name)(curr_amt)
    new_util = get_util_func(ufunc_name)(curr_amt + change)
    return ((new_util + curr_util) / 2) * change


def adj_add_good(agent, good, amt):
    agent["util"] += utility_delta(agent, good, amt)
    agent["goods"][good][AMT_AVAILABLE] += amt
