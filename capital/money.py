"""
A edgeworthbox model.
Places two groups of agents in the enviornment randomly
and moves them around randomly.
"""

from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env
from indra.registry import get_env
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.utils import get_props
from capital.trade_utils import seek_a_trade, gen_util_func, max_util  # noqa F401

MODEL_NAME = "money"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_TRADERS = 2

traders = None


def create_trader(name, i, props=None):
    return Agent(name + str(i), action=seek_a_trade,
                 attrs={"goods": {"wine": {"endow": 10,
                                           "util_func": gen_util_func,
                                           "incr": 0},
                                  "cheese": {"endow": 0,
                                             "util_func": gen_util_func,
                                             "incr": 0}
                                  },
                        "util": 0,
                        "pre_trade_util": 0,
                        "trades_with": "Cheese holders"})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    global max_util
    pa = get_props(MODEL_NAME, props, model_dir="capital")
    traders = Composite("Traders",
                        member_creator=create_trader,
                        props=pa,
                        num_members=pa.get('num_traders',
                                           DEF_NUM_TRADERS))

    Env("MengerMoney",
        height=pa.get('grid_height', DEF_HEIGHT),
        width=pa.get('grid_width', DEF_WIDTH),
        members=[traders],
        props=pa)

    return (traders, max_util)


def main():
    global traders
    global max_util

    (traders, max_util) = set_up()

    # `get_env()` returns an env, which itself is a callable object
    get_env()()
    return 0


if __name__ == "__main__":
    main()
