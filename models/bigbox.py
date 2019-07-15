"""
Big box model for simulating the behaviors of consumers.
"""

from propargs.propargs import PropArgs
from indra.utils import get_prop_path
from indra.agent import Agent
from indra.env import Env
from indra.composite import Composite
from indra.display_methods import GRAY, RED, BLUE

MODEL_NAME = "Big Box"
DEBUG = True

DEF_WIDTH = 30
DEF_HEIGHT = 30

CONSUMER_NUM = 150
MP_NUM = 3
BB_NUM = 2

town = None
groups = None
mp_shops = {"Coffee shop": [30, 20, 700, 20],
            "Grocery store": [80, 30, 1000, 30],
            "Restaurant": [50, 25, 800, 25]}
bb_shops = {"Coffee shop": [60, 40, 1400, 40],
            "Grocery store": [160, 60, 2000, 60],
            "Restaurant": [100, 50, 1600, 50]}
shops_lst = ["Coffee shop",
             "Grocery store",
             "Restaurant"]


def create_consumer(name, expense, store_pref=None):
    """
    Creates a consumer agent.
    Expense is the amount of money that the agent will spend
    in a store during a single period.
    """
    balance = {"expense": expense}
    return Agent(name=name, attrs=balance, action=consumer_action)


def create_mp(name, store_type, expense):
    """
    Creates a mom and pop store agent.
    Expense is a list of ints that contain the corresponding values.
    Fixed expense is things like rent, electricity bills, etc.
    Variable expense is the cost of buying new inventory of goods.
    Capital is the money that is in the bank.
    Inventory is the amount of customers that the store can serve
    in a single period.
    """
    store_books = {"fixed expense": expense[0],
                   "variable expense": expense[1],
                   "capital": expense[2],
                   "inventory": [expense[3], expense[3]]}
    return Agent(name=(store_type + ": " + name),
                 attrs=store_books,
                 action=mp_action)


def create_bb(name, store_type, expense):
    store_books = {"fixed expense": expense[0],
                   "variable expense": expense[1],
                   "capital": expense[2],
                   "inventory": [expense[3], expense[3]]}
    return Agent(name=(store_type + ": " + name),
                 attrs=store_books,
                 action=mp_action)


def town_action(town):
    """
    The action that will be taken every turn.
    Loops through the town env, finds the store agents and
    how many customer agents are in its Moore neighborhood,
    and calculates the transaction.
    """
    global groups

    for y in range(town.height):
        for x in range(town.width):
            curr_store = town.get_agent_at(x, y)
            if (curr_store is not None
                    and curr_store.primary_group() != groups[0]):
                nearby_customers = town.get_moore_hood(curr_store, radius=2)
                if DEBUG:
                    print(curr_store)
                    print("     Location:", curr_store.get_pos())
                    print("     Capital:", curr_store.attrs["capital"])
                    print("     Inventory size before:",
                          curr_store.attrs["inventory"][1])
                num_nearby_customers = 0
                for customer in nearby_customers:
                    if nearby_customers[customer].primary_group() == groups[0]:
                        num_nearby_customers += 1
                        curr_store.attrs["capital"] += (
                            (nearby_customers[customer]).attrs["expense"])
                        curr_store.attrs["inventory"][1] -= 1
                curr_store.attrs["capital"] = (
                    curr_store.attrs["capital"]
                    - curr_store.attrs["fixed expense"])
                if DEBUG:
                    print("     Num of customers:", num_nearby_customers)
                    print("     Inventory size after:",
                          curr_store.attrs["inventory"][1])
                    print("     Fixed expense:",
                          curr_store.attrs["fixed expense"])
                    print("     Capital after:", curr_store.attrs["capital"])
                if (curr_store.attrs["inventory"][1] - num_nearby_customers
                   <= 0):
                    curr_store.attrs["capital"] = (
                        curr_store.attrs["capital"]
                        - curr_store.attrs["variable expense"])
                    curr_store.attrs["inventory"][1] = (
                        curr_store.attrs["inventory"][1]
                        + curr_store.attrs["inventory"][0])
                if curr_store.attrs["capital"] <= 0:
                    print("     ", curr_store, "is out of buisness")
                    # curr_store.die()


def consumer_action(agent):
    global town

    town.stay = False
    town.place_member(agent)
    town.stay = True


def mp_action(agent):
    pass


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    global town
    global groups
    global shops

    ds_file = get_prop_path(MODEL_NAME)
    if props is None:
        pa = PropArgs.create_props(MODEL_NAME,
                                   ds_file=ds_file)
    else:
        pa = PropArgs.create_props(MODEL_NAME,
                                   prop_dict=props)
    width = pa.get('grid_width', DEF_WIDTH)
    height = pa.get('grid_height', DEF_HEIGHT)
    consumer_group = Composite("Consumer", {"color": GRAY})
    mp_group = Composite("Mom and pop", {"color": RED})
    bb_group = Composite("Big box", {"color": BLUE})
    groups = []
    groups.append(consumer_group)
    groups.append(mp_group)
    groups.append(bb_group)
    for c in range(0, CONSUMER_NUM):
        groups[0] += create_consumer("Consumer " + str(c), 50)
    for m in range(0, MP_NUM):
        groups[1] += create_mp("Mom and pop " + str(m),
                               shops_lst[0], mp_shops[shops_lst[0]])
        groups[1] += create_mp("Mom and pop " + str(m),
                               shops_lst[1], mp_shops[shops_lst[1]])
        groups[1] += create_mp("Mom and pop " + str(m),
                               shops_lst[2], mp_shops[shops_lst[2]])
    for b in range(0, BB_NUM):
        groups[2] += create_mp("Big box " + str(b),
                               shops_lst[0], bb_shops[shops_lst[0]])
        groups[2] += create_mp("Big box " + str(b),
                               shops_lst[1], bb_shops[shops_lst[1]])
        groups[2] += create_mp("Big box " + str(b),
                               shops_lst[2], bb_shops[shops_lst[2]])
    town = Env("Town",
               action=town_action,
               members=groups,
               height=height,
               width=width,
               props=pa)
    town.stay_in_place(True)
    return (town, groups)


def main():
    global town
    global groups

    (town, groups) = set_up()
    town()
    return 0


if __name__ == "__main__":
    main()
