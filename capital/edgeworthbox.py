"""
A edgeworthbox model.
Places two groups of agents in the enviornment randomly
and moves them around randomly.
"""

from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import RED, BLUE
from indra.env import Env
from registry.registry import get_env, get_prop
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.utils import init_props
from capital.trade_utils import seek_a_trade, AMT_AVAIL
from capital.trade_utils import GEN_UTIL_FUNC, UTIL_FUNC

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


def create_wagent(name, i, props=None):
    start_wine = DEF_NUM_WINE
    if props is not None:
        start_wine = props.get('start_wine',
                               DEF_NUM_WINE)
    return Agent(name + str(i), action=seek_a_trade,
                 attrs={"goods": {"wine": {AMT_AVAIL: start_wine,
                                           UTIL_FUNC: GEN_UTIL_FUNC,
                                           "incr": 0},
                                  "cheese": {AMT_AVAIL: 0,
                                             UTIL_FUNC: GEN_UTIL_FUNC,
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
                 attrs={"goods": {"cheese": {AMT_AVAIL: start_cheese,
                                             UTIL_FUNC: GEN_UTIL_FUNC,
                                             "incr": 0},
                                  "wine": {AMT_AVAIL: 0,
                                           UTIL_FUNC: GEN_UTIL_FUNC,
                                           "incr": 0}},
                        "util": 0,
                        "pre_trade_util": 0,
                        "trades_with": "Wine holders"})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    global max_util
    pa = init_props(MODEL_NAME, props, model_dir="capital")
    cheese_group = Composite("Cheese holders", {"color": BLUE},
                             member_creator=create_cagent,
                             props=pa,
                             num_members=get_prop('num_cagents',
                                                  DEF_NUM_CAGENTS))
    wine_group = Composite("Wine holders", {"color": RED},
                           member_creator=create_wagent,
                           props=pa,
                           num_members=get_prop('num_wagents',
                                                DEF_NUM_WAGENTS))

    Env("EdgeworthBox",
        height=get_prop('grid_height', DEF_HEIGHT),
        width=get_prop('grid_width', DEF_WIDTH),
        members=[cheese_group, wine_group])

    start_cheese = 0
    start_wine = 0
    if pa is not None:
        start_cheese = get_prop('start_cheese',
                                DEF_NUM_CHEESE)
        start_wine = get_prop('start_wine',
                              DEF_NUM_WINE)
        max_util = max(start_cheese, start_wine)
    else:
        props_max_util = max(start_cheese, start_wine)
        max_util = max(props_max_util, DEF_MAX_UTIL)

    return (cheese_group, wine_group, max_util)


def main():
    global wine_group
    global cheese_group
    global max_util

    (cheese_group, wine_group, max_util) = set_up()

    # `get_env()` returns an env, which itself is a callable object
    get_env()()
    return 0


if __name__ == "__main__":
    main()
