"""
A trade model.
Places two groups of agents in the enviornment randomly
and moves them around randomly.
"""

from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import BLUE
from indra.env import Env
# from indra.registry import registry
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.utils import get_props
from trade_utils import seek_a_trade, gen_util_func, max_util  # noqa F401
import trade_utils as tu
import random

MODEL_NAME = "trade"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off
DEF_NUM_TRADER = 2
DEF_NUM_RESOURCES = 4
DEF_NUM_RESOURCES_TYPE = 4
trader_group = None
market = None

def random_generate_resources(i,total_type, total_resources, num_trader):
    r = []
    for k in range(total_type):
        # r.append(int((total_resources * 2) * (random.random() / num_trader)))
        if i == 0 and k < 2:
            r.append(4)
        elif i ==1 and k > 1:
            r.append(4)
        else:
            r.append(0)
    return r


def create_trader(name, i, props=None):
    num_r = DEF_NUM_RESOURCES
    num_r_type = DEF_NUM_RESOURCES_TYPE
    num_trader = DEF_NUM_TRADER
    if props is not None:
        num_r = props.get('total_resources',
                          DEF_NUM_RESOURCES)
        num_r_type = props.get('total_type',
                               DEF_NUM_RESOURCES_TYPE)
        num_trader = props.get('num_traders',
                               DEF_NUM_TRADER)
    resources = random_generate_resources(i,num_r_type, num_r, num_trader)
    return Agent(name + str(i), action=seek_a_trade,
                 env=market,
                 attrs={"goods": {"penguin": {"endow": resources[0],
                                              "util_func": gen_util_func,
                                              "incr": 0},
                                  "cat": {"endow": resources[1],
                                          "util_func": gen_util_func,
                                          "incr": 0},
                                  "bear": {"endow": resources[2],
                                           "util_func": gen_util_func,
                                           "incr": 0},
                                  "pet food": {"endow": resources[3],
                                               "util_func": gen_util_func,
                                               "incr": 0}
                                  },
                        "util": 0,
                        "pre_trade_util": 0,
                        "trades_with": "trader"})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    global max_util
    pa = get_props(MODEL_NAME, props, model_dir="capital")
    trader_group = Composite("trader", {"color": BLUE},
                             member_creator=create_trader,
                             props=pa,
                             num_members=pa.get('num_traders',
                                                DEF_NUM_TRADER))

    market = Env("env",
                 height=pa.get('grid_height', DEF_HEIGHT),
                 width=pa.get('grid_width', DEF_WIDTH),
                 members=[trader_group],
                 props=pa)
    tu.env = market  # we have to find a better way to handle this!
    return (market, trader_group)


def main():
    global trader_group
    global market

    (market, trader_group) = set_up()

    if DEBUG2:
        market.user.tell(market.__repr__())

    market()
    return 0


if __name__ == "__main__":
    main()
