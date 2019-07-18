"""
Big box model for simulating the behaviors of consumers.
"""
import random

from propargs.propargs import PropArgs
from indra.utils import get_prop_path
from indra.agent import Agent
from indra.env import Env
from indra.composite import Composite
from indra.display_methods import BLUE, GRAY, RED

MODEL_NAME = "bigbox"
DEBUG = True

DEF_HEIGHT = 30
DEF_WIDTH = 30
NUM_OF_CONSUMERS = 150
NUM_OF_BB = 3
NUM_OF_MP = 6

UTIL = 0.15
MP_PREF = 0.1
ADJ_SCALING_FACTOR = 0.2
RADIUS = 2

CONSUMER_INDX = 0
BB_INDX = 1
MP_INDX = 2

town = None
groups = None
mp_pref = None
adj_scaling_factor = None
radius = None

mp_stores = {"books": [60, 30, 360, 60],
             "coffee": [30, 15, 180, 30],
             "groceries": [90, 45, 540, 90],
             "hardware": [80, 40, 480, 80],
             "meals": [45, 23, 270, 45]
             }
bb_store = [60, 25, 1000, 38]


def create_consumer(name):
    """
    Creates a consumer agent.
    Expense is the amount of money that the agent will spend
    in a store during a single period.
    """
    spending_power = random.randint(50, 80)
    item_needed = random.choice(list(mp_stores.keys()))
    characteristics = {"spending power": spending_power,
                       "last util": 0.0,
                       "item needed": item_needed}
    return Agent(name=name, attrs=characteristics, action=consumer_action)


def create_bb(name, util):
    """
    Creates a big box store agent.
    Does not have to randomly determine the store type
    because big box stores will sell everything.

    Expense is a list of ints that contain the corresponding values.

    Fixed expense is things like rent, electricity bills, etc.

    Variable expense is the cost of buying new inventory of goods.

    Capital is the money that is in the bank.

    Inventory is the amount of customers that the store can serve
    before it needs to restock and pay the variable expense.
    """
    expense = bb_store
    store_books = {"fixed expense": expense[0],
                   "variable expense": expense[1],
                   "capital": expense[2],
                   "inventory": [expense[3], expense[3]],
                   "util adj": util}
    return Agent(name=name,
                 attrs=store_books,
                 action=bb_action)


def create_mp(name, util):
    """
    Creates a mom and pop store agent.
    Store type (what the store will sell) is determined randomly
    and assigned as a name.

    Expense is a list of ints that contain the corresponding values.

    Fixed expense is things like rent, electricity bills, etc
    that will be taken out every period.

    Variable expense is the cost of buying new inventory of goods.

    Capital is the money that is in the bank.

    Inventory is the amount of customers that the store can serve
    before it needs to restock and pay the variable expense.
    """
    store_name = random.choice(list(mp_stores.keys()))
    expense = mp_stores[store_name]
    store_name = name + ": " + store_name
    store_books = {"fixed expense": expense[0],
                   "variable expense": expense[1],
                   "capital": expense[2],
                   "inventory": [expense[3], expense[3]],
                   "util adj": util}
    return Agent(name=store_name,
                 attrs=store_books,
                 action=mp_action)


def calc_util(stores):
    global adj_scaling_factor

    return (random.random() + stores.attrs["util adj"]) * adj_scaling_factor


def transaction(store, customer=None):
    """
    Calcuates the expense and the revenue of the store passed in
    after a transaction with the customer passed in.
    """
    if customer is not None:
        store.attrs["capital"] += customer.attrs["spending power"]
        store.attrs["inventory"][1] -= 1
        if store.attrs["inventory"][1] == 1:
            store.attrs["capital"] = (
                store.attrs["capital"]
                - store.attrs["variable expense"])
            store.attrs["inventory"][1] = (
                store.attrs["inventory"][1]
                + store.attrs["inventory"][0])
        if store.attrs["capital"] <= 0:
            print("     ", store, "is going out of buisness")
            store.die()
        if DEBUG:
            print("     ", store, "has a capital of", store.attrs["capital"],
                  "and inventory of", store.attrs["inventory"][1])
    else:
        store.attrs["capital"] -= store.attrs["fixed expense"]


