"""
Abelian sandpile model.
"""

from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import CIRCLE
from indra.env import Env
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.utils import get_props

MODEL_NAME = "sandpile"
DEBUG = False  # Turns debugging code on or off

NUM_GROUPS = 4

sandpile_env = None
groups = None
group_indices = None


def create_grain(x, y):
    """
    Create an agent with the passed x, y value as its name.
    """
    return Agent(name=("(%d,%d)" % (x, y)),
                 action=spagent_action,
                 attrs={"save_neighbors": True})


def add_grain(agent):
    """
    Add a grain to the agent that is passed in
        by changing the group that it is in.
    """
    global sandpile_env
    global groups
    global group_indices
    curr_group_idx = group_indices[agent.primary_group().name]
    next_group_idx = (curr_group_idx + 1) % NUM_GROUPS
    if DEBUG:
        print("Agent at", agent.pos, "is changing from",
              agent.primary_group(), "to", next_group_idx)
    sandpile_env.now_switch(agent, groups[curr_group_idx],
                            groups[next_group_idx])
    if DEBUG:
        print("Agent at", agent.pos, "has changed to", agent.primary_group())
    if next_group_idx == 0:
        topple(agent)


def topple(agent):
    """
    Called when height of an agent is greater than NUM_GROUPS.
    Calls add_grain for its Von Neumann neighbors
        and if those agents need to topple, recursively calls topple.
    """
    global sandpile_env
    global groups
    global group_indices

    if DEBUG:
        print("Sandpile in", agent.pos, "is toppling")
    if agent.neighbors is None:
        sandpile_env.get_vonneumann_hood(agent)
    for neighbor in agent.neighbors:
        add_grain(agent.neighbors[neighbor])


def sandpile_action(sandpile_env):
    """
    The action that will be taken avery period.
    Adds a grain to the center agent.
    """
    global groups
    global group_indices

    if DEBUG:
        print("Adding a grain to sandpile in position",
              sandpile_env.attrs["center_agent"].pos,
              "which is in the group",
              sandpile_env.attrs["center_agent"].primary_group())
    # if str(type(sandpile_env.attrs["center_agent"])) == "<class 'dict'>":
    #     add_grain(sandpile_env.registry[sandpile_env.attrs["center_agent"]["name"]])
    add_grain(sandpile_env.attrs["center_agent"])
    return True


def spagent_action(agent):
    return True


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    global sandpile_env
    global groups
    global group_indices

    pa = get_props(MODEL_NAME, props)
    width = pa.get('grid_width', DEF_WIDTH)
    height = pa.get('grid_height', DEF_HEIGHT)
    groups = []
    group_indices = {}
    for i in range(NUM_GROUPS):
        groups.append(Composite("Group" + str(i), {"marker": CIRCLE}))
        group_indices[groups[i].name] = i
    for y in range(height):
        for x in range(width):
            groups[0] += create_grain(x, y)
    sandpile_env = Env("Sandpile",
                       action=sandpile_action,
                       height=height,
                       width=width,
                       members=groups,
                       attrs={"size": 65,
                              "hide_axes": True,
                              "hide_legend": True},
                       random_placing=False,
                       props=pa)
    sandpile_env.attrs["center_agent"] = sandpile_env.get_agent_at(height // 2,
                                                                   width // 2)
    return sandpile_env, groups, group_indices


def restore_globals(env):
    global groups
    global group_indices
    global sandpile_env
    sandpile_env = env
    groups = []
    group_indices = {}
    # this model needs to be fundamentally revisited, so:
    # for i in range(NUM_GROUPS):
    #     groups.append(env.registry["Group" + str(i)])
    #     group_indices[groups[i].name] = i
    env.attrs["center_agent"] = env.get_agent_at(env.height // 2,
                                                 env.width // 2)


def main():
    global sandpile_env
    global groups
    global group_indices
    (sandpile_env, groups, group_indices) = set_up()
    sandpile_env()
    return 0


if __name__ == "__main__":
    main()
