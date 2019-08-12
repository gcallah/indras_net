"""
A basic model.
Places two groups of agents in the enviornment randomly
and moves them around randomly.
"""

from indra.utils import get_props
from indra.agent import Agent
from indra.composite import Composite
# from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.env import Env
from indra.display_methods import RED, BLUE

import random

MODEL_NAME = "ex-boyfriend"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

# Girlfriend's State Strings
PICK_RANDOM = "Pick Random Cycle"
GO_OUT = "Go Out"
REPEAT_CYCLE = "Repeat Cycle"
CHANGE = "Change day"
SUCCESS = "Success"

# state numbers
PR = 0
GO = 1
RC = 2
CH = 3
SU = 4

NUM_STATES = 5

STATE_MAP = {PR: PICK_RANDOM, GO: GO_OUT,
             RC: REPEAT_CYCLE, CH: CHANGE, SU: SUCCESS}

DEF_NUM_BLUE = 1
DEF_NUM_RED = 1
DEF_CYCLE = 7

girlfriend = None
ex_boyfriend = None
env = None

ex_boyfriend_start = None
period = None
boyfriend_going = False


def girlfriend_action(agent):



def boyfriend_action(agent):
    # print("I'm " + agent.name + " and I'm acting.")
    global ex_boyfriend_start
    global period
    global boyfriend_going

    period += 1
    if ex_boyfriend_start is None:
        decide = random.randint(0,1)
        if decide:
            ex_boyfriend_start = period
            boyfriend_going = True

    # return False means to move
    return False


def create_boyfriend(name, i, props=None):
    """
    Create an agent.
    """
    return Agent(name + str(i), action=boyfriend_action,
                 attrs={"cycle": props.get('cycle', DEF_CYCLE),
                        "going": True})


def create_girlfriend(name, i, props=None, state=PR):
    """
    Create an agent.
    """
    return Agent(name + str(i), action=girlfriend_action,
                 attrs={"state": state})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    global girlfriend
    global ex_boyfriend
    global env

    pa = get_props(MODEL_NAME, props)
    girlfriend = Composite("Girlfriend", {"color": BLUE},
                           member_creator=create_girlfriend,
                           num_members=1)
    ex_boyfriend = Composite("Ex-Boyfriend", {"color": RED},
                             member_creator=create_boyfriend,
                             num_members=1)

    env = Env("env",
              # height=pa.get('grid_height', DEF_HEIGHT),
              # width=pa.get('grid_width', DEF_WIDTH),
              members=[girlfriend, ex_boyfriend],
              props=pa)

    return (env, girlfriend, ex_boyfriend)


def main():
    global red_group
    global blue_group
    global env

    (env, blue_group, red_group) = set_up()

    if DEBUG2:
        print(env.__repr__())

    env()
    return 0


if __name__ == "__main__":
    main()
