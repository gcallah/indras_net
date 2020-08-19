"""
A complementary model.
Places two groups of agents in the enviornment randomly
and moves them around randomly.
"""

from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import BLUE
from indra.env import Env
from registry.execution_registry import CLI_EXEC_KEY, \
    EXEC_KEY, get_exec_key
from registry.registry import get_env, get_prop, user_log_notif
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.utils import init_props
from capital.trade_utils import seek_a_trade_w_comp
from capital.trade_utils import UTIL_FUNC, AMT_AVAIL
import capital.good_structure as gs
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


def create_graph():
    goods = gs.GoodStruct()
    goods.add_node("truck")
    goods.add_node("fuel")
    goods.add_node("land")

    goods.add_edge("truck", "fuel", weight=4)
    goods.add_edge("truck", "land", weight=4)

    goods.add_edge("fuel", "truck", weight=4)
    goods.add_edge("fuel", "land", weight=4)

    goods.add_edge("land", "truck", weight=4)
    goods.add_edge("land", "fuel", weight=4)

    goods.add_node("penguin")
    goods.add_node("pet_food")
    goods.add_node("meat")

    goods.add_edge("penguin", "pet_food", weight=4)
    goods.add_edge("penguin", "meat", weight=4)

    goods.add_edge("pet_food", "penguin", weight=4)
    goods.add_edge("pet_food", "meat", weight=4)

    goods.add_edge("meat", "penguin", weight=4)
    goods.add_edge("meat", "pet_food", weight=4)

    goods.draw_graph()
    return goods


def create_trader(name, i, **kwargs):
    execution_key = get_exec_key(kwargs=kwargs)
    return Agent(name + str(i), action=seek_a_trade_w_comp,
                 attrs={"goods": {"truck": {AMT_AVAIL: 0,
                                            UTIL_FUNC: "steep_util_func",
                                            "incr": 0,
                                            COMPLEMENTS: ["fuel", "land"]},
                                  "penguin": {AMT_AVAIL: 0,
                                              UTIL_FUNC: "steep_util_func",
                                              "incr": 0,
                                              COMPLEMENTS: ["pet_food",
                                                            "meat"]},
                                  "pet_food": {AMT_AVAIL: 0,
                                               UTIL_FUNC: "steep_util_func",
                                               "incr": 0,
                                               COMPLEMENTS: ["penguin",
                                                             "meat"]},
                                  "fuel": {AMT_AVAIL: 0,
                                           UTIL_FUNC: "steep_util_func",
                                           "incr": 0,
                                           COMPLEMENTS: ["truck", "land"]},
                                  "land": {AMT_AVAIL: 0,
                                           UTIL_FUNC: "steep_util_func",
                                           "incr": 0,
                                           COMPLEMENTS: ["truck", "fuel"]},
                                  "meat": {AMT_AVAIL: 0,
                                           UTIL_FUNC: "steep_util_func",
                                           "incr": 0,
                                           COMPLEMENTS: ["penguin",
                                                         "pet_food"]}},
                        "graph": create_graph(),
                        "util": 0,
                        "pre_trade_util": 0,
                        "trades_with": "trader"}, execution_key=execution_key)


def set_env_attrs(execution_key=CLI_EXEC_KEY):
    user_log_notif("Setting env attrs for " + MODEL_NAME)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    pa = init_props(MODEL_NAME, props, model_dir="capital")
    execution_key = int(props[EXEC_KEY].val) \
        if props is not None else CLI_EXEC_KEY
    num_traders = get_prop('num_traders', DEF_NUM_TRADER,
                           execution_key=execution_key)
    trader_group = Composite("trader", {"color": BLUE},
                             member_creator=create_trader,
                             props=pa,
                             num_members=num_traders,
                             execution_key=execution_key)
    Env(MODEL_NAME,
        height=get_prop('grid_height', DEF_HEIGHT,
                        execution_key=execution_key),
        width=get_prop('grid_width', DEF_WIDTH, execution_key=execution_key),
        members=[trader_group], execution_key=execution_key)
    set_env_attrs(execution_key=execution_key)
    num_resources = get_prop('num_resources', DEF_NUM_RESOURCES,
                             execution_key=execution_key)
    MKT_GOODS = {
        "truck": {AMT_AVAIL: num_resources,
                  UTIL_FUNC: "steep_util_func",
                  "incr": 0,
                  COMPLEMENTS: ["fuel", "land"]},
        "penguin": {AMT_AVAIL: num_resources,
                    UTIL_FUNC: "steep_util_func",
                    "incr": 0,
                    COMPLEMENTS: ["pet_food",
                                  "meat"]},
        "pet_food": {AMT_AVAIL: num_resources,
                     UTIL_FUNC: "steep_util_func",
                     "incr": 0,
                     COMPLEMENTS: ["penguin",
                                   "meat"]},
        "fuel": {AMT_AVAIL: num_resources,
                 UTIL_FUNC: "steep_util_func",
                 "incr": 0,
                 COMPLEMENTS: ["truck", "land"]},
        "land": {AMT_AVAIL: num_resources,
                 UTIL_FUNC: "steep_util_func",
                 "incr": 0,
                 COMPLEMENTS: ["truck", "fuel"]},
        "meat": {AMT_AVAIL: num_resources,
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
    set_up()

    if DEBUG2:
        get_env().user.tell(get_env().__repr__())

    get_env()()
    return 0


if __name__ == "__main__":
    main()
