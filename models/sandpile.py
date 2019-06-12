"""
This is an abelian sandpile model.
Starting life of sandpile as segregation clone.
"""

from indra.agent import Agent, switch
from indra.composite import Composite
from indra.env import Env


<<<<<<< HEAD
DEBUG = False  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off
=======
DEBUG = True  # Turns debugging code on or off
DEBUG2 = False  # Turns deeper debugging code on or off
>>>>>>> a51031cc47c4b075cbce65cb62a399d1a5d5a2fe

HEIGHT = 5
WIDTH = 5

SAND_PREFIX = "sand_location "

NEARBY = 1

NUM_GROUPS = 4

sandpile = None

groups = []
group_indices = {}


def is_on_edge(x, y, x1, y1, x2, y2):
    return (x == x1 or x == x2 - 1 or y == y1 or y == y2 - 1)


# def topple(sandpile, agent):
#     # if DEBUG:
#     #     print("Sandpile in", agent.pos, "is toppling")
#     neighbors = sandpile.get_vonneumann_hood(agent)
#     # print("The neighbors have the color of", neighbors.get_color())
#     # if (is_on_edge(agent_))
#     for neighbor in neighbors:
#         #  print("debugging the primary_group: ", neighbor.primary_group())
#         # if DEBUG:
#         #     print("Getting neighbors")
#         #     print(neighbor.get_x(), neighbor.get_y())
#         # curr_group_idx = curr_group(neighbor)
#         # next_group_idx = next_group(curr_group_idx)
#         # change_group(neighbor, sandpile, curr_group_idx, next_group_idx)
#         add_grain(sandpile, neighbor)

def topple(sandpile, agent):
    if DEBUG:
<<<<<<< HEAD
        print("Sandpile in", agent.pos, "is toppling")

    for neighbor in agent.attrs["neighbors"]:
        # print("BEFORE ADD_GRAIN: Grain is being added to the neighbor at (", neighbor.get_x(), ",", neighbor.get_y(), ")")  # noqa E501
        # print("BEFORE ADD_GRAIN: current group of neighbor: ", neighbor.primary_group())  # noqa E501
        # if DEBUG:
        add_grain(sandpile, neighbor)

        # print("AFTER ADD_GRAIN: Grain is being added to the neighbor at (", neighbor.get_x(), ",", neighbor.get_y(), ")")  # noqa E501
        # print("AFTER ADD_GRAIN: current group of neighbor: ", neighbor.primary_group())  # noqa E501
        # print('\n')


def change_group(agent, sandpile, curr_group_idx, next_group_idx):
    if DEBUG:
        print("Agent at (", agent.get_x(), ",", agent.get_y(), ") is changing group from", curr_group_idx, "to", next_group_idx)  # noqa E501
    switch(agent, groups[curr_group_idx], groups[next_group_idx])

    # print("Agent at (", agent.get_x(), ",", agent.get_y(), ") is in GROUP: ", agent.primary_group())  # noqa E501


def curr_group(agent):
=======
        print("Sandpile in", agent.pos, "is toppling and is in",
              agent.primary_group())
    for neighbor in agent.attrs["neighbors"]:
        if DEBUG:
            print("Grain is being added to the neighbor at", neighbor.pos)
        add_grain(sandpile, neighbor)


def get_curr_group_idx(agent):
>>>>>>> a51031cc47c4b075cbce65cb62a399d1a5d5a2fe
    return group_indices[agent.primary_group().name]


def get_next_group_idx(curr_group_idx):
    return (curr_group_idx + 1) % NUM_GROUPS


<<<<<<< HEAD
def add_grain(sandpile, agent):
    curr_group_idx = curr_group(agent)
    next_group_idx = next_group(curr_group_idx)
=======
def change_group(agent, sandpile, curr_group_idx, next_group_idx):
    """
    Change group from current group index passed in
    to the next group index passed in
    """
    switch(agent, groups[curr_group_idx], groups[next_group_idx])


def add_grain(sandpile, agent):
    """
    Addd a grain to whichever agent is passed in
    """
    curr_group_idx = get_curr_group_idx(agent)
    next_group_idx = get_next_group_idx(curr_group_idx)
    if DEBUG:
        print("Agent at", agent.pos, "is changing group from",
              agent.primary_group(), "to", next_group_idx)
>>>>>>> a51031cc47c4b075cbce65cb62a399d1a5d5a2fe
    change_group(agent, sandpile, curr_group_idx, next_group_idx)
    if DEBUG:
        print("Agent at", agent.pos, "has changed to", agent.primary_group())
    if next_group_idx == 0:
        topple(sandpile, agent)


def sandpile_action(sandpile):
    """
    Drop a grain on the center agent.
    """
    if DEBUG:
        print("Adding a grain to sandpile in position",
              sandpile.attrs["center_agent"].pos,
              "which is in the group",
              sandpile.attrs["center_agent"].primary_group())
    add_grain(sandpile, sandpile.attrs["center_agent"])
<<<<<<< HEAD


def place_action(agent):
    # print("Place_action with pos", agent.pos, "and group",
    # agent.primary_group())
=======
    print("Grain has been added to sandpile in position",
          sandpile.attrs["center_agent"].pos,
          "which is now in the group",
          sandpile.attrs["center_agent"].primary_group())


def place_action(agent):
>>>>>>> a51031cc47c4b075cbce65cb62a399d1a5d5a2fe
    if not any(agent.attrs):
        neighbors = sandpile.get_vonneumann_hood(agent)
        agent.attrs = neighbors


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
