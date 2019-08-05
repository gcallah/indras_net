"""
Conway's Game of Life model
"""

from indra.utils import get_props
from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env
from indra.display_methods import BLACK, SQUARE

MODEL_NAME = "gameoflife"
DEBUG = False  # Turns debugging code on or off
DEF_HEIGHT = 30
DEF_WIDTH = 30

gameoflife_env = None
groups = None

reset_lists = False
to_come_alive = []
to_die = []
DEBUG = False


def create_agent(x, y):
    """
    Create an agent with the passed x, y value as its name.
    """
    return Agent(name=("(%d,%d)" % (x, y)), action=game_agent_action)


def apply_live_rules(agent):
    """
    Apply the rules for live agents.
    The agent passed in should be alive, meaning its color should be black.
    """
    global gameoflife_env
    global groups

    num_live_neighbors = 0
    for neighbor in agent.neighbors:
        if agent.neighbors[neighbor].primary_group() == groups[0]:
            num_live_neighbors += 1
    if (num_live_neighbors != 2 and num_live_neighbors != 3):
        return True
    else:
        return False


def apply_dead_rules_composite(composite):
    global groups

    num_live_neighbors = 0
    for neighbor in composite:
        if composite[neighbor].primary_group() == groups[0]:
            num_live_neighbors += 1
    if num_live_neighbors == 3:
        return True
    else:
        return False


def check_for_new_agents(agent):
    global gameoflife_env

    curr_x = agent.get_x()
    curr_y = agent.get_y()
    to_come_alive = []
    for y in ([-1, 0, 1]):
        for x in ([-1, 0, 1]):
            if (x != 0) or (y != 0):
                new_x = curr_x + x
                new_y = curr_y + y
                if gameoflife_env.get_agent_at(new_x, new_y) is None:
                    neighbors = gameoflife_env.get_moore_hood((new_x, new_y))
                    if apply_dead_rules_composite(neighbors):
                        to_come_alive.append((new_x, new_y))
    return to_come_alive


def gameoflife_action(gameoflife_env):
    """
    The action that will be taken every period for the enviornment.
    Loops through the list of agents that has to come alive and die
        and carries out the corresponding action.
    """
    global groups
    global to_come_alive
    global to_die
    global reset_lists

    for agent_pos in to_come_alive:
        if DEBUG:
            print("Agent at", to_come_alive[agent_pos], "will come alive")
        if gameoflife_env.get_agent_at(agent_pos[0], agent_pos[1]) is None:
            agent = create_agent(agent_pos[0], agent_pos[1])
            groups[0] += agent
            gameoflife_env.place_member(agent, xy=(agent_pos[0], agent_pos[1]))
    for agent in to_die:
        if not isinstance(agent, tuple):
            if DEBUG:
                print("Agent at", to_die[agent], "will die")
            agent.die()
            groups[0].del_member(agent)
            gameoflife_env.remove_location(agent.get_x(), agent.get_y())
    reset_lists = True
    return True


def game_agent_action(agent):
    """
    The action that will be taken every period for the agents.
    Checks its Moore neighborhood and checks the number of neighbors to
        the rules of Game of Life.
    """
    global to_come_alive
    global to_die
    global reset_lists

    if reset_lists:
        to_come_alive = []
        to_die = []
        reset_lists = False

    gameoflife_env.get_moore_hood(agent, save_neighbors=True)
    to_come_alive += check_for_new_agents(agent)
    if apply_live_rules(agent):
        to_die.append(agent)
    return True


