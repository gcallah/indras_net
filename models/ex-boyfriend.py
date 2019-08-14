"""
A basic model.
Places two groups of agents in the environment randomly
and moves them around randomly.
"""

from indra.utils import get_props
from indra.agent import Agent
from indra.composite import Composite
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.env import Env
from indra.display_methods import RED, BLUE

import random

MODEL_NAME = "ex-boyfriend"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

# Girlfriend's State Strings
PICK_RANDOM = "Pick Random Cycle"
REPEAT_CYCLE = "Repeat Cycle"
CHANGE_DAY = "Change day"
SUCCESS = "Success"

# state numbers
PR = 0
RC = 1
CD = 2
SU = 3

NUM_STATES = 4

STATE_MAP = {PR: PICK_RANDOM, RC: REPEAT_CYCLE,
             CD: CHANGE_DAY, SU: SUCCESS}

DEF_NUM_BLUE = 1
DEF_NUM_RED = 1
DEF_CYCLE = 7

girlfriend = None
ex_boyfriend = None
env = None

girlfriend_cycle = None
ex_boyfriend_start = None
girlfriend_start = None
period = None
boyfriend_going = False
day = None


def get_girlfriend_decision():
    global period
    global girlfriend_start
    global girlfriend_cycle

    return (period - girlfriend_start) % girlfriend_cycle == 0


def girlfriend_action(agent):
    global period
    global girlfriend_cycle
    global girlfriend_start

    girlfriend_going = False
    # print("GF here")

    if agent["state"] == PR:
        if girlfriend_cycle is None:
            girlfriend_cycle = random.randint(1, 7)
            girlfriend_start = period

        girlfriend_going = get_girlfriend_decision()
        if girlfriend_going:
            if girlfriend_going and boyfriend_going:
                agent["state"] = RC
            else:
                agent["state"] = CD
                girlfriend_start += 1

    elif agent["state"] == RC:
        girlfriend_going = get_girlfriend_decision()
        if girlfriend_going:
            if not boyfriend_going:
                girlfriend_cycle = None
                agent["state"] = PR
            else:
                agent["state"] = SU

    elif agent["state"] == CD:
        girlfriend_going = get_girlfriend_decision()
        if girlfriend_going and boyfriend_going:
            agent["state"] = RC

    else:
        print("SUCCESS!!!!")

    print("State: ", agent["state"])

    if girlfriend_going:
        # print("GF going")
        return False
    else:
        # print("GF not going")
        return True


def boyfriend_action(agent):
    # print("I'm " + agent.name + " and I'm acting.")
    global ex_boyfriend_start
    global period
    global boyfriend_going

    period += 1
    # print("Period: ", period)
    # print("Cycle: ", agent['cycle'])

    if period % agent["cycle"] == 0:
        # print("BF Going")
        boyfriend_going = True
        # return False means to move
        return False

    else:
        # print("BF not going")
        boyfriend_going = False

    return True


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
    global period

    period = 0

    pa = get_props(MODEL_NAME, props)

    girlfriend = Composite("Girlfriend", {"color": BLUE}, props=pa,
                           member_creator=create_girlfriend,
                           num_members=1)

    ex_boyfriend = Composite("Ex-Boyfriend", {"color": RED}, props=pa,
                             member_creator=create_boyfriend,
                             num_members=1)

    env = Env("env",
              height=pa.get('grid_height', DEF_HEIGHT),
              width=pa.get('grid_width', DEF_WIDTH),
              members=[ex_boyfriend, girlfriend],
              props=pa)

    return (env, ex_boyfriend, girlfriend)


def main():
    global ex_boyfriend
    global girlfriend
    global env

    (env, ex_boyfriend, girlfriend) = set_up()

    if DEBUG2:
        print(env.__repr__())

    env()
    return 0


if __name__ == "__main__":
    main()
