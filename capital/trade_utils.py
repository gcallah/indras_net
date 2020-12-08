"""
This file contains general functions useful in trading goods.
"""
from indra.agent import MOVE
from indra.user import user_debug
from registry.execution_registry import get_exec_key
from registry.registry import get_env
import random
import copy
import math

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

DIGITS_TO_RIGHT = 2

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


def trade_debug(agent1, agent2, good1, good2, amt1, amt2, gain, loss):
    if DEBUG:
        user_debug(f"       {agent1.name} is offering {amt1} of {good1} to "
                   + f"{agent2.name} for {amt2} of {good2} with a "
                   + f"gain of {round(gain, 2)} and "
                   + f"a loss of {round(loss, 2)}")


def trader_debug(agent):
    if DEBUG:
        user_debug(f"{agent.name} has {goods_to_str(agent[GOODS])}")


def offer_debug(agent, their_good, their_amt, counterparty=None):
    if DEBUG:
        if counterparty is None:
            counterparty = "Unknown"
        user_debug(f"       {agent.name} has received an offer of {their_amt} "
                   + f"of {their_good} from {counterparty}")


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


def transfer(to_goods, from_goods, good_nm, amt=None, comp=False):
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
    # user_debug("Calling get_rand_good()")
    if goods_dict is None or not len(goods_dict):
        return None
    else:
        if nonzero and is_depleted(goods_dict):
            # we can't allocate what we don't have!
            user_debug("Goods are depleted!")
            return None

        goods_list = list(goods_dict.keys())
        good = random.choice(goods_list)
        if nonzero:
            # pick again if the goods is endowed (amt is 0)
            # if we get big goods dicts, this could be slow:
            while goods_dict[good][AMT_AVAIL] == 0:
                good = random.choice(goods_list)
        return good


def incr_util(good_dict, good, amt=None, agent=None, graph=False, comp=None):
    '''
    if graph=True, increase the utility according to
    the weight of edge in the graph
    '''
    if graph:
        good_graph = agent["graph"]
        if comp:
            incr = good_graph.get_weight(good, comp)
        else:
            incr = good_graph.max_neighbors(good, good_dict)
        good_dict[good]["incr"] += incr
    else:
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
        # if the good is too old, set the avaliable amount to 0
        # (good is no longer valid for trading)
        if math.exp(-(1-trader["goods"][good]["durability"]) *
           (trader["goods"][good]["age"]/10)) < 0.0001:
            trader["goods"][good][AMT_AVAIL] = 0
        return round(trader["goods"][good]["divisibility"], DIGITS_TO_RIGHT)
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


def equal_dist(num_trader, to_goods, from_goods, comp=False):
    """
    each trader get equal amount of goods
    to_goods = trader[GOODS], from_goods = avail_goods
    """
    for good in from_goods:
        amt = from_goods[good][AMT_AVAIL] / num_trader
        transfer(to_goods, from_goods, good, amt, comp=comp)


def rand_dist(to_goods, from_goods, comp=False):
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


def rand_goods_list(goods):
    rand_list = list(goods.keys())
    random.shuffle(rand_list)
    return rand_list


def negotiate(trader1, trader2, comp=False, amt=1):
    # this_good is a dict
    user_debug(f"   {trader1.name} is entering negotiations with" +
               f"{trader2.name}")
    # we randomize to eliminate bias towards earlier goods in list
    rand_goods = rand_goods_list(trader1["goods"])
    for this_good in rand_goods:
        amt = amt_adjust(trader1, this_good)
        incr = amt
        while trader1["goods"][this_good][AMT_AVAIL] >= amt:
            # we want to offer "divisibility" amount extra each loop
            ans = send_offer(trader2, this_good, amt, trader1, comp=comp)
            # Besides acceptance or rejection, the offer can be inadequate!
            if ans == ACCEPT or ans == REJECT:
                break
            amt += incr


def seek_a_trade(agent, comp=False, **kwargs):
    execution_key = get_exec_key(kwargs=kwargs)
    nearby_agent = get_env(execution_key=execution_key).get_closest_agent(
        agent)
    if nearby_agent is not None:
        negotiate(agent, nearby_agent, comp)
        return MOVE


def seek_a_trade_w_comp(agent, **kwargs):
    return seek_a_trade(agent, comp=True, **kwargs)


