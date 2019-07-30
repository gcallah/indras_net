"""
Conway's Game of Life model
"""
from random import randint

from propargs.propargs import PropArgs
from indra.utils import get_prop_path
from indra.agent import Agent, switch
from indra.composite import Composite
from indra.env import Env
from indra.display_methods import BLACK, WHITE, SQUARE

MODEL_NAME = "gameoflife"
DEBUG = False  # Turns debugging code on or off

DEF_HEIGHT = 30
DEF_WIDTH = 30

gameoflife_env = None
groups = None
min_y = None


def create_agent(x, y):
    """
    Create an agent with the passed x, y value as its name.
    """
    name = "(" + str(x) + "," + str(y) + ")"
    return Agent(name=name, action=game_agent_action)


def change_color(agent):
    """
    Automatically change color from one to the other.
    """
    global gameoflife_env
    global groups

    curr_group = agent.primary_group()
    next_group = groups[0]
    if curr_group == next_group:
        next_group = groups[1]
    switch(agent, curr_group, next_group)


def apply_live_rules(agent):
    """
    Apply the rules for live agents.
    The agent passed in should be alive,
    meaning its color should be black.
    """
    global gameoflife_env
    global groups

    num_live_neighbors = 0
    for neighbor in agent.neighbors:
        if (agent.neighbors[neighbor]).primary_group() == groups[1]:
            num_live_neighbors += 1
    if (num_live_neighbors != 2 and num_live_neighbors != 3):
        return True
    else:
        return False


def apply_dead_rules(agent):
    """
    Apply the rules for dead agents.
    The agent passed in should be dead,
    meaning its color should be white.
    """
    global gameoflife_env
    global groups

    num_live_neighbors = 0
    for neighbor in agent.neighbors:
        if (agent.neighbors[neighbor]).primary_group() == groups[1]:
            num_live_neighbors += 1
    if num_live_neighbors == 3:
        return True
    else:
        return False


def gameoflife_action(gameoflife_env):
    """
    The action that will be taken every period.
    Loops through every agent, determines whether it is alive or dead,
    and passes it to the corresponding rule function.
    """
    global min_x
    global min_y
    global groups

    if min_x > 0:
        min_x -= 1
    if min_y > 0:
        min_y -= 1

    new_min_x = 0
    new_min_y = 0
    change_min = True
    for y in range(min_y, gameoflife_env.height):
        for x in range(min_x, gameoflife_env.width):
            curr_agent = gameoflife_env.get_agent_at(x, y)
            if curr_agent.neighbors is not None:
                if change_min:
                    new_min_x = curr_agent.get_x()
                    new_min_y = curr_agent.get_y()
                    change_min = False
                if curr_agent.primary_group() == groups[1]:
                    if apply_live_rules(curr_agent):
                        curr_agent.locator.add_switch(curr_agent, groups[1],
                                                      groups[0])
                elif apply_dead_rules(curr_agent):
                    curr_agent.locator.add_switch(curr_agent, groups[0],
                                                  groups[1])
    min_x = new_min_x
    min_y = new_min_y
    return True


def game_agent_action(agent):
    if agent.neighbors is None:
        gameoflife_env.get_moore_hood(agent, save_neighbors=True)
    return True


def populate_board_random(width, height):
    """
    Randomly populates the center of the board with agents.
    Number of agents is at most 10% of the board's area.
    """
    global min_x
    global min_y
    global gameoflife_env
    global groups

    num_agent = int(0.1 * (width * height))
    upper_limit = int((width / 2) + (width / 4))
    lower_limit = int((width / 2) - (width / 4)) + 1
    min_x = lower_limit
    min_y = lower_limit
    for i in range(num_agent):
        agent = gameoflife_env.get_agent_at(randint(lower_limit, upper_limit),
                                            randint(lower_limit, upper_limit))
        print(agent)
        print(type(agent))
        if agent is not None and agent.primary_group() != groups[1]:
            change_color(agent)


def populate_board_glider(width, height):
    global min_x
    global min_y
    global gameoflife_env

    center = [width // 2, height // 2]
    agent = gameoflife_env.get_agent_at(center[0], center[1])
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] - 1, center[1] + 1)
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] + 1, center[1] + 1)
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] + 1, center[1])
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0], center[1] - 1)
    change_color(agent)
    min_x = center[0] - 1
    min_y = center[1] - 1


def populate_board_small_exploder(width, height):
    global min_x
    global min_y
    global gameoflife_env

    center = [width // 2, height // 2]
    agent = gameoflife_env.get_agent_at(center[0], center[1])
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0], center[1] + 1)
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] - 1, center[1])
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] + 1, center[1])
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] - 1, center[1] - 1)
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] + 1, center[1] - 1)
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0], center[1] - 2)
    change_color(agent)
    min_x = center[0] - 1
    min_y = center[1] - 2


