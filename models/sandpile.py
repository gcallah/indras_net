"""
    This is an abelican sandpile model.
    Starting life of sandpile as segregation clone.
"""

from indra.agent import Agent
from indra.composite import Composite
# from indra.space import in_hood
from indra.env import Env
import indra.display_methods as disp
from indra.space import in_hood

DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

HEIGHT = 8
WIDTH = 8

MAX_SAND = 5

NEARBY = 1

sandpile = None

group0 = None
group1 = None
group2 = None
group3 = None
group4 = None
group5 = None


def env_unfavorable(sand_height):
    """
    Is the environment to our agent's liking or not??
    Here, the question is, "Is there too much sand?"
    """
    return sand_height > MAX_SAND


def agent_action(agent):
    """
    If the agent is surrounded by more "others" than it is comfortable
    with, the agent will move.
    """
    if(env_unfavorable):
        nearby = group0.subset(in_hood, agent, NEARBY)
        nearby += group1.subset(in_hood, agent, NEARBY)
        nearby += group2.subset(in_hood, agent, NEARBY)
        nearby += group3.subset(in_hood, agent, NEARBY)
        nearby += group4.subset(in_hood, agent, NEARBY)
        nearby += group5.subset(in_hood, agent, NEARBY)

        for i in range(agent["grains"]):
            pass
    

    return env_unfavorable(agent["grains"])


def create_agent(i):
    """
    Creates agent for holding sand.
    """
    return Agent("sand location" + str(i),
                 action=agent_action,
                 attrs={"grains": 0})


def set_up():
    """
    A func to set up run that can also be used by test code.
    """
    group0 = Composite("Group0", {"color": disp.BLACK})
    group1 = Composite("Group1", {"color": disp.MAGENTA})
    group2 = Composite("Group2", {"color": disp.BLUE})
    group3 = Composite("Group3", {"color": disp.CYAN})
    group4 = Composite("Group4", {"color": disp.RED})
    group5 = Composite("Group5", {"color": disp.YELLOW})
    for i in range(HEIGHT * WIDTH):
        group0 += create_agent(i)

    sandpile = Env("A sandpile", members=[
                   group0,
                   group1,
                   group2,
                   group3,
                   group4,
                   group5
                   ],
                   height=HEIGHT, width=WIDTH)
    return (group0,
            group1,
            group2,
            group3,
            group4,
            group5,
            sandpile)


def main():
    global sandpile
    global group0
    global group1
    global group2
    global group3
    global group4
    global group5
    (group0, group1, group2, group3, group4, group5,
     sandpile) = set_up()

    if DEBUG2:
        print(sandpile.__repr__())

    sandpile()
    return 0


if __name__ == "__main__":
    main()
