"""
    This is the fashion model re-written in indra.
"""

# from indra.utils import get_prop_path
from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env
from indra.display_methods import RED, BLUE

MODEL_NAME = "Big Box"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

CONSUMER = 100
MP = 5

consumer_group = None
mp_group = None
town = None


def agent_action(agent):
    print("I'm " + agent.name + " and I'm acting.")
    # return False means to move
    return False


def create_consumer(name, expense):
    """
    Create an agent.
    """
    balance = {"expense": expense}
    return Agent(name=name, attrs=balance, action=consumer_action)


def create_mp(name, fixed_expense, variable_expense, capital, inventory_size):
    store_books = {"fixed expense": fixed_expense,
                   "variable expense": variable_expense,
                   "capital": capital, "inventory": [inventory_size, 0]}
    return Agent(name=name, attrs=store_books, action=mp_action)


def consumer_action(town):
    pass


def mp_action(agent, town):
    global town
    capital = agent.attrs['capital']
    customers = town.get_moore_hood(agent)
    for mbr in customers:
        capital += mbr.attrs['expense']
    capital -= agent.attrs['fixed expense']
    num_visits = agent.attrs['inventory'][1]
    num_visits += len(customers)
    inventory_size = agent.attrs['inventory'][0]
    if num_visits >= inventory_size - 8:
        capital -= agent.attrs['variable expense'] * num_visits
        num_visits = 0
    if capital <= 0:
        agent.die()


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    # ds_file = get_prop_path(MODEL_NAME)
    # if props is None:
    #     pa = PropArgs.create_props(MODEL_NAME,
    #                                ds_file=ds_file)
    # else:
    #     pa = PropArgs.create_props(MODEL_NAME,
    #                                prop_dict=props)

    consumer_group = Composite("Consumer", {"color": BLUE})
    mp_group = Composite("Mom and pop", {"color": RED},)
    groups = []
    groups.append(consumer_group)
    groups.append(mp_group)
    for i in range(0, 100):
        groups[0] += create_consumer('Consumer ' + str(i), 50)
    for j in range(0, 5):
        groups[1] += create_mp('Mom and Pop ' + str(j), 250, 100, 1000, 30)

    town = Env("Town",
               height=20,
               width=20,
               members=groups)
    return (town, consumer_group, mp_group)


def main():
    global conusmer_group
    global mp_group
    global town

    (town, consumer_group, mp_group) = set_up()
    town()
    return 0


if __name__ == "__main__":
    main()
