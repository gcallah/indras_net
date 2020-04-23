"""
A edgeworthbox model.
Places two groups of agents in the enviornment randomly
and moves them around randomly.
"""

from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env
from registry.registry import get_env, get_prop
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.utils import init_props
import capital.trade_utils as tu
from capital.trade_utils import seek_a_trade, GEN_UTIL_FUNC
from capital.trade_utils import AMT_AVAILABLE, endow, UTIL_FUNC
import copy

MODEL_NAME = "money"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_TRADERS = 4

MONEY_MAX_UTIL = 100

TRADE_COUNT = "trade_count"
INIT_COUNT = 0  # a starting point for trade_count

# these are the goods we hand out at the start:
natures_goods = {
    "cow": {AMT_AVAILABLE: 10, UTIL_FUNC: GEN_UTIL_FUNC,
            "incr": 0, "durability": 0.9, "divisibility": 1.0,
            "trade_count": 0, },
    "gold": {AMT_AVAILABLE: 8, UTIL_FUNC: GEN_UTIL_FUNC,
             "incr": 0, "durability": 1.0, "divisibility": 0.1,
             "trade_count": 0, },
    "cheese": {AMT_AVAILABLE: 2, UTIL_FUNC: GEN_UTIL_FUNC,
               "incr": 0, "durability": 0.8, "divisibility": 0.4,
               "trade_count": 0, },
    "banana": {AMT_AVAILABLE: 7, UTIL_FUNC: GEN_UTIL_FUNC,
               "incr": 0, "durability": 0.2, "divisibility": 0.2,
               "trade_count": 0, },
    "diamond": {AMT_AVAILABLE: 8, UTIL_FUNC: GEN_UTIL_FUNC,
                "incr": 0, "durability": 1.0, "divisibility": 0.8,
                "trade_count": 0, },
}


def initial_amt(pop_hist):
    """
    Set up our pop hist object to record amount traded per period.
    """
    for good in natures_goods:
        pop_hist.record_pop(good, INIT_COUNT)


def record_amt(pop_hist):
    """
    This is our hook into the env to record the number of trades each
    period.
    """
    get_env()
    for good in natures_goods:
        # INIT_COUNT = curr_natures_goods[good][TRADE_COUNT]
        pop_hist.record_pop(good, natures_goods[good][TRADE_COUNT])


def set_env_attrs():
    env = get_env()
    env.set_attr("pop_hist_func", record_amt)
    tu.max_utils = MONEY_MAX_UTIL


def incr_trade_count(good):
    """
    This function will increment the local trade_count by 1
    """
    natures_goods[good]["trade_count"] += 1


def good_decay(goods):
    """
    This function will allow each good to be decaied in each period,
    with AMT_AVAILABLE being adjusted by durability.
    """
    for good in goods:
        goods[good][AMT_AVAILABLE] *= goods[good]["durability"]


def trader_action(agent):
    dic1 = copy.deepcopy(agent["goods"])
    ret = seek_a_trade(agent)
    dic2 = copy.deepcopy(agent["goods"])
    diff = {x: (dic1[x][AMT_AVAILABLE]-dic2[x][AMT_AVAILABLE])
            for x in dic1 if x in dic2}
    for good in diff:
        decayed_amt = dic1[good]["durability"] * dic1[good][AMT_AVAILABLE]
        if (diff[good] != decayed_amt and diff[good] != 0):
            incr_trade_count(good)
            # print(good, "is traded",
            #       natures_goods[good]["trade_count"], "times")
    print(" TRADE COUNT")
    for good in natures_goods:
        print(good, " is traded ",
              natures_goods[good]["trade_count"], " times")
    good_decay(agent["goods"])
    return ret


def create_trader(name, i):
    """
    A func to create a trader.
    """
    return Agent(name + str(i), action=trader_action,
                 attrs={"goods": {},
                        "util": 0,
                        "pre_trade_util": 0})


def nature_to_traders(traders, nature):
    """
    A func to do the initial endowment from nature to all traders
    """
    for trader in traders:
        endow(traders[trader], nature)
        for good in nature:
            if good not in traders[trader]["goods"]:
                traders[trader]["goods"][good] = nature[good].copy()
                traders[trader]["goods"][good][AMT_AVAILABLE] = 0
            else:
                # put attributes other than AMT_AVAILABLE into trader dict
                temp_amt = traders[trader]["goods"][good][AMT_AVAILABLE]
                traders[trader]["goods"][good] = nature[good].copy()
                traders[trader]["goods"][good][AMT_AVAILABLE] = temp_amt
    # each trader is given goods and knows all goods in nature
        print(repr(traders[trader]))


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    # global max_util -> not in use now
    init_props(MODEL_NAME, props, model_dir="capital")
    traders = Composite("Traders",
                        member_creator=create_trader,
                        num_members=get_prop('num_traders',
                                             DEF_NUM_TRADERS))

    nature_to_traders(traders, natures_goods)

    Env("MengerMoney",
        height=get_prop('grid_height', DEF_HEIGHT),
        width=get_prop('grid_width', DEF_WIDTH),
        members=[traders],
        attrs={"goods": natures_goods},
        pop_hist_setup=initial_amt)
    set_env_attrs()


def main():
    set_up()
    # `get_env()` returns an env, which itself is a callable object
    get_env()()
    return 0


if __name__ == "__main__":
    main()
