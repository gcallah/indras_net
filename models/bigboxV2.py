"""
Second version of Big box model for simulating the behaviors of consumers.
"""
# import random

# from indra.utils import get_props
from indra.agent import Agent
from indra.composite import Composite
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.env import Env
from indra.display_methods import GRAY

MODEL_NAME = "bigbox"
NUM_OF_CONSUMERS = 50
CONSUMER_INDX = 0

town = None


def create_consumer(name, i, props=None):
    return Agent(name + str(i), action=consumer_action)


def consumer_action(consumer):
    return False


def town_action(town):
    pass


def set_up(props=None):
    global groups
    global town
    consumer_group = Composite("Consumer", {"color": GRAY},
                               member_creator=create_consumer,
                               num_members=NUM_OF_CONSUMERS)
    groups = []
    groups.append(consumer_group)
    town = Env("Town",
               action=town_action,
               members=groups,
               height=DEF_HEIGHT,
               width=DEF_WIDTH)
    return (town, groups)


def main():
    global town
    global groups

    (town, groups) = set_up()
    town()
    return 0


if __name__ == "__main__":
    main()
