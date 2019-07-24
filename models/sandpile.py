"""
Abelian sandpile model
"""
from propargs.propargs import PropArgs
from indra.utils import get_prop_path
from indra.agent import Agent, switch
from indra.composite import Composite
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.env import Env
from indra.display_methods import CIRCLE

MODEL_NAME = "sandpile"
DEBUG = False  # Turns debugging code on or off

NUM_GROUPS = 4

sandpile_env = None
groups = None
group_indices = None


def create_agent(x, y):
    """
    Create an agent with the passed x, y value as its name.
    """
    name = "(" + str(x) + "," + str(y) + ")"
    return Agent(name=name, action=place_action)


def get_curr_group_idx(agent):
    """
    Returns the int index of the current group.
    Ex) Returns 0 if group is Group 0
    """
    return group_indices[agent.primary_group().name]


def get_next_group_idx(curr_group_idx):
    """
    Returns the int index of the next group.
    Ex) Returns 1 if curr_group_idx group is Group 0
    """
    return (curr_group_idx + 1) % NUM_GROUPS


def change_group(agent, curr_group_idx, next_group_idx):  # noqa F811
    """
    Change group from curr_group_idx passed in
    to the next_group_idx passed in.
    """
    global sandpile_env

    switch(agent, groups[curr_group_idx], groups[next_group_idx])


def add_grain(agent):
    """
    Add a grain to the agent that is passed in
    by changing the group that it is in.
    """
    global sandpile_env

    agent.has_acted = True
    curr_group_idx = get_curr_group_idx(agent)
    next_group_idx = get_next_group_idx(curr_group_idx)
    if DEBUG:
        print("Agent at", agent.pos, "is changing group from",
              agent.primary_group(), "to", next_group_idx)
    change_group(agent, curr_group_idx, next_group_idx)
    if DEBUG:
        print("Agent at", agent.pos, "has changed to", agent.primary_group())
    if next_group_idx == 0:
        topple(agent)


def topple(agent):
    global sandpile_env

    if DEBUG:
        print("Sandpile in", agent.pos, "is toppling")
    neighbors = sandpile_env.get_vonneumann_hood(agent, save_neighbors=True)
    for neighbor in neighbors:
        add_grain(neighbors[neighbor])


def sandpile_action(sandpile_env):
    """
    The action that will be taken avery period.
    Adds a grain to the center agent.
    """
    if DEBUG:
        print("Adding a grain to sandpile in position",
              sandpile_env.attrs["center_agent"].pos,
              "which is in the group",
              sandpile_env.attrs["center_agent"].primary_group())
    add_grain(sandpile_env.attrs["center_agent"])
    return True


def place_action(agent):
    return True
    # if agent.neighbors is None:
    #     sandpile_env.get_vonneumann_hood(agent, save_neighbors=True)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    global sandpile_env
    global groups
    global group_indices

    ds_file = get_prop_path(MODEL_NAME)
    if props is None:
        pa = PropArgs.create_props(MODEL_NAME,
                                   ds_file=ds_file)
    else:
        pa = PropArgs.create_props(MODEL_NAME,
                                   prop_dict=props)
    width = pa.get('grid_width', DEF_WIDTH)
    height = pa.get('grid_height', DEF_HEIGHT)
    groups = []
    group_indices = {}
    for i in range(NUM_GROUPS):
        groups.append(Composite(("Group" + str(i)), {"marker": CIRCLE}))
        group_indices[groups[i].name] = i
    for y in range(height):
        for x in range(width):
            groups[0] += create_agent(x, y)
    sandpile_env = Env("Sanpile",
                       action=sandpile_action,
                       members=groups,
                       height=height,
                       width=width,
                       random_placing=False,
                       props=pa)
    sandpile_env.attrs["center_agent"] = sandpile_env.get_agent_at(height // 2,
                                                                   width // 2)
    return (sandpile_env, groups, group_indices)


def main():
    global sandpile_env
    global groups
    global group_indices
    (sandpile_env, groups, group_indices) = set_up()
    sandpile_env()
    return 0


if __name__ == "__main__":
    main()
