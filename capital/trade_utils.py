"""
This file contains general functions useful in trading goods.
"""
from registry.registry import get_env
import random
import copy

DEBUG = True

ACCEPT = 1
INADEQ = 0
REJECT = -1

AMT_AVAIL = "amt_available"
GOODS = "goods"

answer_dict = {
    1: "I accept",
    0: "I'm indifferent about",
    -1: "I reject"
}

COMPLEMENTS = "complementaries"
DEF_MAX_UTIL = 20  # this should be set by the models that use this module
DIM_UTIL_BASE = 1.1  # we should experiment with this!

max_util = DEF_MAX_UTIL


"""
All utility functions must be registered here!
"""
UTIL_FUNC = "util_func"
GEN_UTIL_FUNC = "gen_util_func"
STEEP_GRADIENT = 20


def gen_util_func(qty):
    return max_util * (DIM_UTIL_BASE ** (-qty))


def penguin_util_func(qty):
    return 25 * (1 ** (-qty))


def cat_util_func(qty):
    return 10 * (1 ** (-qty))


def bear_util_func(qty):
    return 15 * (1 ** (-qty))


def steep_util_func(qty):
    return 20 * (2 ** (-qty))


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
            "houses": { AMT_AVAIL: int, "maybe more fields": vals ... },
            "trucks": { AMT_AVAIL: int, "maybe more fields": vals ... },
            "etc.": { AMT_AVAIL: int, "maybe more fields": vals ... },
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
        if goods_dict[good][AMT_AVAIL] > 0:
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
        amt = from_goods[good_nm][AMT_AVAIL]
    for good in from_goods:
        if good in to_goods:
            amt_before_add = to_goods[good][AMT_AVAIL]
        else:
            amt_before_add = 0
        to_goods[good] = nature[good]
        if good != good_nm:
            to_goods[good][AMT_AVAIL] = amt_before_add
        else:
            from_goods[good][AMT_AVAIL] -= amt
            to_goods[good][AMT_AVAIL] = amt_before_add + amt
    if comp:
        for g in to_goods:
            if to_goods[g][AMT_AVAIL] > 0:
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
            while goods_dict[good][AMT_AVAIL] == 0:
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
        amt = from_goods[good][AMT_AVAIL] / num_trader
        transfer(to_goods, from_goods, good, amt, comp=comp)


def rand_dist(to_goods, from_goods, comp=None):
    """
    select random good by random amount and transfer to trader
    """
    selected_good = get_rand_good(from_goods, nonzero=True)
    amt = random.randrange(0, from_goods[selected_good][AMT_AVAIL], 1)
    transfer(to_goods, from_goods, selected_good, amt, comp=comp)


def goods_to_str(goods):
    """
    take a goods dict to string
    """
    string = ', '.join([str(goods[k][AMT_AVAIL]) + " " + str(k)
                        for k in goods.keys()])
    return string


def answer_to_str(ans):
    """
    convert integer value of ans to string
    """
    return answer_dict[ans]


def negotiate(trader1, trader2, comp=False, amt=1):
    # this_good is a dict
    for this_good in trader1["goods"]:
        amt = amt_adjust(trader1, this_good)
        while trader1["goods"][this_good][AMT_AVAIL] >= amt:
            # we want to offer "divisibility" amount extra each loop
            ans = rec_offer(trader2, this_good, amt, trader1, comp=comp)
            # Besides acceptance or rejection, the offer can be inadequate!
            if ans == ACCEPT or ans == REJECT:
                break
            amt += amt


def seek_a_trade(agent, comp=False):
    nearby_agent = get_env().get_closest_agent(agent)
    if nearby_agent is not None:
        negotiate(agent, nearby_agent, comp)
        if DEBUG:
            print("I'm", agent.name,
                  "I have", goods_to_str(agent[GOODS]))
    # return False means to move
    return False


def seek_a_trade_w_comp(agent):
    return seek_a_trade(agent, comp=True)


