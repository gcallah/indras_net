"""
Abelian sandpile model
"""
from propargs.propargs import PropArgs

from indra.agent import Agent, switch
from indra.env import Env
from indra.space import DEF_WIDTH, DEF_HEIGHT
from indra.composite import Composite

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


def change_group(agent, sandpile_env, curr_group_idx, next_group_idx):  # noqa F811
    """
    Change group from curr_group_idx passed in
    to the next_group_idx passed in.
    """
    switch(agent, groups[curr_group_idx], groups[next_group_idx])


def add_grain(sandpile_env, agent):
    """
    Addd a grain to the agent that is passed in
    by changing the group that it is in.
    """
    curr_group_idx = get_curr_group_idx(agent)
    next_group_idx = get_next_group_idx(curr_group_idx)
    if DEBUG:
        print("Agent at", agent.pos, "is changing group from",
              agent.primary_group(), "to", next_group_idx)
    change_group(agent, sandpile_env, curr_group_idx, next_group_idx)
    if DEBUG:
        print("Agent at", agent.pos, "has changed to", agent.primary_group())
    if next_group_idx == 0:
        topple(sandpile_env, agent)


def topple(sandpile_env, agent):
    if DEBUG:
        print("Sandpile in", agent.pos, "is toppling")
    for neighbor in agent.neighbors:
        add_grain(sandpile_env, agent.neighbors[neighbor])


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
    add_grain(sandpile_env, sandpile_env.attrs["center_agent"])


def place_action(agent):
    if agent.neighbors is None:
        sandpile_env.get_hood(["get_x_hood", "get_y_hood"], agent, True)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    global groups

    if props is None:
        pa = PropArgs.create_props('sandpile_props',
                                   ds_file='props/sandpile.props.json')
    else:
        pa = PropArgs.create_props('sandpile_props',
                                   prop_dict=props)
    width = pa.get('grid_width', DEF_WIDTH)
    height = pa.get('grid_height', DEF_HEIGHT)
    groups = []
    group_indices = {}
    for i in range(NUM_GROUPS):
        groups.append(Composite("Group" + str(i)))
        group_indices[groups[i].name] = i
    for y in range(height):
        for x in range(width):
            groups[0] += create_agent(x, y)
    sandpile_env = Env("Sanpile",
                       action=sandpile_action,
                       members=groups,
                       height=height,
                       width=width,
                       random_placing=False)
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
