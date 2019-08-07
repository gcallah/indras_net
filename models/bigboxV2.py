"""
Second version of Big box model for simulating the behaviors of consumers.
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

CONSUMER_INDX = 0
BB_INDX = 1

RADIUS = 2
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
radius = None
store_census = None

# The data below creates store types with default values.
# "Store type":
# [expense, capital, color]
mp_stores = {"Bookshop": [45, 105, TAN],
             "Coffeeshop": [23, 100, BLACK],
             "Grocery store": [67, 100, GREEN],
             "Hardware": [60, 110, RED],
             "Restaurant": [40, 100, YELLOW]}


def sells_good(store, consumer):
    if store.primary_group() == groups[BB_INDX]:
        return True
    else:
        if consumer["item needed"] in store.name:
            return True
        return False
    # if BB return True else return seller sells that type


def get_rand_good_type():
    return random.choice(list(mp_stores.keys()))


def create_consumer(name, i, props=None):
    spending_power = random.randint(70, 100)
    consumer_books = {"spending power": spending_power,
                      "last util": 0.0,
                      "item needed": get_rand_good_type()}
    return Agent(name + str(i), attrs=consumer_books, action=consumer_action)


def create_mp(store_type, i):
    expense = mp_stores[str(store_type)]
    name = str(store_type) + " " + str(i)
    store_books = {"expense": expense[EXPENSE_INDX],
                   "capital": expense[CAPITAL_INDX]}
    return Agent(name=name, attrs=store_books, action=mp_action)


def create_bb(name):
    global multiplier

    bb_book = {"expense": 150,
               "capital": multiplier * STANDARD}
    return Agent(name=name, attrs=bb_book, action=bb_action)


def bb_action(bb):
    bb["capital"] -= bb["expense"]
    return True


def get_util(store):
    global mp_pref

    if store.primary_group() == groups[BB_INDX]:
        return calc_util(store)
    else:
        return calc_util(store) + mp_pref


def consumer_action(consumer):
    global radius
    nearby_neighbors = town.get_moore_hood(consumer,
                                           radius=radius)
    store_to_go = None
    max_util = 0.0
    for neighbors in nearby_neighbors:
        neighbor = nearby_neighbors[neighbors]
        if (neighbor.isactive()
                and neighbor.primary_group()
            != groups[CONSUMER_INDX]):
            if sells_good(neighbor, consumer):
                curr_store_util = get_util(neighbor)
                if curr_store_util > max_util:
                    max_util = curr_store_util
                    store_to_go = neighbor
            # collapse if and else to single case by
            #  1) make bb sell all goods and
            #  2) make store cough up util and add mp_pref in there
    if store_to_go is not None:
        transaction(store_to_go, consumer)
    consumer["item needed"] = get_rand_good_type()
    return False


def transaction(store, consumer):
    store["capital"] += consumer["spending power"]
    # print("   ", consumer, "spend money at ", store)


def calc_util(stores):
    return random.random()


def mp_action(mp):
    mp["capital"] -= mp["expense"]
    # print("    ", mp, "has a capital of ", mp["capital"])
    return True


def town_action(town):
    global groups
    global period

    if town.get_periods() == period:
        new_bb = create_bb("Big Box")
        groups[BB_INDX] += new_bb
        town.place_member(new_bb)
    for y in range(town.height):
        for x in range(town.width):
            curr_store = town.get_agent_at(x, y)
            if (curr_store is not None and curr_store.primary_group()
               != groups[CONSUMER_INDX]):
                if curr_store["capital"] <= 0:
                    curr_store.die()
                    print("       ", curr_store, "is out of business.")


def set_up(props=None):
    global town
    global groups
    global mp_pref
    global radius
    global store_census
    global period
    global multiplier

    pa = get_props(MODEL_NAME, props)

    width = pa.get("grid_width", DEF_WIDTH)
    height = pa.get("grid_height", DEF_HEIGHT)
    num_consumers = pa.get("consumer_num", NUM_OF_CONSUMERS)
    num_mp = pa.get("mp_num", NUM_OF_MP)
    mp_pref = pa.get("mp_pref", MP_PREF)
    radius = pa.get("radius", RADIUS)
    store_census = pa.get("store_census", False)
    multiplier = pa.get("multiple", MULTIPLIER)
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


def main():
    global town
    global groups

    (town, groups) = set_up()
    town()
    return 0


if __name__ == "__main__":
    main()
