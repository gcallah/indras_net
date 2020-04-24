"""
This file contains general functions useful in trading goods.
"""
# from indra.user import user_debug
from registry.registry import get_env
import random
import copy

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
COMPLEMENTS = "complementaries"
DEF_MAX_UTIL = 20  # this should be set by the models that use this module

max_util = DEF_MAX_UTIL


"""
All utility functions must be registered here!
"""
UTIL_FUNC = "util_func"
GEN_UTIL_FUNC = "gen_util_func"
STEEP_GRADIENT = 20


def gen_util_func(qty):
    return max_util - qty


def penguin_util_func(qty):
    return 25 - qty


def cat_util_func(qty):
    return 10 - qty


def bear_util_func(qty):
    return 15 - qty


def steep_util_func(qty):
    return 20 - STEEP_GRADIENT*qty


util_funcs = {
    GEN_UTIL_FUNC: gen_util_func,
    "penguin_util_func": penguin_util_func,
    "cat_util_func": cat_util_func,
    "bear_util_func": bear_util_func,
    "steep_util_func": steep_util_func
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


def is_complement(trader, good, comp):
    """
    see if 'comp' is complement of 'good'
    """
    if comp in trader[GOODS][good][COMPLEMENTS]:
        return True
    else:
        return False


def check_complement(trader):
    """
    see if COMPLEMENT is an attribute in trader
    """
    if COMPLEMENTS in trader[GOODS]:
        return True
    else:
        return False


def is_depleted(goods_dict):
    """
    See if `goods_dict` has any non-zero amount of goods in it.
    """
    for good in goods_dict:
        if goods_dict[good][AMT_AVAILABLE] > 0:
            return False
    # if all goods are 0 (or less) dict is empty:
    return True


def transfer(to_goods, from_goods, good_nm, amt=None, comp=None):
    """
    Transfer goods between two goods dicts.
    Use `amt` if it is not None.
    """
    nature = copy.deepcopy(from_goods)
    if not amt:
        amt = from_goods[good_nm][AMT_AVAILABLE]
    for good in from_goods:
        if good in to_goods:
            amt_before_add = to_goods[good][AMT_AVAILABLE]
        else:
            amt_before_add = 0
        to_goods[good] = nature[good]
        if good != good_nm:
            to_goods[good][AMT_AVAILABLE] = amt_before_add
        else:
            from_goods[good][AMT_AVAILABLE] -= amt
            to_goods[good][AMT_AVAILABLE] = amt_before_add + amt
    if comp:
        for g in to_goods:
            if to_goods[g][AMT_AVAILABLE] > 0:
                to_goods[g]['incr'] += amt * STEEP_GRADIENT
                comp_list = to_goods[g][COMPLEMENTS]
                for comp in comp_list:
                    to_goods[comp]['incr'] += STEEP_GRADIENT * amt


def get_rand_good(goods_dict, nonzero=False):
    """
    What should this do with empty dict?
    """
    # print("Calling get_rand_good()")
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


def incr_util(good_dict, good, amt=None):
    if amt:
        good_dict[good]["incr"] += amt
    else:
        good_dict[good]["incr"] += 1


def amt_adjust(trader, good):
    """
    This function will check if divisibility is an attribute of
    the goods. If so, amt traded will depend on divisibility; otherwise,
    amt will be 1.
    """
    item = list(trader["goods"])[0]
    if "divisibility" in trader["goods"][item]:
        return trader["goods"][good]["divisibility"]
    else:
        return 1


def endow(trader, avail_goods, equal=False, rand=False, comp=False):
    """
    This function is going to pick a good at random, and give the
    trader all of it, by default. We will write partial distributions
    later.
    """
    if equal:
        # each trader get equal amount of good
        equal_dist(comp=comp)
    elif rand:
        # each trader get random amt of good
        rand_dist(trader[GOODS], avail_goods, comp=comp)
    else:
        # pick an item at random
        # stick all of it in trader's goods dictionary
        good2acquire = get_rand_good(avail_goods, nonzero=True)
        if good2acquire is not None:
            # get some of the good
            transfer(trader[GOODS], avail_goods, good2acquire, comp=comp)


def equal_dist(num_trader, to_goods, from_goods, comp=None):
    """
    each trader get equal amount of goods
    to_goods = trader[GOODS], from_goods = avail_goods
    """
    for good in from_goods:
        amt = from_goods[good][AMT_AVAILABLE]/num_trader
        transfer(to_goods, from_goods, good, amt, comp=comp)


def rand_dist(to_goods, from_goods, comp=None):
    """
    select random good by random amount and transfer to trader
    """
    selected_good = get_rand_good(from_goods, nonzero=True)
    amt = random.randrange(0, from_goods[selected_good][AMT_AVAILABLE], 1)
    transfer(to_goods, from_goods, selected_good, amt, comp=comp)


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


def negotiate(trader1, trader2, comp=None):
    # this_good is a dict
    for this_good in trader1["goods"]:
        amt = 1
        # amt = amt_adjust(trader1, this_good)
        while trader1["goods"][this_good][AMT_AVAILABLE] >= amt:
            ans = rec_offer(trader2, this_good, amt, trader1, comp=comp)
#             user_debug("I'm " + trader1.name
#                        + ", " + answer_to_str(ans) + " this offer")
            if ans == ACCEPT or ans == REJECT:
                break
            amt += amt


def seek_a_trade(agent):
    nearby_agent = get_env().get_closest_agent(agent)
    if nearby_agent is not None:
        negotiate(agent, nearby_agent)
        print("I'm", agent.name, "I have", goods_to_str(agent[GOODS]))
    # return False means to move
    return False


def seek_a_trade_w_comp(agent):
    nearby_agent = get_env().get_closest_agent(agent)
    if nearby_agent is not None:
        negotiate(agent, nearby_agent, comp=True)
        print("I'm", agent.name, "I have", goods_to_str(agent[GOODS]))
    # return False means to move
    return False


def rec_offer(agent, his_good, his_amt, counterparty, comp=None):
    """
    Receive an offer: we don't need to ever change my_amt
    in this function, because if the counter-party can't bid enough
    for a single unit, no trade is possible.
    """
    my_amt = 1
    gain = utility_delta(agent, his_good, his_amt)
    if comp:
        gain += agent[GOODS][his_good]["incr"]
        print(his_good, agent[GOODS][his_good]['incr'])
    for my_good in agent["goods"]:
        # adjust my_amt if "divisibility" is one of the attributes
        # my_amt = amt_adjust(agent, my_good)
        if my_good != his_good and agent["goods"][my_good][AMT_AVAILABLE] > 0:
            loss = -utility_delta(agent, my_good, -my_amt)
            if comp:
                loss += agent[GOODS][my_good]["incr"]

            print("my good: " + my_good + "; his good: " + his_good
                  + ", I gain: " + str(gain) +
                  " and lose: " + str(loss))
            if gain > loss:
                if rec_reply(counterparty, his_good,
                             his_amt, my_good, my_amt, comp=comp):
                    trade(agent, my_good, my_amt,
                          counterparty, his_good, his_amt, comp=comp)
                    return ACCEPT
                else:
                    return INADEQ
    return REJECT


def rec_reply(agent, my_good, my_amt, his_good, his_amt, comp=None):
    gain = utility_delta(agent, his_good, his_amt)
    loss = utility_delta(agent, my_good, -my_amt)
    if comp:
        gain += agent[GOODS][his_good]["incr"]
        loss -= agent[GOODS][my_good]["incr"]
#     print(agent.name, "receiving a reply: gain = ",
#           gain, "and loss =", abs(loss))
    if gain > abs(loss):
        return ACCEPT
    else:
        return INADEQ


def trade(agent, my_good, my_amt, counterparty, his_good, his_amt, comp=None):
    adj_add_good(agent, my_good, -my_amt, comp=comp)
    adj_add_good(agent, his_good, his_amt, comp=comp)
    adj_add_good(counterparty, his_good, -his_amt, comp=comp)
    adj_add_good(counterparty, my_good, my_amt, comp=comp)


def utility_delta(agent, good, change):
    """
    We are going to determine the utility of goods gained
    (amt is positive) or lost (amt is negative).
    """
    curr_good = agent["goods"][good]
    ufunc_name = curr_good[UTIL_FUNC]
    # temp change
    if ("divisibility" in agent["goods"][list(agent["goods"])[0]]):
        curr_amt = curr_good[AMT_AVAILABLE]/curr_good["divisibility"]
    else:
        curr_amt = curr_good[AMT_AVAILABLE]
    # curr_amt = curr_good[AMT_AVAILABLE]
    curr_util = get_util_func(ufunc_name)(curr_amt)
    new_util = get_util_func(ufunc_name)(curr_amt + change)
    return ((new_util + curr_util) / 2) * change


def adj_add_good(agent, good, amt, comp=None):
    if not comp:
        agent["util"] += utility_delta(agent, good, amt)
        # temp change
        amt *= amt_adjust(agent, good)
        agent["goods"][good][AMT_AVAILABLE] += amt
    else:
        adj_add_good_w_comp(agent, good, amt)


def adj_add_good_w_comp(agent, good, amt):
    agent["util"] += utility_delta(agent, good, amt)
    # temp change
    amt *= amt_adjust(agent, good)
    old_amt = agent["goods"][good][AMT_AVAILABLE]
    if old_amt == 0 and amt > 0 and agent[GOODS][good]['incr'] != 0:
        incr_util(agent[GOODS], good, amt=amt*STEEP_GRADIENT)
        for comp in agent[GOODS][good][COMPLEMENTS]:
            incr_util(agent[GOODS], comp, amt=amt*STEEP_GRADIENT)
        print(agent[GOODS])
    agent["goods"][good][AMT_AVAILABLE] += amt
#     agent["goods"][good]["incr"] = 0
    for g in agent[GOODS]:
        if agent[GOODS][g][AMT_AVAILABLE] == 0:
            agent[GOODS][g]['incr'] = 0
            comp_list = agent["goods"][good][COMPLEMENTS]
            for comp in comp_list:
                agent["goods"][comp]['incr'] = 0
        if agent[GOODS][g][AMT_AVAILABLE] > 0:
            agent[GOODS][g]['incr'] += amt * STEEP_GRADIENT
            comp_list = agent["goods"][good][COMPLEMENTS]
            for comp in comp_list:
                agent["goods"][comp]['incr'] += STEEP_GRADIENT * amt