def get_store_census(town):
    for bb in groups[1]:
        print(groups[1][bb], "has a capital of",
              groups[1][bb].attrs["capital"],
              "and inventory of", (groups[1][bb]).attrs["inventory"][1])
    for mp in groups[2]:
        print(groups[2][mp], "has a capital of",
              groups[2][mp].attrs["capital"],
              "and inventory of", (groups[2][mp]).attrs["inventory"][1])


def town_action(town):
    """
    The action that will be taken every turn.
    Loops through the town env and finds the customer agents.
    The customer agents are assigned their neighbors,
    and loop through the neighbors to determine which is a store
    and carries out the transaction.
    """
    global groups
    global mp_pref
    global radius

    for y in range(town.height):
        for x in range(town.width):
            curr_customer = town.get_agent_at(x, y)
            if (curr_customer is not None
                    and (curr_customer.primary_group()
                         == groups[CONSUMER_INDX])):
                nearby_neighbors = town.get_moore_hood(curr_customer,
                                                       radius=radius)
                store_to_go = None
                max_util = 0.0
                for neighbor in nearby_neighbors:
                    if (nearby_neighbors[neighbor].isactive()):
                        if (nearby_neighbors[neighbor].primary_group()
                           == groups[BB_INDX]):
                            curr_customer.has_acted = True
                            util = calc_util(nearby_neighbors[neighbor])
                            transaction(nearby_neighbors[neighbor])
                            if DEBUG:
                                print("Customer", curr_customer.get_pos())
                                print("   Shopping at big box store at",
                                      nearby_neighbors[neighbor].get_pos())
                                print("      Utility:", util)
                            if util > max_util:
                                max_util = util
                                store_to_go = nearby_neighbors[neighbor]
                        elif (nearby_neighbors[neighbor].primary_group()
                                == groups[MP_INDX]):
                            transaction(nearby_neighbors[neighbor])
                            if DEBUG:
                                print("Customer", curr_customer.get_pos())
                                print("   Checking if mom and pop at",
                                      nearby_neighbors[neighbor].get_pos(),
                                      "has",
                                      curr_customer.attrs["item needed"])
                            if (curr_customer.attrs["item needed"] in
                                    nearby_neighbors[neighbor].name):
                                curr_customer.has_acted = True
                                util = (calc_util(nearby_neighbors[neighbor])
                                        + mp_pref)
                                if DEBUG:
                                    print("     ", neighbor, "has",
                                          curr_customer.attrs["item needed"])
                                    print("      Utility:", util)
                                if util > max_util:
                                    max_util = util
                                    store_to_go = nearby_neighbors[neighbor]
                    else:
                        print("   ", nearby_neighbors[neighbor],
                              "is out of buisness")
                curr_customer.attrs["last utils"] = max_util
                if store_to_go is not None:
                    if DEBUG:
                        print("   Max utility was", max_util)
                        print("   Spending $"
                              + str(curr_customer.attrs["spending power"])
                              + " at " + str(store_to_go))
                    transaction(store_to_go, curr_customer)
    if DEBUG:
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
    global adj_scaling_factor
    global radius

    ds_file = get_prop_path(MODEL_NAME)
    if props is None:
        pa = PropArgs.create_props(MODEL_NAME, ds_file=ds_file)
    else:
        pa = PropArgs.create_props(MODEL_NAME,
                                   prop_dict=props)

    width = pa.get("grid_width", DEF_WIDTH)
    height = pa.get("grid_height", DEF_HEIGHT)
    num_consumers = pa.get("consumer_num", NUM_OF_CONSUMERS)
    num_bb = pa.get("bb_num", NUM_OF_BB)
    num_mp = pa.get("mp_num", NUM_OF_MP)
    util = pa.get("util", UTIL)
    mp_pref = pa.get("mp_pref", MP_PREF)
    adj_scaling_factor = pa.get("adj_scaling_factor", ADJ_SCALING_FACTOR)
    radius = pa.get("radius", RADIUS)

    consumer_group = Composite("Consumer", {"color": GRAY})
    mp_group = Composite("Mom and pop", {"color": RED})
    bb_group = Composite("Big box", {"color": BLUE})
    groups = []
    groups.append(consumer_group)
    groups.append(bb_group)
    groups.append(mp_group)
    for c in range(0, num_consumers):
        groups[CONSUMER_INDX] += create_consumer("Consumer " + str(c))
    for b in range(0, num_bb):
        groups[BB_INDX] += create_bb("Big box " + str(b), util)
    for m in range(0, num_mp):
        groups[MP_INDX] += create_mp("Mom and pop " + str(m), util)
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
