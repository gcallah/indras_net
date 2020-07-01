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
from capital.trade_utils import AMT_AVAIL, endow, UTIL_FUNC
import copy

MODEL_NAME = "money"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_TRADERS = 4

MONEY_MAX_UTIL = 100

DUR_DECR = "durability_decrement"
TRADE_COUNT = "trade_count"
INIT_COUNT = 0  # a starting point for trade_count

# these are the goods we hand out at the start:
natures_goods = {
    # add initial value to this data?
    "cow": {AMT_AVAIL: 10, UTIL_FUNC: GEN_UTIL_FUNC,
            "incr": 0, DUR_DECR: 0.8, "divisibility": 1.0,
            "trade_count": 0, "is_allocated": False, },
    "gold": {AMT_AVAIL: 8, UTIL_FUNC: GEN_UTIL_FUNC,
             "incr": 0, DUR_DECR: 1.0, "divisibility": 0.1,
             "trade_count": 0, "is_allocated": False, },
    "cheese": {AMT_AVAIL: 2, UTIL_FUNC: GEN_UTIL_FUNC,
               "incr": 0, DUR_DECR: 0.8, "divisibility": 0.4,
               "trade_count": 0, "is_allocated": False, },
    "banana": {AMT_AVAIL: 7, UTIL_FUNC: GEN_UTIL_FUNC,
               "incr": 0, DUR_DECR: 0.2, "divisibility": 0.2,
               "trade_count": 0, "is_allocated": False, },
    "diamond": {AMT_AVAIL: 8, UTIL_FUNC: GEN_UTIL_FUNC,
                "incr": 0, DUR_DECR: 1.0, "divisibility": 0.8,
                "trade_count": 0, "is_allocated": False, },
    "avocado": {AMT_AVAIL: 5, UTIL_FUNC: GEN_UTIL_FUNC,
                "incr": 0, DUR_DECR: 0.3, "divisibility": 0.5,
                "trade_count": 0, "is_allocated": False, },
    "stone": {AMT_AVAIL: 10, UTIL_FUNC: GEN_UTIL_FUNC,
              "incr": 0, DUR_DECR: 1.0, "divisibility": 1.0,
              "trade_count": 0, "is_allocated": False, },
    "milk": {AMT_AVAIL: 8, UTIL_FUNC: GEN_UTIL_FUNC,
             "incr": 0, DUR_DECR: 0.2, "divisibility": 0.15,
             "trade_count": 0, "is_allocated": False, },
}


class Good:
    def __init__(self, name, amt, age=0):
        self.amt = amt
        self.dur_decr = natures_goods[name][DUR_DECR]
        self.util_func = natures_goods[name][UTIL_FUNC]
        self.age = age

    def get_decr_amt(self):
        return self.dur_decr * self.age

    def decay(self):
        self.age += 1


def initial_amt(pop_hist):
    """
    Set up our pop hist object to record amount traded per period.
    """
    for good in natures_goods:
        if natures_goods[good]["is_allocated"] is True:
            pop_hist.record_pop(good, INIT_COUNT)


def record_amt(pop_hist):
    """
    This is our hook into the env to record the number of trades each
    period.
    """
    get_env()
    for good in natures_goods:
        if natures_goods[good]["is_allocated"] is True:
            pop_hist.record_pop(good, natures_goods[good][TRADE_COUNT])


def incr_trade_count(good):
    """
    This function will increment the local trade_count by 1
    """
    natures_goods[good]["trade_count"] += 1


def good_decay(goods):
    """
    This function will allow each good to be decaied in each period,
    with AMT_AVAIL being adjusted by durability.
    """
    for good in goods:
        # Durability calculation needs to be updated
        goods[good][AMT_AVAIL] = goods[good][DUR_DECR]


def trade_report(env):
    get_env()
    trade_count_dic = {x: natures_goods[x]["trade_count"]
                       for x in natures_goods}
    return "Number of trades last period: " + "\n" \
           + str(trade_count_dic) + "\n"


def money_trader_action(agent):
    dic1 = copy.deepcopy(agent["goods"])
    ret = seek_a_trade(agent)
    dic2 = copy.deepcopy(agent["goods"])
    diff = {x: (dic1[x][AMT_AVAIL] - dic2[x][AMT_AVAIL])
            for x in dic1 if x in dic2}
    for good in diff:
        # updated due to change in durability calculation
        # decayed_amt = dic1[good][DUR_DECR] * dic1[good][AMT_AVAIL]
        # if (diff[good] != decayed_amt and diff[good] != 0):
        if diff[good] != 0:
            incr_trade_count(good)
    # print("TRADE COUNT")
    # for good in natures_goods:
    #     print(good, " is traded ",
    #           natures_goods[good]["trade_count"], " times")
    # good_decay(agent["goods"])
    return ret


def create_trader(name, i):
    """
    A func to create a trader.
    """
    return Agent(name + str(i), action=money_trader_action,
                 # goods will now be a dictionary like:
                 # goods["cow"] = [cowA, cowB, cowC, etc.]
                 attrs={"goods": {},
                        "util": 0,
                        "pre_trade_util": 0})


def nature_to_traders(traders, nature):
    """
    A func to do the initial endowment from nature to all traders
    """
    for trader in traders:
        endow(traders[trader], nature)
        for good in traders[trader]["goods"]:
            if traders[trader]["goods"][good][AMT_AVAIL] != 0:
                nature[good]["is_allocated"] = True
        print(repr(traders[trader]))


def set_env_attrs():
    env = get_env()
    env.set_attr("pop_hist_func", record_amt)
    env.set_attr("census_func", trade_report)
    tu.max_utils = MONEY_MAX_UTIL


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    init_props(MODEL_NAME, props, model_dir="capital")
    traders = Composite("Traders",
                        member_creator=create_trader,
                        num_members=get_prop('num_traders',
                                             DEF_NUM_TRADERS))

    nature_to_traders(traders, natures_goods)

    Env(MODEL_NAME,
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
