"""
Conway's Game of Life model
"""
from propargs.propargs import PropArgs

from indra.agent import Agent, switch
from indra.env import Env
from indra.space import DEF_WIDTH, DEF_HEIGHT
from indra.composite import Composite
from indra.display_methods import BLACK, WHITE, SQUARE

DEBUG = True  # Turns debugging code on or off

groups = []


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


def get_color(group):
    """
    Returns 0 or 1, 0 for white and 1 for black
    when passed in a group.
    """
    if group == groups[0]:
        return 0
    else:
        return 1


def apply_live_rules(gameoflife_env, agent):
    num_live_neighbors = agent.neighbors
    if (num_live_neighbors != 2 and num_live_neighbors != 3
       and num_live_neighbors is not None):
        change_color(gameoflife_env, agent)


def apply_dead_rules(gameoflife_env, agent):
    num_live_neighbors = agent.neighbors
    if num_live_neighbors == 3:
        change_color(gameoflife_env, agent)


def gameoflife_action(gameoflife_env):
    """
    The action that will be taken every period.
    """
    for y in range(0, gameoflife_env.height):
        for x in range(0, gameoflife_env.width):
            curr_agent = gameoflife_env.get_agent_at(x, y)
            if curr_agent.primary_group() == groups[1]:
                if DEBUG:
                    print("Agent at", curr_agent.get_pos(), "has",
                          curr_agent.neighbors, "neighbors")
                apply_live_rules(gameoflife_env, curr_agent)
            else:
                apply_dead_rules(gameoflife_env, curr_agent)


def agent_action(agent):
    if agent.neighbors is None:
        neighbors = gameoflife_env.get_all_neighbors(agent)
        num_live_neighbors = 0
        for neighbor in neighbors:
            if neighbor.primary_group() == groups[1]:
                num_live_neighbors += 1
        agent.neighbors = num_live_neighbors


def set_up():
    """
    A func to set up run that can also be used by test code.
    """
    pa = PropArgs.create_props('basic_props',
                               ds_file='props/gameoflife.props.json')
    width = pa.get('grid_width', DEF_WIDTH)
    height = pa.get('grid_height', DEF_HEIGHT)
    black = Composite("black", {"color": BLACK, "marker": SQUARE})
    white = Composite("white", {"color": WHITE})
    groups.append(white)
    groups.append(black)
    for y in range(height):
        for x in range(width):
            groups[0] += create_agent(x, y)
    gameoflife_env = Env("game of life env",
                         action=gameoflife_action,
                         height=height,
                         width=width,
                         members=groups,
                         random_placing=False)
    gameoflife_env.user.exclude_choices(["line_graph"])

    a = gameoflife_env.get_agent_at((width // 2), (height // 2))
    change_color(gameoflife_env, a)
    b = gameoflife_env.get_agent_at((width // 2), (height // 2) + 1)
    change_color(gameoflife_env, b)
    c = gameoflife_env.get_agent_at((width // 2) + 1, (height // 2))
    change_color(gameoflife_env, c)
    d = gameoflife_env.get_agent_at((width // 2) + 1, (height // 2) + 1)
    change_color(gameoflife_env, d)

    return (groups, gameoflife_env)


def main():
    global groups
    global gameoflife_env
    (groups, gameoflife_env) = set_up()
    gameoflife_env()
    return 0


if __name__ == "__main__":
    main()
