"""
Big box model for simulating the behaviors of consumers.
"""

import random
from indra.utils import get_props
from indra.agent import Agent
from indra.composite import Composite
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.env import Env
from indra.display_methods import BLACK, BLUE, GRAY, GREEN, RED, TAN, YELLOW

MODEL_NAME = "bigbox"
NUM_OF_CONSUMERS = 50
NUM_OF_MP = 8
DEBUG = False

CONSUMER_INDX = 0
BB_INDX = 1

HOOD_SIZE = 2
MP_PREF = 0.1
PERIOD = 7
STANDARD = 200
MULTIPLIER = 10

EXPENSE_INDX = 0
CAPITAL_INDX = 1
COLOR_INDX = 2

town = None
groups = None
mp_pref = None
hood_size = None
bb_capital = 2000

# The data below creates store types with default values.
# "Store type":
# [expense, capital, color]
mp_stores = {"Bookshop": [65, 90, TAN],
             "Coffeeshop": [63, 100, BLACK],
             "Grocery store": [67, 100, GREEN],
             "Hardware": [60, 110, RED],
             "Restaurant": [60, 100, YELLOW]}


def sells_good(store, consumer, groups):
    """
    Check if the store sells what the consumer wants.
    If BB return True else return whether seller sells that type.
    """
    if store.primary_group() == groups[BB_INDX]:
        return True
    else:
        if consumer["item needed"] in store.name:
            return True
        return False


def get_rand_good_type():
    """
    Randomly select consumer's item needed
    after each run.
    """
    return random.choice(list(mp_stores.keys()))


def create_consumer(name, i, props=None):
    """
    Create consumers
    """
    spending_power = random.randint(50, 70)
    consumer_books = {"spending power": spending_power,
                      "last util": 0.0,
                      "item needed": get_rand_good_type()}
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
    global bb_capital

    bb_book = {"expense": 150,
               "capital": bb_capital}
    return Agent(name=name, attrs=bb_book, action=bb_action)


def bb_action(bb):
    """
    Deduct expense from the capital of big box and
    check if big box goes out of business.
    """
    bb["capital"] -= bb["expense"]
    if DEBUG:
        print("       ", bb, "has a capital of ", bb["capital"])
    if bb["capital"] <= 0:
        bb.die()
        if DEBUG:
            print("       ", bb, "is out of business.")
    return True


def get_util(store):
    """
    Get utility depending on the store type.
    """
    global mp_pref

    if store.primary_group() == groups[BB_INDX]:
        return calc_util(store)
    else:
        return calc_util(store) + mp_pref


def consumer_action(consumer):
    """
    Check shops near consumer and
    consumer decide where to shop at.
    """
    global hood_size
    nearby_neighbors = town.get_moore_hood(consumer,
                                           hood_size=hood_size)
    store_to_go = None
    max_util = 0.0
    for neighbors in nearby_neighbors:
        neighbor = nearby_neighbors[neighbors]
        if (neighbor.isactive() and (neighbor.primary_group()
           != groups[CONSUMER_INDX])):
            if sells_good(neighbor, consumer, groups):
                curr_store_util = get_util(neighbor)
                if curr_store_util > max_util:
                    max_util = curr_store_util
                    store_to_go = neighbor
    if store_to_go is not None:
        transaction(store_to_go, consumer)
        if DEBUG:
            print("     someone shopped at ", store_to_go)
    consumer["item needed"] = get_rand_good_type()
    return False


def transaction(store, consumer):
    """
    Add money to the store's capital from consumer.
    """
    store["capital"] += consumer["spending power"]
    # print("   ", consumer, "spend money at ", store)


def calc_util(stores):
    """
    calculate utility for stores.
    """
    return random.random()


def mp_action(mp):
    """
    deduct expenses from mom and pop stores and
    check if mom and pop store goes out or business.
    """

    mp["capital"] -= mp["expense"]
    if DEBUG:
        print("       ", mp, "has a capital of ", mp["capital"])
    if mp["capital"] <= 0:
        mp.die()
        if DEBUG:
            print("       ", mp, "is out of business.")
    return True


def town_action(town):
    """
    check the period and decide when to add
    the big box store
    """
    global groups
    global period

    if town.get_periods() == period:
        new_bb = create_bb("Big Box")
        groups[BB_INDX] += new_bb
        town.place_member(new_bb)


def set_up(props=None):
    """
    Create an Env for Big box.
    """
    global town
    global groups
    global mp_pref
    global hood_size
    global store_census
    global period
    global bb_capital

    pa = get_props(MODEL_NAME, props)

    width = pa.get("grid_width", DEF_WIDTH)
    height = pa.get("grid_height", DEF_HEIGHT)
    num_consumers = pa.get("consumer_num", NUM_OF_CONSUMERS)
    num_mp = pa.get("mp_num", NUM_OF_MP)
    mp_pref = pa.get("mp_pref", MP_PREF)
    hood_size = pa.get("hood_size", HOOD_SIZE)
    multiplier = pa.get("multiple", MULTIPLIER)
    bb_capital = multiplier * STANDARD
    period = pa.get("period", PERIOD)

    consumer_group = Composite("Consumer", {"color": GRAY},
                               member_creator=create_consumer,
                               num_members=num_consumers)
    bb_group = Composite("Big box", {"color": BLUE})
    groups = []
    groups.append(consumer_group)
    groups.append(bb_group)
    for stores in range(0, len(mp_stores)):
        store_name = list(mp_stores.keys())[stores]
        groups.append(Composite(store_name,
                                {"color": mp_stores[store_name][COLOR_INDX]}))
    for m in range(0, num_mp):
        rand = random.randint(2, len(groups) - 1)
        groups[rand] += create_mp(groups[rand], m)
    town = Env("Town",
               action=town_action,
               members=groups,
               height=height,
               width=width,
               props=pa)
    return (town, groups)


def bb_unrestorable(env):
    global town
    global groups
    global mp_pref
    global hood_size
    global store_census
    town = env
    mp_pref = env.props["mp_pref"]
    hood_size = env.props["hood_size"]


def main():
    global town
    global groups

    (town, groups) = set_up()
    town()
    return 0


if __name__ == "__main__":
    main()
