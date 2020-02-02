"""
A trade model.
Places two groups of agents in the enviornment randomly
and moves them around randomly.
"""

import random
from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import BLUE
from indra.env import Env
from indra.registry import get_env
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.utils import get_props
from capital.trade_utils import seek_a_trade, gen_util_func
import capital.trade_utils as tu

MODEL_NAME = "trade"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off
DEF_NUM_TRADER = 2
DEF_NUM_RESOURCES = 20
DEF_NUM_RESOURCES_TYPE = 4
trader_group = None

max_utility = tu.max_util


def random_generate_resources(i, total_type, total_resources):
    r = []
    global max_utility
    for k in range(total_type):
        # total resources is the amt of resource that each resource holder have
        num_resource = int((total_resources * 2)
                           * (random.random() / total_type * 2))
        if num_resource > max_utility:
            max_utility = num_resource
        if i % 2 == 0 and k < total_type // 2:
            r.append(num_resource)
        elif i % 2 == 1 and k > total_type // 2 - 1:
            r.append(num_resource)
        else:
            r.append(0)

    return r


def create_trader(name, i, props=None):
    num_r = DEF_NUM_RESOURCES
    num_r_type = DEF_NUM_RESOURCES_TYPE
    # num_trader = DEF_NUM_TRADER
    if props is not None:
        num_r = props.get('total_resources',
                          DEF_NUM_RESOURCES)
        num_r_type = props.get('total_type',
                               DEF_NUM_RESOURCES_TYPE)
    resources = random_generate_resources(i, num_r_type, num_r)
    return Agent(name + str(i), action=seek_a_trade,
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
    global max_utility
    pa = get_props(MODEL_NAME, props, model_dir="capital")
    trader_group = Composite("trader", {"color": BLUE},
                             member_creator=create_trader,
                             props=pa,
                             num_members=pa.get('num_traders',
                                                DEF_NUM_TRADER))

    Env("env",
        height=pa.get('grid_height', DEF_HEIGHT),
        width=pa.get('grid_width', DEF_WIDTH),
        members=[trader_group],
        props=pa)
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
