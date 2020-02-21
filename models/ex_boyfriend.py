"""
A basic model.
Places two groups of agents in the environment randomly
and moves them around randomly.
"""

import random

from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import RED, BLUE
from indra.env import Env
from indra.registry import get_env, get_prop
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.utils import init_props

MODEL_NAME = "ex_boyfriend"
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

newly_freed_cycle = None
ex_boyfriend_start = None
newly_freed_start = None
period = None
boyfriend_going = False
day = None


def get_newly_freed_decision():
    global period
    global newly_freed_start
    global newly_freed_cycle

    return (period - newly_freed_start) % newly_freed_cycle == 0


def newly_freed_action(agent):
    global period
    global newly_freed_cycle
    global newly_freed_start

    newly_freed_going = False
    # print("GF here")

    if agent["state"] == PR:
        if newly_freed_cycle is None:
            newly_freed_cycle = random.randint(1, 7)
            newly_freed_start = period

        newly_freed_going = get_newly_freed_decision()
        if newly_freed_going:
            if newly_freed_going and boyfriend_going:
                agent["state"] = RC
            else:
                agent["state"] = CD
                newly_freed_start += 1

    elif agent["state"] == RC:
        newly_freed_going = get_newly_freed_decision()
        if newly_freed_going:
            if not boyfriend_going:
                newly_freed_cycle = None
                agent["state"] = PR
            else:
                agent["state"] = SU

    elif agent["state"] == CD:
        newly_freed_going = get_newly_freed_decision()
        if newly_freed_going and boyfriend_going:
            agent["state"] = RC

    else:
        print("SUCCESS!!!!")

    print("State: ", agent["state"])

    if newly_freed_going:
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
                 attrs={"cycle": get_prop('cycle', DEF_CYCLE),
                        "going": True})


def create_newly_freed(name, i, props=None, state=PR):
    """
    Create an agent.
    """
    return Agent(name + str(i), action=newly_freed_action,
                 attrs={"state": state})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    global period

    period = 0

    init_props(MODEL_NAME, props)

    newly_freed = Composite("Girlfriend", {"color": BLUE},
                            member_creator=create_newly_freed,
                            num_members=1)

    ex_boyfriend = Composite("Ex-Boyfriend", {"color": RED},
                             member_creator=create_boyfriend,
                             num_members=1)

    Env("bar",
        height=get_prop('grid_height', DEF_HEIGHT),
        width=get_prop('grid_width', DEF_WIDTH),
        members=[ex_boyfriend, newly_freed])


def main():
    set_up()
    get_env()()
    return 0


if __name__ == "__main__":
    main()