def send_offer(trader2, their_good, their_amt, counterparty, comp=False):
    """
    trader2 receives an offer sent by counterparty.
    We don't need to ever change my_amt
    in this function, because if the counter-party can't bid enough
    for a single unit, no trade is possible.
    """
    offer_debug(trader2, their_good, their_amt, counterparty)
    my_amt = 1
    gain = utility_delta(trader2, their_good, their_amt)
    if comp:
        gain += trader2[GOODS][their_good]["incr"]
    # we randomize to eliminate bias towards earlier goods in list
    rand_goods = rand_goods_list(trader2["goods"])
    for my_good in rand_goods:
        # adjust my_amt if "divisibility" is one of the attributes
        my_amt = amt_adjust(trader2, my_good)
        # don't bother trading identical goods AND we must have some
        # of any good we will trade
        if my_good != their_good and trader2["goods"][my_good][AMT_AVAIL] > 0:
            loss = -utility_delta(trader2, my_good, -my_amt)
            if comp:
                loss += trader2[GOODS][my_good]["incr"]

            trade_debug(trader2, counterparty, my_good, their_good, my_amt,
                        their_amt, gain, loss)
            if gain > loss:
                if send_reply(counterparty, their_good,
                              their_amt, my_good, my_amt, comp=comp):
                    trade(trader2, my_good, my_amt,
                          counterparty, their_good, their_amt, comp=comp)
                    # both goods' trade_count will be increased in sender's dic
                    item = list(trader2["goods"])[0]
                    if "trade_count" in trader2["goods"][item]:
                        counterparty["goods"][my_good]["trade_count"] += 1
                        counterparty["goods"][their_good]["trade_count"] += 1
                    print("RESULT:", trader2.name, "accepts the offer\n")
                    return ACCEPT
                else:
                    print("RESULT:", trader2.name, "rejects the offer\n")
                    return REJECT
            else:
                print("RESULT: offer is inadequate\n")
                return INADEQ
    if DEBUG:
        user_debug(f"{trader2} is rejecting all offers of {their_good}")
    return REJECT


def send_reply(trader1, my_good, my_amt, their_good, their_amt, comp=False):
    """
    trader1 evaluates trader2's offer here:
    """
    # offer_debug(trader1, their_good, their_amt)
    gain = utility_delta(trader1, their_good, their_amt)
    loss = utility_delta(trader1, my_good, -my_amt)
    user_debug(f"       {trader1.name} is evaluating the offer with gain: " +
               f"{round(gain, 2)}, loss: {round(loss, 2)}")
    if comp:
        gain += trader1[GOODS][their_good]["incr"]
        loss -= trader1[GOODS][my_good]["incr"]
    if gain > abs(loss):
        return ACCEPT
    else:
        # this will call a halt to negotiations on this good:
        return INADEQ


def trade(agent, my_good, my_amt, counterparty,
          their_good, their_amt, comp=None):
    adj_add_good(agent, my_good, -my_amt, comp=comp)
    adj_add_good(agent, their_good, their_amt, comp=comp)
    adj_add_good(counterparty, their_good, -their_amt, comp=comp)
    adj_add_good(counterparty, my_good, my_amt, comp=comp)


def adjust_dura(trader, good, val):
    """
    This function will check if durability is an attribute of
    the goods. If so, utility will be adjusted by durability.
    """
    item = list(trader["goods"])[0]
    if "durability" in trader["goods"][item]:
        return val*(trader["goods"][good]["durability"] **
                    (trader["goods"][good]["age"]/5))
    else:
        return val


def utility_delta(agent, good, change):
    """
    We are going to determine the utility of goods gained
    (amt is positive) or lost (amt is negative).
    `change` will be fractional if good divisibility < 1
    """
    curr_good = agent["goods"][good]
    ufunc_name = curr_good[UTIL_FUNC]
    curr_amt = curr_good[AMT_AVAIL]
    curr_util = adjust_dura(agent, good, get_util_func(ufunc_name)(curr_amt))
    new_util = adjust_dura(agent, good,
                           get_util_func(ufunc_name)(curr_amt + change))
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
            incr_util(agent[GOODS], good,
                      amt=amt * STEEP_GRADIENT, agent=agent,
                      graph=True)
        # now increase utility of this good's complements:
        for comp in compl_lst(agent, good):
            incr_util(agent[GOODS], comp,
                      amt=amt * STEEP_GRADIENT, agent=agent,
                      graph=True, comp=good)
        user_debug(agent[GOODS])

    if good_all_gone(agent, good):
        for comp in compl_lst(agent, good):
            agent[GOODS][comp]['incr'] = 0