def populate_board_exploder(width, height):
    global min_x
    global min_y
    global gameoflife_env

    center = [width // 2, height // 2]
    agent = gameoflife_env.get_agent_at(center[0], center[1])
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0], center[1] - 4)
    change_color(agent)
    for i in range(0, 5):
        agent_left = gameoflife_env.get_agent_at(center[0] - 2, center[1] - i)
        agent_right = gameoflife_env.get_agent_at(center[0] + 2, center[1] - i)
        change_color(agent_left)
        change_color(agent_right)
    min_x = center[0] - 4
    min_y = center[1] - 4


def populate_board_n_horizontal_row(width, height, n=10):
    global min_x
    global min_y
    global gameoflife_env

    center = [width // 2, height // 2]
    right = (n // 2) + (n % 2)
    left = n // 2
    for r in range(right):
        agent = gameoflife_env.get_agent_at(center[0] + r, center[1])
        change_color(agent)
    for l in range(1, left):
        agent = gameoflife_env.get_agent_at(center[0] - l, center[1])
        change_color(agent)
    min_x = center[0] - left - 1
    min_y = center[1]


def populate_board_n_vertical_row(width, height, n=10):
    global min_x
    global min_y
    global gameoflife_env

    center = [width // 2, height // 2]
    top = (n // 2) + (n % 2)
    bottom = n // 2
    for t in range(top):
        agent = gameoflife_env.get_agent_at(center[0], center[1] + t)
        change_color(agent)
    for b in range(1, bottom):
        agent = gameoflife_env.get_agent_at(center[0], center[1] - b)
        change_color(agent)
    min_x = center[0]
    min_y = center[1] - bottom - 1


def populate_board_lightweight_spaceship(width, height):
    global min_x
    global min_y
    global gameoflife_env

    center = [width // 2, height // 2]
    agent = gameoflife_env.get_agent_at(center[0], center[1])
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] - 1, center[1])
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] - 2, center[1])
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] - 3, center[1])
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0], center[1] - 1)
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0], center[1] - 2)
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] - 4, center[1] - 1)
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] - 1, center[1] - 3)
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] - 4, center[1] - 3)
    change_color(agent)
    min_x = center[0] - 4
    min_y = center[1] - 3


def populate_board_tumbler(width, height):
    global min_x
    global min_y
    global gameoflife_env

    center = [width // 2, height // 2]
    agent = gameoflife_env.get_agent_at(center[0], center[1])
    agent = gameoflife_env.get_agent_at(center[0] - 1, center[1])
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] - 2, center[1])
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] + 1, center[1])
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] + 2, center[1])
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] - 1, center[1] - 1)
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] - 2, center[1] - 1)
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] + 1, center[1] - 1)
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] + 2, center[1] - 1)
    change_color(agent)

    agent = gameoflife_env.get_agent_at(center[0] - 1, center[1] - 2)
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] - 1, center[1] - 3)
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] - 1, center[1] - 4)
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] + 1, center[1] - 2)
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] + 1, center[1] - 3)
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] + 1, center[1] - 4)
    change_color(agent)

    agent = gameoflife_env.get_agent_at(center[0] - 3, center[1] - 3)
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] - 3, center[1] - 4)
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] - 3, center[1] - 5)
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] - 2, center[1] - 5)
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] + 3, center[1] - 3)
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] + 3, center[1] - 4)
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] + 3, center[1] - 5)
    change_color(agent)
    agent = gameoflife_env.get_agent_at(center[0] + 2, center[1] - 5)
    change_color(agent)

    min_x = center[0] - 3
    min_y = center[1] - 5


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    global groups
    global gameoflife_env

    ds_file = get_prop_path(MODEL_NAME)
    if props is None:
        pa = PropArgs.create_props(MODEL_NAME, ds_file=ds_file)
    else:
        pa = PropArgs.create_props(MODEL_NAME,
                                   prop_dict=props)
    height = pa.get("grid_heigh", DEF_HEIGHT)
    width = pa.get("grid_width", DEF_WIDTH)
    simulation = pa.get("simulation", 1)
    white = Composite("white", {"color": WHITE})
    black = Composite("black", {"color": BLACK, "marker": SQUARE})
    groups = []
    groups.append(white)
    groups.append(black)
    for y in range(height):
        for x in range(width):
            groups[0] += create_agent(x, y)
    gameoflife_env = Env("Game of Life",
                         action=gameoflife_action,
                         height=height,
                         width=width,
                         members=groups,
                         random_placing=False,
                         props=pa)
    gameoflife_env.exclude_menu_item("line_graph")
    if simulation == 0:
        populate_board_random(width, height)
    elif simulation == 1:
        populate_board_glider(width, height)
    elif simulation == 2:
        populate_board_small_exploder(width, height)
    elif simulation == 3:
        populate_board_exploder(width, height)
    elif simulation == 4:
        populate_board_n_horizontal_row(width, height)
    elif simulation == 5:
        populate_board_n_vertical_row(width, height)
    elif simulation == 6:
        populate_board_lightweight_spaceship(width, height)
    elif simulation == 7:
        populate_board_tumbler(width, height)
    return (gameoflife_env, groups)


def main():
    global gameoflife_env
    global groups
    (gameoflife_env, groups) = set_up()
    gameoflife_env()
    return 0


if __name__ == "__main__":
    main()
