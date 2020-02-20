"""
A edgeworthbox model.
Places two groups of agents in the enviornment randomly
and moves them around randomly.
"""

from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env
from indra.registry import get_env, get_prop
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.utils import init_props
from capital.trade_utils import seek_a_trade, GEN_UTIL_FUNC
from capital.trade_utils import AMT_AVAILABLE, endow, UTIL_FUNC

MODEL_NAME = "money"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_TRADERS = 2


# these are the goods we hand out at the start:
natures_goods = {
    "oil": {AMT_AVAILABLE: 100, UTIL_FUNC: GEN_UTIL_FUNC, "incr": 0},
    "gold": {AMT_AVAILABLE: 100, UTIL_FUNC: GEN_UTIL_FUNC, "incr": 0},
}


def create_trader(name, i, props=None):
    return Agent(name + str(i), action=seek_a_trade,
                 attrs={"goods": {},
                        "util": 0,
                        "pre_trade_util": 0})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    # global max_util -> not in use now
    pa = init_props(MODEL_NAME, props, model_dir="capital")
    traders = Composite("Traders",
                        member_creator=create_trader,
                        props=pa,
                        num_members=get_prop('num_traders',
                                             DEF_NUM_TRADERS))
    for trader in traders:
        endow(traders[trader], natures_goods)
        for good in natures_goods:
            if good not in traders[trader]["goods"]:
                traders[trader]["goods"][good] = natures_goods[good]
                traders[trader]["goods"][good][AMT_AVAILABLE] = 0
    # each trader is given goods and know all goods in the nature
            print(repr(traders[trader]))

    Env("MengerMoney",
        height=get_prop('grid_height', DEF_HEIGHT),
        width=get_prop('grid_width', DEF_WIDTH),
        members=[traders])


def main():
    set_up()
    # `get_env()` returns an env, which itself is a callable object
    get_env()()
    return 0


if __name__ == "__main__":
    main()
