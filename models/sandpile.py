"""
    This is an abelican sandpile model.
    Starting life of sandpile as segregation clone.
"""

from indra.agent import Agent
from indra.composite import Composite
# from indra.space import in_hood
from indra.env import Env


DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

HEIGHT = 5
WIDTH = 5

SAND_PREFIX = "sand_location "

NEARBY = 1

NUM_GROUPS = 6

sandpile = None

groups = []
group_indices = {}


def topple(sandpile, agent):
    if DEBUG:
        print("Sandpile in", agent.pos, "is toppling")
    neighbors = sandpile.get_vonneumann_hood(agent)


def change_group(agent, sandpile, curr_group_idx, next_group_idx):
    if DEBUG:
        print("Say something about group switch")
    sandpile.add_switch(agent, groups[curr_group_idx], groups[next_group_idx])


def curr_group(agent):
    return group_indices[agent.primary_group().name]


def next_group(curr_group_idx):
    return (curr_group_idx + 1) % NUM_GROUPS


def add_grain(agent):
    curr_group_idx = curr_group(agent)
    next_group_idx = next_group(curr_group_idx)
    change_group(agent, sandpile, curr_group_idx, next_group_idx)
    if next_group_idx == 0:

        topple(sandpile, agent)
    return next_group_idx


def sandpile_action(sandpile):
    """
    The sandpile just drops grains on the center agent.
    """
    if DEBUG:
        print("Adding a grain to sandpile in position (",
              sandpile.attrs["center_agent"].get_x(), ",",
              sandpile.attrs["center_agent"].get_y(), ")",
              "which is in the group",
              sandpile.attrs["center_agent"].primary_group())     
    add_grain(sandpile.attrs["center_agent"])

def place_action(agent):
    print("Place_action with pos", agent.pos, "and group", agent.primary_group())


def create_agent(i):
    """
    Creates agent for holding sand.
    """
    return Agent(SAND_PREFIX + str(i), action=place_action)


def set_up():
    """
    A func to set up run that can also be used by test code.
    """
    for i in range(NUM_GROUPS):
        groups.append(Composite("Group" + str(i)))
        group_indices[groups[i].name] = i

    for i in range((HEIGHT) * (WIDTH)):
        groups[0] += create_agent(i)

    sandpile = Env("A sandpile", action=sandpile_action, members=groups,
                   height=HEIGHT, width=WIDTH)
    sandpile.attrs["center_agent"] = sandpile.get_agent_at(int(HEIGHT / 2),
                                                           int(WIDTH / 2))

    return (groups, group_indices, sandpile)


def main():
    global sandpile
    global groups
    (groups, group_indices, sandpile) = set_up()

    if DEBUG2:
        print(sandpile.__repr__())

    sandpile()
    return 0


if __name__ == "__main__":
    main()
