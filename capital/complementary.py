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
from indra.user import user_log_notif
from capital.trade_utils import seek_a_trade_w_comp
from capital.trade_utils import UTIL_FUNC, AMT_AVAILABLE
import capital.trade_utils as tu

MODEL_NAME = "complementary"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off
DEF_NUM_TRADER = 2

DEF_NUM_RESOURCES = 1
DEF_NUM_RESOURCES_TYPE = 6
MKT_GOODS = "mkt_goods"

COMPLEMENTS = "complementaries"


def allocate_resources(trader, avail_goods,
                       equal=False, rand=False):
    tu.endow(trader, avail_goods, equal=equal, rand=rand, comp=True)


def create_trader(name, i, props=None):
    return Agent(name + str(i), action=seek_a_trade_w_comp,
                 attrs={"goods": {"truck": {AMT_AVAILABLE: 0,
                                            UTIL_FUNC: "steep_util_func",
                                            "incr": 0,
                                            COMPLEMENTS: ["fuel", "land"]},
                                  "penguin": {AMT_AVAILABLE: 0,
                                              UTIL_FUNC: "steep_util_func",
                                              "incr": 0,
                                              COMPLEMENTS: ["pet_food",
                                                            "meat"]},
                                  "pet_food": {AMT_AVAILABLE: 0,
                                               UTIL_FUNC: "steep_util_func",
                                               "incr": 0,
                                               COMPLEMENTS: ["penguin",
                                                             "meat"]},
                                  "fuel": {AMT_AVAILABLE: 0,
                                           UTIL_FUNC: "steep_util_func",
                                           "incr": 0,
                                           COMPLEMENTS: ["truck", "land"]},
                                  "land": {AMT_AVAILABLE: 0,
                                           UTIL_FUNC: "steep_util_func",
                                           "incr": 0,
                                           COMPLEMENTS: ["truck", "fuel"]},
                                  "meat": {AMT_AVAILABLE: 0,
                                           UTIL_FUNC: "steep_util_func",
                                           "incr": 0,
                                           COMPLEMENTS: ["penguin",
                                                         "pet_food"]}},
                        "util": 0,
                        "pre_trade_util": 0,
                        "trades_with": "trader"})


def set_env_attrs():
    user_log_notif("Setting env attrs for " + MODEL_NAME)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    pa = init_props(MODEL_NAME, props, model_dir="capital")
    num_traders = get_prop('num_traders', DEF_NUM_TRADER)
    trader_group = Composite("trader", {"color": BLUE},
                             member_creator=create_trader,
                             props=pa,
                             num_members=num_traders)
    Env(MODEL_NAME,
        height=get_prop('grid_height', DEF_HEIGHT),
        width=get_prop('grid_width', DEF_WIDTH),
        members=[trader_group])
    set_env_attrs()
    num_resources = get_prop('num_resources', DEF_NUM_RESOURCES)
    MKT_GOODS = {
                 "truck": {AMT_AVAILABLE: num_resources,
                           UTIL_FUNC: "steep_util_func",
                           "incr": 0,
                           COMPLEMENTS: ["fuel", "land"]},
                 "penguin": {AMT_AVAILABLE: num_resources,
                             UTIL_FUNC: "steep_util_func",
                             "incr": 0,
                             COMPLEMENTS: ["pet_food",
                                           "meat"]},
                 "pet_food": {AMT_AVAILABLE: num_resources,
                              UTIL_FUNC: "steep_util_func",
                              "incr": 0,
                              COMPLEMENTS: ["penguin",
                                            "meat"]},
                 "fuel": {AMT_AVAILABLE: num_resources,
                          UTIL_FUNC: "steep_util_func",
                          "incr": 0,
                          COMPLEMENTS: ["truck", "land"]},
                 "land": {AMT_AVAILABLE: num_resources,
                          UTIL_FUNC: "steep_util_func",
                          "incr": 0,
                          COMPLEMENTS: ["truck", "fuel"]},
                 "meat": {AMT_AVAILABLE: num_resources,
                          UTIL_FUNC: "steep_util_func",
                          "incr": 0,
                          COMPLEMENTS: ["penguin",
                                        "pet_food"]}
                }
    for trader in trader_group:
        for i in range(len(MKT_GOODS) // num_traders):
            allocate_resources(trader_group[trader], MKT_GOODS)
        user_log_notif(repr(trader_group[trader]["goods"]))


def main():
    global trader_group

    set_up()

    if DEBUG2:
        get_env().user.tell(get_env().__repr__())

    get_env()()
    return 0


if __name__ == "__main__":
    main()
