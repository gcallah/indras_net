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
DEBUG = False

NUM_OF_CONSUMERS = 180
NUM_OF_BB = 4
NUM_OF_MP = 8

MP_PREF = 0.1
RADIUS = 2

CONSUMER_INDX = 0
BB_INDX = 1
MP_INDX = 2

town = None
groups = None
mp_pref = None
radius = None
store_census = None

# The data below creates store types with default values.
# "Store type":
# [fixed expense, variable expense, capital, inventory,
# color, consumers visited]
mp_stores = {"Mom and pop: Books": [45, 30, 360, 60, TAN, 0],
             "Mom and pop: Coffee": [23, 15, 180, 30, BLACK, 0],
             "Mom and pop: Groceries": [67, 45, 540, 90, GREEN, 0],
             "Mom and pop: Hardware": [60, 40, 480, 80, RED, 0],
             "Mom and pop: Meals": [40, 23, 270, 45, YELLOW, 0]}

COLOR_INDEX = 4


bb_store = [60, 25, 480, 90, 0]
# [Fixed expense, variable expense, capital, inventory, consumers visited]


def create_consumer(name):
    """
    Creates a consumer agent.
    Expense is the amount of money that the agent will spend
        in a store during a single period.
    """
    spending_power = random.randint(70, 100)
    item_needed = random.choice(list(mp_stores.keys()))
    consumer_books = {"spending power": spending_power,
                      "last util": 0.0,
                      "item needed": item_needed}
    return Agent(name=name, attrs=consumer_books, action=consumer_action)


def create_bb(name):
    """
    Creates a big box store agent.
    Does not have to randomly determine the store type
        because big box stores will sell everything.
    Expense is a list of ints that contain the corresponding values.
    Fixed expense is things like rent, electricity bills, etc
        that will be taken out every period.
    Variable expense is the cost of buying new inventory of goods.
    Capital is the money that is in the bank.
    Inventory is the amount of consumer that the store can serve
        before it needs to restock and pay the variable expense.
    """
    expense = bb_store
    store_books = {"fixed expense": expense[0],
                   "variable expense": expense[1],
                   "capital": expense[2],
                   "inventory": [expense[3], expense[3]],
                   "visited": expense[4]}
    return Agent(name=name, attrs=store_books, action=bb_action)


def create_mp(store_type, i):
    """
    Creates a mom and pop store agent.
    Store type (what the store will sell) is determined randomly
    and assigned as a name.
    Expense is a list of ints that contain the corresponding values.
    Fixed expense is things like rent, electricity bills, etc
        that will be taken out every period.
    Variable expense is the cost of buying new inventory of goods.
    Capital is the money that is in the bank.
    Inventory is the amount of consumers that the store can serve
        before it needs to restock and pay the variable expense.
    """
    expense = mp_stores[str(store_type)]
    name = str(store_type) + " " + str(i)
    store_books = {"fixed expense": expense[0],
                   "variable expense": expense[1],
                   "capital": expense[2],
                   "inventory": [expense[3], expense[3]],
                   "visited": expense[5]}
    return Agent(name=name, attrs=store_books, action=mp_action)


def calc_util(stores):
    return random.random()


def transaction(store, consumer):
    """
    Calcuates the expense and the revenue of the store passed in
        after a transaction with the consumer passed in.
    """
    store["visited"] += 1
    store["capital"] += consumer["spending power"]
    store["inventory"][1] -= 1
    if store["inventory"][1] == 1:
        store["capital"] -= (
            store["variable expense"])
        store["inventory"][1] += (
            store["inventory"][0])
    if store["capital"] <= 0:
        print("     ", store, "is out of buisness")
        store.die()
    if DEBUG:
        print("     ", store, "has a capital of", store["capital"],
              "and inventory of", store["inventory"][1])


def get_store_census(town):
    to_print = " ".join(["\n==================\n",
                         "Store census for period ",
                         str(town.get_periods()), ":\n",
                         "==================\n"])
    for i in range(1, 6):
        for store in groups[i]:
            if groups[i][store]["capital"] > -1:
                to_print = " ".join([to_print, str(groups[i][store]),
                                     "\n  Capital: ",
                                     str(groups[i][store]["capital"]),
                                     "\n  Inventory: ",
                                     str((groups[i][store]
                                          )["inventory"][1]),
                                     "\n  ",
                                     str((groups[i][store])["visited"])])
                if (groups[i][store])["visited"] == 1:
                    to_print = " ".join([to_print,
                                         " consumer visited this store",
                                         " in the last period.\n"])
                else:
                    to_print = " ".join([to_print,
                                         " consumers visited this store",
                                         " in the last period.\n"])
    town.user.tell(to_print)


