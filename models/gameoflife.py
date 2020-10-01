"""
Conway's Game of Life model.
"""
from indra.agent import Agent, X, Y
from indra.composite import Composite
from indra.display_methods import SQUARE
from indra.env import Env
from registry.registry import get_env, get_prop, get_group
from registry.registry import get_env_attr, set_env_attr
from indra.utils import init_props
from indra.space import Region
from registry.execution_registry import init_exec_key, get_exec_key
from registry.execution_registry import CLI_EXEC_KEY

MODEL_NAME = "gameoflife"
DEBUG = False  # Turns debugging code on or off
DEF_HEIGHT = 30
DEF_WIDTH = 30
BLACK = "Black"

LIVE = True  # BLACK
DIE = False  # WHITE

# These are the indices for our patterns:
GLIDER = 0
SMALL_EXPL = 1
EXPLODER = 2
HORIZONTAL_ROW = 3
SPACESHIP = 4
TUMBLER = 5


def reset_env_attrs():
    set_env_attr("to_come_alive", [])
    set_env_attr("to_die", [])
    set_env_attr("reset_lists", False)


def create_game_cell(x, y, execution_key=CLI_EXEC_KEY):
    """
    Create an agent with the passed x, y value as its name.
    """
    return Agent(name=("(%d,%d)" % (x, y)),
                 action=game_agent_action,
                 attrs={"save_neighbors": True},
                 execution_key=execution_key)


def live_or_die(agent):
    """
    Apply the rules for live agents.
    The agent passed in should be alive, meaning its color should be black.
    """
    curr_region = Region(space=get_env(), center=agent.get_pos(),
                         size=1)
    num_live_neighbors = curr_region.get_num_of_agents(exclude_self=True,
                                                       pred=None)
    if (num_live_neighbors != 2 and num_live_neighbors != 3):
        return DIE
    else:
        return LIVE


def is_black(agent):
    return agent.prim_group == BLACK


def apply_dead_rules(new_x, new_y, execution_key=CLI_EXEC_KEY):
    """
    Apply the rules for dead agents.
    The agent passed in should be dead, meaning its color should be white.
    """
    curr_region = Region(space=get_env(), center=(new_x, new_y),
                         size=1)
    num_live_neighbors = curr_region.get_num_of_agents(exclude_self=True,
                                                       pred=is_black)
    if num_live_neighbors == 3:
        return True
    else:
        return False


def check_for_new_agents(agent):
    curr_x = agent.get_x()
    curr_y = agent.get_y()
    for y in ([-1, 0, 1]):
        for x in ([-1, 0, 1]):
            if (x != 0) or (y != 0):
                new_x = curr_x + x
                new_y = curr_y + y
                potential_new_agent = get_env().get_agent_at(new_x, new_y)
                if potential_new_agent is None:
                    if apply_dead_rules(new_x, new_y):
                        get_env_attr("to_come_alive").append((new_x, new_y))


def gameoflife_action(biosphere, **kwargs):
    """
    The action that will be taken every period for the enviornment.
    Loops through the list of agents that has to come alive and die
        and carries out the corresponding action.
    """
    b = get_group(BLACK, get_exec_key(kwargs))
    # for the next loop, why not use the womb?
    for agent_pos in get_env_attr("to_come_alive"):
        if DEBUG:
            print("Agent at", agent_pos, "will come alive")
        if biosphere.get_agent_at(agent_pos[X], agent_pos[Y]) is None:
            agent = create_game_cell(agent_pos[X], agent_pos[Y])
            b += agent
            biosphere.place_member(agent, xy=(agent_pos[X], agent_pos[Y]))
    for agent in get_env_attr("to_die"):
        if not isinstance(agent, tuple):
            if DEBUG:
                print("Agent at", get_env_attr("to_die[agent]"), "will die")
            agent.die()
            # we shouldn't need to do the following:
            b.del_member(agent)
    return True


def game_agent_action(agent, **kwargs):
    """
    The action that will be taken every period for the agents.
    Checks its Moore neighborhood and checks the number of neighbors to
        the rules of Game of Life.
    """

    if get_env_attr("reset_lists"):
        reset_env_attrs()

    check_for_new_agents(agent)
    if live_or_die(agent) == DIE:
        get_env_attr("to_die").append(agent)
    return True


