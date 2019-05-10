"""
    This is the fashion model re-written in indra.
"""

from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env
from indra.display_methods import RED, BLUE

DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

NUM_RED = 8
NUM_BLUE = 8

red_group = None
blue_group = None
env = None


def agent_action(agent):
    print("I'm " + agent.name + " and I'm acting.")
    # return False means to move
    return False


def create_agent(color, i):
    """
    Create an agent.
    """
    return Agent(color + str(i), action=agent_action)


def set_up():
    """
    A func to set up run that can also be used by test code.
    """
    blue_group = Composite("Blues", {"color": BLUE},
                           member_creator=create_agent,
                           num_members=NUM_BLUE)
    red_group = Composite("Reds", {"color": RED},
                          member_creator=create_agent,
                          num_members=NUM_RED)

    env = Env("env", members=[blue_group, red_group])
    return (blue_group, red_group, env)


def main():
    global red_group
    global blue_group
    global env

    (blue_group, red_group, env) = set_up()

    if DEBUG2:
        print(env.__repr__())

    env()
    return 0


if __name__ == "__main__":
    main()
