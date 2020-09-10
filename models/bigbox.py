"""
Big box model for simulating the behaviors of consumers.
"""
import random
from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import BLACK, BLUE, GRAY, GREEN, RED, ORANGE, YELLOW
from indra.env import Env
from registry.registry import get_env, get_prop, get_group, get_env_attr
from indra.space import DEF_HEIGHT, DEF_WIDTH, get_neighbor
from indra.utils import init_props

MODEL_NAME = "bigbox"
NUM_OF_CONSUMERS = 50
NUM_OF_MP = 8
DEBUG = False

CONSUMER_INDX = 0
BB_INDX = 1
BIG_BOX = "Big box"
CONSUMER = "Consumer"
HOOD_SIZE = 2
hood_size = 2
MP_PREF = 0.1
mp_pref = 0.1
PERIOD = 7
period = 7
STANDARD = 200
MULTIPLIER = 10

EXPENSE_INDX = 0
CAPITAL_INDX = 1
COLOR_INDX = 2
GOOD_INDX = 3

bb_capital = 1000
bb_expense = 100
item_needed = None

# The data below creates store types with default values.
# "Store type":
# [expense, capital, color, goods sold]
cons_goods = ["books", "coffee", "groceries", "hardware", "meal"]
bs_goods = ["books"]
cs_goods = ["coffee"]
gs_goods = ["groceries"]
hw_goods = ["hardware"]
rs_goods = ["meal"]
mp_stores = {"Bookshop": [20, 90, ORANGE, bs_goods],
             "Coffeeshop": [22, 100, BLACK, cs_goods],
             "Grocery store": [23, 100, GREEN, gs_goods],
             "Hardware": [18, 110, RED, hw_goods],
             "Restaurant": [25, 100, YELLOW, rs_goods]}


def sells_good(store):
    """
    Check if the store sells what the consumer wants.
    If BB return True else return whether seller sells that type.
    We are going to use a global for item_needed: a kludge until
    we come up with something better.
    """
    global item_needed
    if store.primary_group() == get_group(BIG_BOX):
        return True
    else:
        store_name = store.name
        str_name = ""
        for ch in store_name:
            if ch.isalpha():
                str_name = "".join([str_name, ch])
        if (str_name in mp_stores.keys()):
            active = store.is_active
            if active and item_needed in mp_stores[str_name][GOOD_INDX]:
                return True
        return False


# should we have a separate list of goods that consumers might want?
def get_rand_good():
    """
    Randomly select consumer's item needed
    after each run.
    """
    return random.choice(cons_goods)


def create_consumer(name, i, props=None):
    """
    Create consumers
    """
    spending_power = random.randint(50, 70)
    consumer_books = {"spending power": spending_power,
                      "last util": 0.0,
                      "item needed": get_rand_good()}
    return Agent(name + str(i), attrs=consumer_books, action=consumer_action)


def create_mp(store_type, i):
    """
    Create a mom and pop store.
    """
    expense = mp_stores[str(store_type)]
    name = str(store_type) + " " + str(i)
    store_books = {"expense": expense[EXPENSE_INDX],
                   "capital": expense[CAPITAL_INDX]}
    return Agent(name=name, attrs=store_books, action=mp_action)


def create_bb(name):
    """
    Create a big box store.
    """
    bb_book = {"expense": bb_expense,
               "capital": get_env_attr("bb_capital")}
    return Agent(name=name, attrs=bb_book, action=bb_action)


def bb_action(bb, **kwargs):
    """
    Deduct expenses from the capital of big box and
    check if big box goes out of business.
    """
    return common_action(bb)


def get_util(store):
    """
    Get utility depending on the store type.
    """
    if store.primary_group() == get_group(BIG_BOX):
        return calc_util(store)
    else:
        return calc_util(store) + get_env_attr("mp_pref")


def consumer_action(consumer, **kwargs):
    """
    Check shops near consumer and
    consumer decide where to shop at.
    """
    global item_needed
    item_needed = consumer["item needed"]
    shop_at = get_neighbor(consumer, pred=sells_good)
    if shop_at is None:
        return False

    max_util = 0.0
    curr_store_util = get_util(shop_at)
    if curr_store_util > max_util:
        max_util = curr_store_util
    transaction(shop_at, consumer)
    if DEBUG:
        print("     someone shopped at ",   shop_at)
    consumer["item needed"] = get_rand_good()
    return False


def transaction(store, consumer):
    """
    Add money to the store's capital from consumer.
    """
    store["capital"] += consumer["spending power"]


def calc_util(stores):
    """
    calculate utility for stores.
    """
    return random.random()


def mp_action(mp, **kwargs):
    """
    Deduct expenses from mom and pop stores and
    check if mom and pop store goes out of business.
    """

    return common_action(mp)


def common_action(business):
    """
    Common action to deduct expenses and
    check whether the entity goes out of business
    """
    business["capital"] -= business["expense"]
    if DEBUG:
        print("       ", business, "has a capital of ", business["capital"])
    if business["capital"] <= 0:
        business.die()
        if DEBUG:
            print("       ", business, "is out of business.")
    return True


def town_action(town, **kwargs):
    """
    check the period and decide when to add
    the big box store
    """
    box = get_env()
    if town.get_periods() == box.get_attr("period"):
        new_bb = create_bb("Big Box")
        box.attrs["bb_group"] += new_bb
        town.place_member(new_bb)


def set_up(props=None):
    """
    Create an Env for Big box.
    """

    init_props(MODEL_NAME, props)

    width = get_prop("grid_width", DEF_WIDTH)
    height = get_prop("grid_height", DEF_HEIGHT)
    num_consumers = get_prop("consumer_num", NUM_OF_CONSUMERS)
    num_mp = get_prop("mp_num", NUM_OF_MP)
    mp_pref = get_prop("mp_pref", MP_PREF)
    hood_size = get_prop("hood_size", HOOD_SIZE)
    multiplier = get_prop("multiple", MULTIPLIER)
    bb_capital = multiplier * STANDARD
    period = get_prop("period", PERIOD)

    consumer_group = Composite(CONSUMER, {"color": GRAY},
                               member_creator=create_consumer,
                               num_members=num_consumers)
    bb_group = Composite(BIG_BOX, {"color": BLUE})
    groups = [consumer_group, bb_group]
    for stores in range(0, len(mp_stores)):
        store_name = list(mp_stores.keys())[stores]
        groups.append(Composite(store_name,
                                {"color": mp_stores[store_name][COLOR_INDX]}))
    for kind in range(0, len(mp_stores)):
        groups[kind+2] += create_mp(groups[kind+2], kind)
    if num_mp > len(mp_stores):
        for mp in range(len(mp_stores), num_mp):
            rand = random.randint(2, len(groups) - 1)
            groups[rand] += create_mp(groups[rand], mp)
    box = Env(MODEL_NAME,
              action=town_action,
              members=groups,
              height=height,
              width=width)
    box.set_attr("consumer_group", consumer_group)
    box.set_attr("bb_group", bb_group)
    box.set_attr("hood_size", hood_size)
    box.set_attr("mp_pref", mp_pref)
    box.set_attr("period", period)
    box.set_attr("bb_capital", bb_capital)


def main():

    set_up()
    get_env()()
    return 0


if __name__ == "__main__":
    main()
