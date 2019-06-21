"""
"""

from propargs.propargs import PropArgs

from indra.agent import Agent, switch
from indra.env import Env
from indra.space import DEF_WIDTH
from indra.composite import Composite
from indra.display_methods import BLACK, WHITE
import ast

X = 0
Y = 1

DEBUG = False  # Turns debugging code on or off
DEBUG2 = False  # Turns deeper debugging code on or off

# States
B = 1
W = 0

STATE_MAP = {B: BLACK, W: WHITE}

# Some dictionaries of rules:
RULE30 = {
    (B, B, B): W,
    (B, B, W): W,
    (B, W, B): W,
    (B, W, W): B,
    (W, B, B): B,
    (W, B, W): B,
    (W, W, B): B,
    (W, W, W): W
}

GRID_WIDTH = 30
GRID_HEIGHT = 30

groups = []

template = {}

rules = [
    (B, B, B),
    (B, B, W),
    (B, W, B),
    (B, W, W),
    (W, B, B),
    (W, B, W),
    (W, W, B),
    (W, W, W)
]

pa = PropArgs.create_props('basic_props',
                           ds_file='props/wolfram.props.json')


def create_agent(x, y):
    """
    Create an agent with the passed in name
    """
    name = "(" + str(x) + "," + str(y) + ")"
    return Agent(name=name, action=agent_action)


def change_color(wolfram_env, agent):
    """
    Automatically change color from one group to the other
    """
    curr_group = agent.primary_group()
    next_group = groups[0]
    if curr_group == next_group:
        next_group = groups[1]
    switch(agent, curr_group, next_group)


def get_active_row(wolfram_env):
    """
    Returns an int of the current row, which is the bottom most row with
    an alive agent
    """
    for y in range(0, wolfram_env.height):
        row_to_check = wolfram_env.get_row_hood(y)
        for x in row_to_check:
            if x.primary_group() == groups[1]:
                return y
    return -1


def get_color(group):
    """
    Returns 0 or 1, 0 for white and 1 for black
    when passed in a group
    """
    if group == groups[0]:
        return 0
    else:
        return 1


def get_rule(rule_num):
    """
    Takes in an int for the rule_num
    and returns a dictionary that contains those rules
    read from a master texte file that contains all 256 rules
    """
    rule_txt = ""
    with open("wolfram_rules.txt") as rule_line:
        for i, line in enumerate(rule_line):
            if i == rule_num:
                rule_txt = line
                break
                break
    return ast.literal_eval(rule_txt)


def check_rule(left, middle, right):
    """
    Takes in the current agent, the agent left and right to it,
    and returns the color that the current agent needs to change to
    in the next row based on the given rule
    """
    left_group = left.primary_group()
    middle_group = middle.primary_group()
    right_group = right.primary_group()
    left_color = get_color(left_group)
    middle_color = get_color(middle_group)
    right_color = get_color(right_group)
    color_tuple = (left_color, middle_color, right_color)
    rule_num = pa.get('rule_number', RULE30[color_tuple])
    rule_dict = get_rule(rule_num)
    new_color = rule_dict[str(color_tuple)]
    if new_color == 0:
        return False
    else:
        return True


def wolfram_action(wolfram_env):
    """
    The action that will be taken every period
    """
    active_row_y = get_active_row(wolfram_env)
    if DEBUG:
        print("The current active row is at y =", active_row_y)
    active_row = wolfram_env.get_row_hood(active_row_y)
    next_row = wolfram_env.get_row_hood(active_row_y - 1)
    for i in range(1, len(active_row) - 1):
        curr_agent = active_row[i]
        left_agent = active_row[i - 1]
        right_agent = active_row[i + 1]
        if DEBUG2:
            print("curr_agent is at", curr_agent.get_pos(),
                  ", left_agent is at", left_agent.get_pos(),
                  ", and right_agent is at", right_agent.get_pos())
        changing_color = check_rule(left_agent, curr_agent, right_agent)
        next_curr_agent = next_row[i]
        if changing_color:
            change_color(wolfram_env, next_curr_agent)


def agent_action(agent):
    if DEBUG:
        print("Agent located at " + agent.name + " is acting")


def set_up():
    """
    A func to set up run that can also be used by test code.
    """

    width = pa.get('grid_width', DEF_WIDTH)
    height = 0
    if (width % 2 == 1):
        height = (width // 2) + 1
    else:
        height = (width // 2)
    black = Composite("black", {"color": BLACK})
    white = Composite("white", {"color": WHITE})
    groups.append(white)
    groups.append(black)
    for y in range(height):
        for x in range(width):
            groups[0] += create_agent(x, y)
    wolfram_env = Env("wolfram env",
                      action=wolfram_action,
                      height=height,
                      width=width,
                      members=groups,
                      random_placing=False)
    first_agent = wolfram_env.get_agent_at(width // 2, height - 1)
    change_color(wolfram_env, first_agent)
    return (groups, wolfram_env)


def main():
    global groups
    global wolfram_env
    (groups, wolfram_env) = set_up()
    wolfram_env()
    return 0


if __name__ == "__main__":
    main()