def populate_board(patterns, pattern_num, execution_key=CLI_EXEC_KEY):
    agent_locs = patterns[pattern_num]
    b = get_group(BLACK, execution_key)
    for loc in agent_locs:
        agent = create_game_cell(loc[X], loc[Y])
        b += agent
        get_env().place_member(agent, xy=loc)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    init_props(MODEL_NAME, props)
    exec_key = init_exec_key(props)
    height = get_prop("grid_height", DEF_HEIGHT)
    width = get_prop("grid_width", DEF_WIDTH)
    simulation = get_prop("simulation", 0)
    black = Composite(BLACK, {"color": BLACK, "marker": SQUARE},
                      execution_key=exec_key)
    groups = [black]
    Env("Game of Life",
        action=gameoflife_action,
        height=height,
        width=width,
        members=groups,
        attrs={"size": 100,
               "change_grid_spacing": (0.5, 1),
               "hide_xy_ticks": True,
               "hide_legend": True},
        random_placing=False,
        execution_key=exec_key)

    center = (width // 2, height // 2)
    patterns = [
        [
            (center[X], center[Y]),
            (center[X] - 1, center[1] + 1),
            (center[X] + 1, center[Y] + 1),
            (center[X] + 1, center[Y]),
            (center[X], center[1] - 1)
        ],
        [
            (center[X], center[Y]),
            (center[X], center[1] + 1),
            (center[X] - 1, center[Y]),
            (center[X] + 1, center[Y]),
            (center[X] - 1, center[1] - 1),
            (center[X] + 1, center[Y] - 1),
            (center[X], center[Y] - 2)
        ],
        [
            (center[X], center[Y]),
            (center[X], center[1] - 4),
            (center[X] - 2, center[Y]),
            (center[X] + 2, center[Y]),
            (center[X] - 2, center[Y] - 1),
            (center[X] + 2, center[Y] - 1),
            (center[X] - 2, center[Y] - 2),
            (center[X] + 2, center[Y] - 2),
            (center[X] - 2, center[Y] - 3),
            (center[X] + 2, center[Y] - 3),
            (center[X] - 2, center[Y] - 4),
            (center[X] + 2, center[Y] - 4)
        ],
        [
            (center[X], center[Y]),
            (center[X] + 1, center[Y]),
            (center[X] - 1, center[Y]),
            (center[X] + 2, center[Y]),
            (center[X] - 2, center[Y]),
            (center[X] + 3, center[Y]),
            (center[X] - 3, center[Y]),
            (center[X] + 4, center[Y]),
            (center[X] - 4, center[Y]),
        ],
        [
            (center[X], center[Y]),
            (center[X] - 1, center[Y]),
            (center[X] - 2, center[Y]),
            (center[X] - 3, center[Y]),
            (center[X], center[Y] - 1),
            (center[X], center[Y] - 2),
            (center[X] - 4, center[Y] - 1),
            (center[X] - 1, center[Y] - 3),
            (center[X] - 4, center[Y] - 3)
        ],
        [
            (center[X] - 1, center[Y]),
            (center[X] - 2, center[Y]),
            (center[X] + 1, center[Y]),
            (center[X] + 2, center[Y]),
            (center[X] - 1, center[Y] - 1),
            (center[X] - 2, center[Y] - 1),
            (center[X] + 1, center[Y] - 1),
            (center[X] + 2, center[Y] - 1),
            (center[X] - 1, center[Y] - 2),
            (center[X] - 1, center[Y] - 3),
            (center[X] - 1, center[Y] - 4),
            (center[X] + 1, center[Y] - 2),
            (center[X] + 1, center[Y] - 3),
            (center[X] + 1, center[Y] - 4),
            (center[X] - 3, center[Y] - 3),
            (center[X] - 3, center[Y] - 4),
            (center[X] - 3, center[Y] - 5),
            (center[X] - 2, center[Y] - 5),
            (center[X] + 3, center[Y] - 3),
            (center[X] + 3, center[Y] - 4),
            (center[X] + 3, center[Y] - 5),
            (center[X] + 2, center[Y] - 5)
        ]
    ]
    populate_board(patterns, simulation)
    reset_env_attrs()


def main():
    set_up()
    get_env()()
    return 0


if __name__ == "__main__":
    main()
