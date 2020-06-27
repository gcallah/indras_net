"""
Abelian sandpile model.
"""

from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import CIRCLE
from indra.env import Env
from registry.registry import get_env, get_group, get_prop
from registry.registry import user_log_notif
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.utils import init_props

MODEL_NAME = "sandpile"
DEBUG = False  # Turns debugging code on or off

NUM_GROUPS = 4


def create_grain(x, y):
    """
    Create an agent with the passed x, y value as its name.
    """
    return Agent(name=("(%d,%d)" % (x, y)),
                 action=None,
                 attrs={"save_neighbors": True})


def add_grain(agent):
    """
    Add a grain to the agent that is passed in
        by changing the group that it is in.
    """

    curr_group_idx = int(agent.prim_group_nm())
    next_group_idx = (curr_group_idx + 1) % NUM_GROUPS
    if DEBUG:
        print("Agent at", agent.pos, "is changing from",
              agent.prim_group_nm(), "to", next_group_idx)
    get_env().add_switch(agent,
                         get_group(str(curr_group_idx)),
                         get_group(str(next_group_idx)))
    agent.set_prim_group(str(next_group_idx))
    if DEBUG:
        print("Agent at", agent.pos, "has changed to", agent.prim_group_nm())
        print("Primary group number", agent.prim_group_nm())
        print("Current group index", curr_group_idx)
        print("Next group index", next_group_idx)
    if next_group_idx == 0:
        topple(agent)


def topple(agent):
    """
    Called when height of an agent is greater than NUM_GROUPS.
    Calls add_grain for its Von Neumann neighbors
        and if those agents need to topple, recursively calls topple.
    """

    if DEBUG:
        print("Sandpile in", agent.pos, "is toppling")
    if agent.neighbors is None:
        agent.neighbors = get_env().get_vonneumann_hood(agent)
    for neighbor in agent.neighbors:
        add_grain(agent.neighbors[neighbor])


def sandpile_action(env):
    """
    The action that will be taken avery period.
    Adds a grain to the center agent.
    """

    if DEBUG:
        print("Adding a grain to sandpile in position",
              env.attrs["center"].pos,
              "which is in the group",
              env.attrs["center"].prim_group_nm())
    add_grain(env.attrs["center"])
    return True


def set_env_attrs():
    user_log_notif("Setting env attrs for forest fire.")
    width = get_prop('grid_width', DEF_WIDTH)
    height = get_prop('grid_height', DEF_HEIGHT)
    get_env().attrs["center"] = get_env().get_agent_at(height // 2,
                                                       width // 2)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """

    init_props(MODEL_NAME, props)
    width = get_prop('grid_width', DEF_WIDTH)
    height = get_prop('grid_height', DEF_HEIGHT)
    groups = []
    for i in range(NUM_GROUPS):
        groups.append(Composite(str(i), {"marker": CIRCLE}))
    for y in range(height):
        for x in range(width):
            groups[0] += create_grain(x, y)
    sandpile_env = Env(MODEL_NAME,
                       action=sandpile_action,
                       height=height,
                       width=width,
                       members=groups,
                       attrs={"size": 65,
                              "hide_axes": True,
                              "hide_legend": True},
                       random_placing=False
                       )
    # these settings must be re-done every API re-load:
    set_env_attrs()
    return sandpile_env, groups


def main():
    set_up()
    get_env()()
    return 0


if __name__ == "__main__":
    main()
