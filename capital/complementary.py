"""
A complementary model.
Places two groups of agents in the enviornment randomly
and moves them around randomly.
"""

from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import BLUE
from indra.env import Env
from registry.registry import get_env, get_prop
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.utils import init_props
from capital.trade_utils import seek_a_trade_w_comp
from capital.trade_utils import UTIL_FUNC, AMT_AVAILABLE
import capital.trade_utils as tu

MODEL_NAME = "complementary"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off
DEF_NUM_TRADER = 2
DEF_NUM_RESOURCES = 2
DEF_NUM_RESOURCES_TYPE = 4
trader_group = None

COMPLEMENTS = "complementaries"
max_utility = tu.max_util
Mkt_GOODS = {"truck": {AMT_AVAILABLE: DEF_NUM_RESOURCES,
                       UTIL_FUNC: "steep_util_func",
                       "incr": 0,
                       COMPLEMENTS: "fuel"},
             "penguin": {AMT_AVAILABLE: DEF_NUM_RESOURCES,
                         UTIL_FUNC: "steep_util_func",
                         "incr": 0,
                         COMPLEMENTS: "pet_food"},
             "pet_food": {AMT_AVAILABLE: DEF_NUM_RESOURCES,
                          UTIL_FUNC: "steep_util_func",
                          "incr": 0,
                          COMPLEMENTS: "penguin"},
             "fuel": {AMT_AVAILABLE: DEF_NUM_RESOURCES,
                      UTIL_FUNC: "steep_util_func",
                      "incr": 0,
                      COMPLEMENTS: "truck"}
             }


def allocate_resources(trader, avail_goods,
                       equal=False, rand=False, comp=True):
    tu.endow(trader, avail_goods, comp=comp)


def create_trader(name, i, props=None):
    return Agent(name + str(i), action=seek_a_trade_w_comp,
                 attrs={"goods": {"truck": {AMT_AVAILABLE: 0,
                                            UTIL_FUNC: "steep_util_func",
                                            "incr": 0,
                                            COMPLEMENTS: "fuel"},
                                  "penguin": {AMT_AVAILABLE: 0,
                                              UTIL_FUNC: "steep_util_func",
                                              "incr": 0,
                                              COMPLEMENTS: "pet_food"},
                                  "pet_food": {AMT_AVAILABLE: 0,
                                               UTIL_FUNC: "steep_util_func",
                                               "incr": 0,
                                               COMPLEMENTS: "penguin"},
                                  "fuel": {AMT_AVAILABLE: 0,
                                           UTIL_FUNC: "steep_util_func",
                                           "incr": 0,
                                           COMPLEMENTS: "truck"}},
                        "util": 0,
                        "pre_trade_util": 0,
                        "trades_with": "trader"})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    global max_utility
    pa = init_props(MODEL_NAME, props, model_dir="capital")
    trader_group = Composite("trader", {"color": BLUE},
                             member_creator=create_trader,
                             props=pa,
                             num_members=get_prop('num_traders',
                                                  DEF_NUM_TRADER))
    Env("env",
        height=get_prop('grid_height', DEF_HEIGHT),
        width=get_prop('grid_width', DEF_WIDTH),
        members=[trader_group])
    for trader in trader_group:
        for i in range(2):
            allocate_resources(trader_group[trader], Mkt_GOODS)
        get_env().user.tell(trader_group[trader]["goods"])
    return (trader_group, max_utility)


def main():
    global trader_group
    global max_utility

    (trader_group, max_utility) = set_up()

    if DEBUG2:
        get_env().user.tell(get_env().__repr__())

    get_env()()
    return 0


if __name__ == "__main__":
    main()
