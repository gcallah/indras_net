"""
Big box model for simulating the behaviors of consumers.
"""
import random
from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import BLACK, BLUE, GRAY, GREEN, RED, ORANGE, PURPLE
from indra.env import Env
from registry.registry import get_env, get_prop, get_group, get_env_attr
from indra.space import DEF_HEIGHT, DEF_WIDTH, get_neighbor
from indra.utils import init_props

MODEL_NAME = "bigbox"
NUM_OF_CONSUMERS = 50
NUM_OF_MP = 8
DEBUG = False

# Why these values? Why not params to model?
MIN_CONSUMER_SPENDING = 50
MAX_CONSUMER_SPENDING = 70

BIG_BOX = "Big box"
CONSUMER = "Consumer"
HOOD_SIZE = 2
MP_PREF = 0.1
PERIOD = 7
STANDARD = 200
MULTIPLIER = 10

bb_capital = 1000
bb_expense = 100
item_needed = None

cons_goods = ["books", "coffee", "groceries", "hardware", "meals"]

# we don't know where the expense and capital numbers come from!
#  (Prof. C & Dennis)
mp_stores = [
    Composite("Bookshop",
              attrs={"color": ORANGE, "per_expense": 20,
                     "init_capital": 90, "goods_sold": ["books"], }),
    Composite("Coffeeshop",
              attrs={"color": BLACK, "per_expense": 22,
                     "init_capital": 100, "goods_sold": ["coffee"], }),
    Composite("Grocery store",
              attrs={"color": GREEN, "per_expense": 23,
                     "init_capital": 100, "goods_sold": ["groceries"], }),
    Composite("Hardware",
              attrs={"color": RED, "per_expense": 18,
                     "init_capital": 110, "goods_sold": ["hardware"], }),
    Composite("Restaurant",
              attrs={"color": PURPLE, "per_expense": 25,
                     "init_capital": 100, "goods_sold": ["meals"], }),
]


def sells_good(store):
    """
    Check if the store sells what the consumer wants.
    If BB return True else return whether seller sells that type.
    We are going to use a global for item_needed: a kludge until
    we come up with something better.
    """
    global item_needed
    if str(store.primary_group()) == BIG_BOX:
        return True
    elif str(store.primary_group()) == CONSUMER:
        return False
    else:
        if store.is_active():
            if item_needed in store.primary_group().get_attr("goods_sold"):
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
    spending_power = random.randint(MIN_CONSUMER_SPENDING,
                                    MAX_CONSUMER_SPENDING)
    consumer_books = {"spending power": spending_power,
                      "last util": 0.0,
                      "item needed": get_rand_good()}
    return Agent(name + str(i), attrs=consumer_books, action=consumer_action)


def create_mp(store_grp, i):
    """
    Create a mom and pop store.
    """
    return Agent(name=str(store_grp) + " " + str(i),
                 attrs={"expense": store_grp.get_attr("per_expense"),
                        "capital": store_grp.get_attr("init_capital")},
                 action=mp_action)


def create_bb(name):
    """
    Create a big box store.
    """
    return Agent(name=name,
                 attrs={"expense": bb_expense,
                        "capital": get_env_attr("bb_capital")},
                 action=bb_action)


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
    # add mom and pop stores to groups:
    groups.extend(mp_stores)

    # loop over m&p store types and add stores:
    for i in range(num_mp):
        store_num = i % len(mp_stores)  # keep store_num in range
        mp_stores[store_num] += create_mp(mp_stores[store_num], i)

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