def populate_board_glider(width, height):
    global gameoflife_env
    global groups

    center = [width // 2, height // 2]
    agent_loc = []
    agent_loc.append((center[0], center[1]))
    agent_loc.append((center[0] - 1, center[1] + 1))
    agent_loc.append((center[0] + 1, center[1] + 1))
    agent_loc.append((center[0] + 1, center[1]))
    agent_loc.append((center[0], center[1] - 1))
    for loc in agent_loc:
        agent = create_agent(loc[0], loc[1])
        groups[0] += agent
        gameoflife_env.place_member(agent, xy=loc)


def populate_board_small_exploder(width, height):
    global gameoflife_env
    global groups

    center = [width // 2, height // 2]
    agent_loc = []
    agent_loc.append((center[0], center[1]))
    agent_loc.append((center[0], center[1] + 1))
    agent_loc.append((center[0] - 1, center[1]))
    agent_loc.append((center[0] + 1, center[1]))
    agent_loc.append((center[0] - 1, center[1] - 1))
    agent_loc.append((center[0] + 1, center[1] - 1))
    agent_loc.append((center[0], center[1] - 2))
    for loc in agent_loc:
        agent = create_agent(loc[0], loc[1])
        groups[0] += agent
        gameoflife_env.place_member(agent, xy=loc)


def populate_board_exploder(width, height):
    global gameoflife_env

    center = [width // 2, height // 2]
    agent_loc = []
    agent_loc.append((center[0], center[1]))
    agent_loc.append((center[0], center[1] - 4))
    for i in range(0, 5):
        agent_loc.append((center[0] - 2, center[1] - i))
        agent_loc.append((center[0] + 2, center[1] - i))
    for loc in agent_loc:
        agent = create_agent(loc[0], loc[1])
        groups[0] += agent
        gameoflife_env.place_member(agent, xy=loc)


def populate_board_n_horizontal_row(width, height, n=10):
    global gameoflife_env

    center = [width // 2, height // 2]
    agent_loc = []
    right = (n // 2) + (n % 2)
    left = n // 2
    for r in range(right):
        agent_loc.append((center[0] + r, center[1]))
    for l in range(1, left):
        agent_loc.append((center[0] - l, center[1]))
    for loc in agent_loc:
        agent = create_agent(loc[0], loc[1])
        groups[0] += agent
        gameoflife_env.place_member(agent, xy=loc)


def populate_board_n_vertical_row(width, height, n=10):
    global gameoflife_env

    center = [width // 2, height // 2]
    agent_loc = []
    top = (n // 2) + (n % 2)
    bottom = n // 2
    for t in range(top):
        agent_loc.append((center[0], center[1] + t))
    for b in range(1, bottom):
        agent_loc.append((center[0], center[1] - b))
    for loc in agent_loc:
        agent = create_agent(loc[0], loc[1])
        groups[0] += agent
        gameoflife_env.place_member(agent, xy=loc)


def populate_board_lightweight_spaceship(width, height):
    global gameoflife_env

    center = [width // 2, height // 2]
    agent_loc = []
    agent_loc.append((center[0], center[1]))
    agent_loc.append((center[0] - 1, center[1]))
    agent_loc.append((center[0] - 2, center[1]))
    agent_loc.append((center[0] - 3, center[1]))
    agent_loc.append((center[0], center[1] - 1))
    agent_loc.append((center[0], center[1] - 2))
    agent_loc.append((center[0] - 4, center[1] - 1))
    agent_loc.append((center[0] - 1, center[1] - 3))
    agent_loc.append((center[0] - 4, center[1] - 3))
    for loc in agent_loc:
        agent = create_agent(loc[0], loc[1])
        groups[0] += agent
        gameoflife_env.place_member(agent, xy=loc)


def populate_board_tumbler(width, height):
    global gameoflife_env

    center = [width // 2, height // 2]
    agent_loc = []

    agent_loc.append((center[0] - 1, center[1]))
    agent_loc.append((center[0] - 2, center[1]))
    agent_loc.append((center[0] + 1, center[1]))
    agent_loc.append((center[0] + 2, center[1]))
    agent_loc.append((center[0] - 1, center[1] - 1))
    agent_loc.append((center[0] - 2, center[1] - 1))
    agent_loc.append((center[0] + 1, center[1] - 1))
    agent_loc.append((center[0] + 2, center[1] - 1))

    agent_loc.append((center[0] - 1, center[1] - 2))
    agent_loc.append((center[0] - 1, center[1] - 3))
    agent_loc.append((center[0] - 1, center[1] - 4))
    agent_loc.append((center[0] + 1, center[1] - 2))
    agent_loc.append((center[0] + 1, center[1] - 3))
    agent_loc.append((center[0] + 1, center[1] - 4))

    agent_loc.append((center[0] - 3, center[1] - 3))
    agent_loc.append((center[0] - 3, center[1] - 4))
    agent_loc.append((center[0] - 3, center[1] - 5))
    agent_loc.append((center[0] - 2, center[1] - 5))
    agent_loc.append((center[0] + 3, center[1] - 3))
    agent_loc.append((center[0] + 3, center[1] - 4))
    agent_loc.append((center[0] + 3, center[1] - 5))
    agent_loc.append((center[0] + 2, center[1] - 5))
    for loc in agent_loc:
        agent = create_agent(loc[0], loc[1])
        groups[0] += agent
        gameoflife_env.place_member(agent, xy=loc)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    global groups
    global gameoflife_env

    pa = get_props(MODEL_NAME, props)

    height = pa.get("grid_height", DEF_HEIGHT)
    width = pa.get("grid_width", DEF_WIDTH)
    simulation = pa.get("simulation", 0)
    black = Composite("Black", {"color": BLACK, "marker": SQUARE})
    groups = []
    groups.append(black)
    gameoflife_env = Env("Game of Life",
                         action=gameoflife_action,
                         height=height,
                         width=width,
                         members=groups,
                         attrs={"change_grid_spacing": 0.5,
                                "hide_xy_labels": True},
                         random_placing=False,
                         props=pa)
    if simulation == 0:
        populate_board_glider(width, height)
    elif simulation == 1:
        populate_board_small_exploder(width, height)
    elif simulation == 2:
        populate_board_exploder(width, height)
    elif simulation == 3:
        populate_board_n_horizontal_row(width, height)
    elif simulation == 4:
        populate_board_n_vertical_row(width, height)
    elif simulation == 5:
        populate_board_lightweight_spaceship(width, height)
    elif simulation == 6:
        populate_board_tumbler(width, height)
    return (gameoflife_env, groups)


def main():
    global gameoflife_env
    global groups
    (gameoflife_env, groups) = set_up()

    if DEBUG:
        print(gameoflife_env.__repr__())

    gameoflife_env()
    return 0


if __name__ == "__main__":
    main()
