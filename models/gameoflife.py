"""
Conway's Game of Life model
"""
from random import randint

from propargs.propargs import PropArgs

from indra.agent import Agent, switch
from indra.env import Env
from indra.space import DEF_WIDTH, DEF_HEIGHT
from indra.composite import Composite
from indra.display_methods import BLACK, WHITE, SQUARE

DEBUG = False  # Turns debugging code on or off

gameoflife_env = None
groups = None


def create_agent(x, y):
    """
    Create an agent with the passed x, y value as its name.
    """
    name = "(" + str(x) + "," + str(y) + ")"
    return Agent(name=name, action=agent_action)


def change_color(gameoflife_env, agent):
    """
    Automatically change color from one to the other.
    """
    curr_group = agent.primary_group()
    next_group = groups[0]
    if curr_group == next_group:
        next_group = groups[1]
    switch(agent, curr_group, next_group)


def apply_live_rules(gameoflife_env, agent):
    """
    Apply the rules for live agents.
    The agent passed in should be alive.
    """
    num_live_neighbors = 0
    for neighbor in agent.neighbors:
        if (agent.neighbors[neighbor]).primary_group() == groups[1]:
            num_live_neighbors += 1
    if (num_live_neighbors != 2 and num_live_neighbors != 3):
        return True
    else:
        return False


def apply_dead_rules(gameoflife_env, agent):
    """
    Apply the rules for dead agents.
    The agent passed in should be dead.
    """
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
    to_be_changed = []
    for y in range(0, gameoflife_env.height):
        for x in range(0, gameoflife_env.width):
            curr_agent = gameoflife_env.get_agent_at(x, y)
            if curr_agent.neighbors is not None:
                if curr_agent.primary_group() == groups[1]:
                    if apply_live_rules(gameoflife_env, curr_agent):
                        to_be_changed.append(curr_agent)
                else:
                    if apply_dead_rules(gameoflife_env, curr_agent):
                        to_be_changed.append(curr_agent)
    for to_change in to_be_changed:
        change_color(gameoflife_env, to_change)


def agent_action(agent):
    if agent.neighbors is None:
        gameoflife_env.get_hood(["get_x_hood", "get_y_hood",
                                "get_top_lr_hood", "get_bottom_lr_hood"],
                                agent, True)


def populate_board_random(gameoflife_env, width, height):
    """
    Randomly populates the center of the board with agents.
    Number of agents is at most 10% of the board's area.
    """
    num_agent = int(0.1 * (width * height))
    upper_limit = int((width / 2) + (width / 4))
    lower_limit = int((width / 2) - (width / 4)) + 1
    for i in range(num_agent):
        agent = gameoflife_env.get_agent_at(randint(lower_limit, upper_limit),
                                            randint(lower_limit, upper_limit))
        if agent.primary_group() != groups[1]:
            change_color(gameoflife_env, agent)


def populate_board_glider(gameoflife_env, width, height):
    center = [width // 2, height // 2]
    agent = gameoflife_env.get_agent_at(center[0], center[1])
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] - 1, center[1] + 1)
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] + 1, center[1] + 1)
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] + 1, center[1])
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0], center[1] - 1)
    change_color(gameoflife_env, agent)


def populate_board_small_exploder(gameoflife_env, width, height):
    center = [width // 2, height // 2]
    agent = gameoflife_env.get_agent_at(center[0], center[1])
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0], center[1] + 1)
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] - 1, center[1])
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] + 1, center[1])
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] - 1, center[1] - 1)
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] + 1, center[1] - 1)
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0], center[1] - 2)
    change_color(gameoflife_env, agent)


def populate_board_exploder(gameoflife_env, width, height):
    center = [width // 2, height // 2]
    agent = gameoflife_env.get_agent_at(center[0], center[1])
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0], center[1] - 4)
    change_color(gameoflife_env, agent)
    for i in range(0, 5):
        agent_left = gameoflife_env.get_agent_at(center[0] - 2, center[1] - i)
        agent_right = gameoflife_env.get_agent_at(center[0] + 2, center[1] - i)
        change_color(gameoflife_env, agent_left)
        change_color(gameoflife_env, agent_right)


