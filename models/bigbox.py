"""
Big box model for simulating the behaviors of consumers.
"""

from propargs.propargs import PropArgs
from indra.utils import get_prop_path
from indra.agent import Agent
from indra.env import Env
from indra.composite import Composite
from indra.display_methods import RED, BLUE

MODEL_NAME = "Big Box"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_WIDTH = 20
DEF_HEIGHT = 20

CONSUMER = 100
MP = 5

town = None
groups = None


def create_consumer(name, expense):
    """
    Create a consumer agent.
    """
    balance = {"expense": expense}
    return Agent(name=name, attrs=balance, action=consumer_action)


def create_mp(name, fixed_expense, variable_expense, capital, inventory_size):
    """
    Create a mom and pop store agent.
    Fixed expense is things like rent, electricity bills, etc.
    Variable expense is the cost of buying new inventory of goods.
    Capital is the money that is in the bank.
    Inventory size is the amounf of customers that the store can serve
    in a single period.
    """
    store_books = {"fixed expense": fixed_expense,
                   "variable expense": variable_expense,
                   "capital": capital, "inventory": [inventory_size, 0]}
    return Agent(name=name, attrs=store_books, action=mp_action)


def town_action(town):
    """
    The action that will be taken every turn.
    Loops through the town env, finds the store agents and
    how many customer agents are in its moore hood,
    and calculates the transaction.
    """
    global groups

    for y in range(town.height):
        for x in range(town.width):
            curr_store = town.get_agent_at(x, y)
            if (curr_store is not None
                    and curr_store.primary_group() == groups[1]):
                nearby_customers = town.get_moore_hood(curr_store)
                if DEBUG:
                    print(curr_store, "capital:", curr_store.attrs["capital"])
                    print("     Num of customers:", len(nearby_customers))
                    print("     Inventory size before:",
                          curr_store.attrs["inventory"][1])
                for customer in nearby_customers:
                    if nearby_customers[customer].primary_group() == groups[0]:
                        curr_store.attrs["capital"] = (
                            (nearby_customers[customer]).attrs["expense"]
                            + curr_store.attrs["capital"])
                        curr_store.attrs["inventory"][1] += 1
                curr_store.attrs["capital"] = (
                    curr_store.attrs["capital"]
                    - curr_store.attrs["fixed expense"])
                if DEBUG:
                    print("     Inventory size after:",
                          curr_store.attrs["inventory"][1])
                    print("     Capital after:", curr_store.attrs["capital"])
                if (curr_store.attrs["inventory"][1]
                   >= curr_store.attrs["inventory"][0] - 8):
                    curr_store.attrs["capital"] = (
                        curr_store.attrs["capital"]
                        - curr_store.attrs["variable expense"])
                    curr_store.attrs["inventory"][1] = (
                        curr_store.attrs["inventory"][1]
                        - curr_store.attrs["inventory"][0])
                if curr_store.attrs["capital"] <= 0:
                    curr_store.die()


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

    ds_file = get_prop_path(MODEL_NAME)
    if props is None:
        pa = PropArgs.create_props(MODEL_NAME,
                                   ds_file=ds_file)
    else:
        pa = PropArgs.create_props(MODEL_NAME,
                                   prop_dict=props)
    width = pa.get('grid_width', DEF_WIDTH)
    height = pa.get('grid_height', DEF_HEIGHT)
    consumer_group = Composite("Consumer", {"color": BLUE})
    mp_group = Composite("Mom and pop", {"color": RED})
    groups = []
    groups.append(consumer_group)
    groups.append(mp_group)
    for i in range(0, CONSUMER):
        groups[0] += create_consumer('Consumer ' + str(i), 50)
    for j in range(0, MP):
        groups[1] += create_mp('Mom and pop ' + str(j), 80, 30, 1000, 30)
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
