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
from capital.trade_utils import seek_a_trade, gen_util_func, max_util  # noqa F401
import capital.trade_utils as tu

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
market = None


def create_wagent(name, i, props=None):
    start_wine = DEF_NUM_WINE
    if props is not None:
        start_wine = props.get('start_wine',
                               DEF_NUM_WINE)
    return Agent(name + str(i), action=seek_a_trade,
                 env=market,
                 attrs={"goods": {"wine": {"endow": start_wine,
                                           "util_func": gen_util_func,
                                           "incr": 0},
                                  "cheese": {"endow": 0,
                                             "util_func": gen_util_func,
                                             "incr": 0}
                                  },
                        "util": 0,
                        "pre_trade_util": 0,
                        "trades_with": "Cheese holders"})


def create_cagent(name, i, props=None):
    start_cheese = DEF_NUM_CHEESE
    if props is not None:
        start_cheese = props.get('start_cheese',
                                 DEF_NUM_CHEESE)
    return Agent(name + str(i), action=seek_a_trade,
                 env=market,
                 attrs={"goods": {"cheese": {"endow": start_cheese,
                                             "util_func": gen_util_func,
                                             "incr": 0},
                                  "wine": {"endow": 0,
                                           "util_func": gen_util_func,
                                           "incr": 0}},
                        "util": 0,
                        "pre_trade_util": 0,
                        "trades_with": "Wine holders"})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    global max_util
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

    market = Env("env",
                 height=pa.get('grid_height', DEF_HEIGHT),
                 width=pa.get('grid_width', DEF_WIDTH),
                 members=[cheese_group, wine_group],
                 props=pa)
    tu.env = market  # we have to find a better way to handle this!

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

    return (market, cheese_group, wine_group, max_util)


def main():
    global wine_group
    global cheese_group
    global market
    global max_util

    (market, cheese_group, wine_group, max_util) = set_up()

    if DEBUG2:
        market.user.tell(market.__repr__())

    market()
    return 0


if __name__ == "__main__":
    main()