def populate_board_n_horizontal_row(gameoflife_env, width, height, n=10):
    center = [width // 2, height // 2]
    right = (n // 2) + (n % 2)
    left = n // 2
    for r in range(right):
        agent = gameoflife_env.get_agent_at(center[0] + r, center[1])
        change_color(gameoflife_env, agent)
    for l in range(1, left):
        agent = gameoflife_env.get_agent_at(center[0] - l, center[1])
        change_color(gameoflife_env, agent)


def populate_board_n_vertical_row(gameoflife_env, width, height, n=10):
    center = [width // 2, height // 2]
    top = (n // 2) + (n % 2)
    bottom = n // 2
    for t in range(top):
        agent = gameoflife_env.get_agent_at(center[0], center[1] + t)
        change_color(gameoflife_env, agent)
    for b in range(1, bottom):
        agent = gameoflife_env.get_agent_at(center[0], center[1] - b)
        change_color(gameoflife_env, agent)


def populate_board_lightweight_spaceship(gameoflife_env, width, height):
    center = [width // 2, height // 2]
    agent = gameoflife_env.get_agent_at(center[0], center[1])
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] - 1, center[1])
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] - 2, center[1])
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] - 3, center[1])
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0], center[1] - 1)
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0], center[1] - 2)
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] - 4, center[1] - 1)
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] - 1, center[1] - 3)
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] - 4, center[1] - 3)
    change_color(gameoflife_env, agent)


def populate_board_tumbler(gameoflife_env, width, height):
    center = [width // 2, height // 2]
    agent = gameoflife_env.get_agent_at(center[0], center[1])
    agent = gameoflife_env.get_agent_at(center[0] - 1, center[1])
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] - 2, center[1])
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] + 1, center[1])
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] + 2, center[1])
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] - 1, center[1] - 1)
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] - 2, center[1] - 1)
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] + 1, center[1] - 1)
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] + 2, center[1] - 1)
    change_color(gameoflife_env, agent)

    agent = gameoflife_env.get_agent_at(center[0] - 1, center[1] - 2)
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] - 1, center[1] - 3)
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] - 1, center[1] - 4)
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] + 1, center[1] - 2)
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] + 1, center[1] - 3)
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] + 1, center[1] - 4)
    change_color(gameoflife_env, agent)

    agent = gameoflife_env.get_agent_at(center[0] - 3, center[1] - 3)
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] - 3, center[1] - 4)
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] - 3, center[1] - 5)
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] - 2, center[1] - 5)
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] + 3, center[1] - 3)
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] + 3, center[1] - 4)
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] + 3, center[1] - 5)
    change_color(gameoflife_env, agent)
    agent = gameoflife_env.get_agent_at(center[0] + 2, center[1] - 5)
    change_color(gameoflife_env, agent)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    global groups

    ds_file = 'props/gameoflife.props.json'
    if props is None:
        pa = PropArgs.create_props('gameoflife_props', ds_file=ds_file)
    else:
        pa = PropArgs.create_props('gameoflife_props',
                                   prop_dict=props)
    width = pa.get('grid_width', DEF_WIDTH)
    height = pa.get('grid_height', DEF_HEIGHT)
    simulation = pa.get('simulation', 0)
    black = Composite("black", {"color": BLACK, "marker": SQUARE})
    white = Composite("white", {"color": WHITE})
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
                         random_placing=False)
    gameoflife_env.user.exclude_choices(["line_graph"])
    if simulation == 0:
        populate_board_random(gameoflife_env, width, height)
    elif simulation == 1:
        populate_board_glider(gameoflife_env, width, height)
    elif simulation == 2:
        populate_board_small_exploder(gameoflife_env, width, height)
    elif simulation == 3:
        populate_board_exploder(gameoflife_env, width, height)
    elif simulation == 4:
        populate_board_n_horizontal_row(gameoflife_env, width, height)
    elif simulation == 5:
        populate_board_n_vertical_row(gameoflife_env, width, height)
    elif simulation == 6:
        populate_board_lightweight_spaceship(gameoflife_env, width, height)
    elif simulation == 7:
        populate_board_tumbler(gameoflife_env, width, height)
    return (gameoflife_env, groups)


def main():
    global gameoflife_env
    global groups
    (gameoflife_env, groups) = set_up()
    gameoflife_env()
    return 0


if __name__ == "__main__":
    main()