def town_action(town):
    """
    The action that will be taken every turn.
    Loops through the town env and finds the consumer agents.
    The consumer agents are assigned their neighbors,
        and loop through the neighbors to determine which is a store
        and carries out the transaction.
    """
    global groups
    global mp_pref
    global radius
    global store_census

    for y in range(town.height):
        for x in range(town.width):
            curr_consumer = town.get_agent_at(x, y)
            if (curr_consumer is not None
                    and (curr_consumer.primary_group()
                         == groups[CONSUMER_INDX])):
                if DEBUG:
                    print(" ".join(["Checking around consumer",
                                    str(curr_consumer.get_pos()), "..."]))
                nearby_neighbors = town.get_moore_hood(curr_consumer,
                                                       radius=radius)
                store_to_go = None
                max_util = 0.0
                for neighbors in nearby_neighbors:
                    neighbor = nearby_neighbors[neighbors]
                    if (neighbor.isactive()
                            and neighbor.primary_group()
                        != groups[CONSUMER_INDX]
                            and neighbor["capital"] > -1):
                        curr_store_util = 0.0
                        if neighbor["visited"] > 0:
                            neighbor["visited"] = 0
                        neighbor["capital"] -= (
                            neighbor["fixed expense"])
                        if (neighbor.primary_group()
                           == groups[BB_INDX]):
                            curr_store_util = calc_util(neighbor)
                            if DEBUG:
                                print(" ".join(["   Getting util from bb ",
                                                str(neighbor.get_pos()), "\n",
                                                "      Utility from big box:",
                                                str(curr_store_util)]))
                        else:
                            if DEBUG:
                                print("   Checking if mom and pop at "
                                      + str(neighbor.get_pos()) + " has "
                                      + curr_consumer["item needed"]
                                      + "...")
                            if (curr_consumer["item needed"] in
                                    neighbor.name):
                                curr_store_util = (calc_util(neighbor)
                                                   + mp_pref)
                                if DEBUG:
                                    print("     ", neighbor, "has item")
                                    print("      Getting util from mp"
                                          + str(neighbor.get_pos()) + "...")
                                    print("      Utility from mom and pop:",
                                          curr_store_util)
                            else:
                                if DEBUG:
                                    print("     ", neighbor,
                                          "does not have item")
                        if curr_store_util > max_util:
                            max_util = curr_store_util
                            store_to_go = neighbor
                curr_consumer["last utils"] = max_util
                if store_to_go is not None:
                    if DEBUG:
                        print("   Max utility was", max_util)
                        print("   Spending $"
                              + str(curr_consumer["spending power"])
                              + " at " + str(store_to_go) + "...")
                    transaction(store_to_go, curr_consumer)
    if DEBUG or store_census:
        get_store_census(town)


def consumer_action(consumer):
    return False


def bb_action(bb):
    return True


def mp_action(mp):
    return True


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    global town
    global groups
    global mp_pref
    global radius
    global store_census

    pa = get_props(MODEL_NAME, props)

    width = pa.get("grid_width", DEF_WIDTH)
    height = pa.get("grid_height", DEF_HEIGHT)
    num_consumers = pa.get("consumer_num", NUM_OF_CONSUMERS)
    num_bb = pa.get("bb_num", NUM_OF_BB)
    num_mp = pa.get("mp_num", NUM_OF_MP)
    mp_pref = pa.get("mp_pref", MP_PREF)
    radius = pa.get("radius", RADIUS)
    store_census = pa.get("store_census", False)

    consumer_group = Composite("Consumer", {"color": GRAY})
    bb_group = Composite("Big box", {"color": BLUE})
    groups = []
    groups.append(consumer_group)
    groups.append(bb_group)
    for stores in range(0, len(mp_stores)):
        store_name = list(mp_stores.keys())[stores]
        groups.append(Composite(store_name,
                                {"color": mp_stores[store_name][COLOR_INDEX]}))
    for c in range(0, num_consumers):
        groups[CONSUMER_INDX] += create_consumer("Consumer " + str(c))
    for b in range(0, num_bb):
        groups[BB_INDX] += create_bb("Big box " + str(b))
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
