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
nature_goods = {
    "cow": {AMT_AVAILABLE: 10, UTIL_FUNC: GEN_UTIL_FUNC,
            "incr": 0, "durability": 0.9, "divisibility": 1.0, },
    "gold": {AMT_AVAILABLE: 8, UTIL_FUNC: GEN_UTIL_FUNC,
             "incr": 0, "durability": 1.0, "divisibility": 0.1, },
    "cheese": {AMT_AVAILABLE: 2, UTIL_FUNC: GEN_UTIL_FUNC,
               "incr": 0, "durability": 0.8, "divisibility": 0.3, },
    "banana": {AMT_AVAILABLE: 7, UTIL_FUNC: GEN_UTIL_FUNC,
               "incr": 0, "durability": 0.2, "divisibility": 0.9, },
    "diamond": {AMT_AVAILABLE: 8, UTIL_FUNC: GEN_UTIL_FUNC,
                "incr": 0, "durability": 1.0, "divisibility": 0.2, },
}


def create_trader(name, i, props=None):
    """
    A func to create a trader with given name
    """
    return Agent(name + str(i), action=seek_a_trade,
                 attrs={"goods": {},
                        "util": 0,
                        "pre_trade_util": 0})


def nature_to_traders(traders, nature):
    """
    A func to do the initial endowment from the nature to all traders
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
    # each trader is given goods and know all goods in the nature
        print(repr(traders[trader]))


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

    nature_to_traders(traders, nature_goods)

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