def rec_offer(agent, their_good, their_amt, counterparty, comp=False):
    """
    Receive an offer: we don't need to ever change my_amt
    in this function, because if the counter-party can't bid enough
    for a single unit, no trade is possible.
    """
    my_amt = 1
    gain = utility_delta(agent, their_good, their_amt)
    if comp:
        gain += agent[GOODS][their_good]["incr"]
        print(their_good, agent[GOODS][their_good]['incr'])
    for my_good in agent["goods"]:
        # adjust my_amt if "divisibility" is one of the attributes
        my_amt = amt_adjust(agent, my_good)
        if my_good != their_good and agent["goods"][my_good][AMT_AVAIL] > 0:
            loss = -utility_delta(agent, my_good, -my_amt)
            if comp:
                loss += agent[GOODS][my_good]["incr"]

            print("my good: " + my_good + "; his good: " + their_good
                  + ", I gain: " + str(gain) +
                  " and lose: " + str(loss))
            if gain > loss:
                if rec_reply(counterparty, their_good,
                             their_amt, my_good, my_amt, comp=comp):
                    trade(agent, my_good, my_amt,
                          counterparty, their_good, their_amt, comp=comp)
                    return ACCEPT
                else:
                    return INADEQ
    return REJECT


def rec_reply(agent, my_good, my_amt, their_good, their_amt, comp=None):
    gain = utility_delta(agent, their_good, their_amt)
    loss = utility_delta(agent, my_good, -my_amt)
    if comp:
        gain += agent[GOODS][their_good]["incr"]
        loss -= agent[GOODS][my_good]["incr"]
    if gain > abs(loss):
        return ACCEPT
    else:
        return INADEQ


def trade(agent, my_good, my_amt, counterparty,
          their_good, their_amt, comp=None):
    adj_add_good(agent, my_good, -my_amt, comp=comp)
    adj_add_good(agent, their_good, their_amt, comp=comp)
    adj_add_good(counterparty, their_good, -their_amt, comp=comp)
    adj_add_good(counterparty, my_good, my_amt, comp=comp)


def utility_delta(agent, good, change):
    """
    We are going to determine the utility of goods gained
    (amt is positive) or lost (amt is negative).
    `change` will be fractional if good divisibility < 1
    """
    curr_good = agent["goods"][good]
    ufunc_name = curr_good[UTIL_FUNC]
    curr_amt = curr_good[AMT_AVAIL]
    curr_util = get_util_func(ufunc_name)(curr_amt)
    new_util = get_util_func(ufunc_name)(curr_amt + change)
    return ((new_util + curr_util) / 2) * change


def adj_add_good(agent, good, amt, comp=None):
    agent["util"] += utility_delta(agent, good, amt)
    old_amt = agent["goods"][good][AMT_AVAIL]
    agent["goods"][good][AMT_AVAIL] += amt
    if comp:
        adj_add_good_w_comp(agent, good, amt, old_amt)


def new_good(old_amt, amt):
    return old_amt == 0 and amt > 0


def is_compl_good(agent, good):
    '''
    check if this good is a comp of other goods that the agent have
    '''
    return agent[GOODS][good]['incr'] != 0


def good_all_gone(agent, g):
    '''
    Check if this agent no longer has this good
    '''
    return agent[GOODS][g][AMT_AVAIL] == 0


def compl_lst(agent, good):
    '''
    return the complimentary list of this good
    '''
    return agent[GOODS][good][COMPLEMENTS]


def adj_add_good_w_comp(agent, good, amt, old_amt):
    if new_good(old_amt, amt):
        if is_compl_good(agent, good):
            incr_util(agent[GOODS], good, amt=amt * STEEP_GRADIENT)
        # now increase utility of this good's complements:
        for comp in compl_lst(agent, good):
            incr_util(agent[GOODS], comp, amt=amt * STEEP_GRADIENT)
        print(agent[GOODS])

    if good_all_gone(agent, good):
        for comp in compl_lst(agent, good):
            agent[GOODS][comp]['incr'] = 0
