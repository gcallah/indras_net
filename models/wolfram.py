"""
Wolfram's cellular automata model.
"""

import ast
import os
import random

from indra.agent import Agent, switch
from indra.composite import Composite
from indra.display_methods import BLACK, WHITE, SQUARE
from indra.env import Env
from indra.space import DEF_WIDTH
from indra.utils import init_props
from registry.registry import get_prop, get_env, get_group, set_env_attr, get_env_attr

MODEL_NAME = "wolfram"
DEBUG = False  # Turns debugging code on or off
DEF_RULE = 30

# Group codes:
W = 0
B = 1


def create_wolf_cell(x, y):
    """
    Create an agent with the passed x, y value as its name.
    """
    return Agent(name=("(%d,%d)" % (x, y)))


def get_color(group):
    """
    Returns W or B, W for white and B for black
        when passed in a group.
    W and B are integer values:- 0 and 1, respectively.
    """

    if group == get_group(WHITE):
        return W
    else:
        return B


def get_rule(rule_num):
    """
    Takes in an int for the rule_num
        and returns the corresponding rule dictionary.
    Read from a text file that contains all 256 rules.
    """
    rule_str = ""
    rules_file = os.path.join(os.getenv("INDRA_HOME", "/home/indrasnet/indras_net"), "models", "wolfram_rules.txt")
    with open(rules_file) as rule_line:
        for i, line in enumerate(rule_line):
            if i == rule_num:
                rule_str = line
                break
    return ast.literal_eval(rule_str)


def next_color(rule_dict, left, middle, right):
    """
    Takes in a trio of colors
        and returns the color that the agent in the next row should be
        based on the rule number picked by the user.
    """
    # print("left-{}, middle-{}, right-{}".format(left, middle, right))
    return rule_dict[str((left, middle, right))]


def get_str_key(x, y):
    return ("(%d,%d)" % (x, y))


def set_wolfram_env_attr():
    curr_row_idx = get_env_attr("curr_row_idx")


def wolfram_action(wolfram_env: Env):
    """
    The action that will be taken every period.
    """
    curr_row = wolfram_env.get_row_hood(get_env_attr("curr_row_idx"))
    # if not isinstance(curr_row, Composite):
    #     curr_row = Composite(name=curr_row["name"], serial_obj=curr_row)

    rule_num = get_prop('rule_number', DEF_RULE)
    rule_dict = get_rule(rule_num)
    active_row_y = wolfram_env.height - wolfram_env.get_periods() - 1
    # print("Active row - {}, period -  {}".format(active_row_y, wolfram_env.get_periods()))
    if curr_row == wolfram_env.get_row_hood(wolfram_env.height - 1):
        curr_row = wolfram_env.get_row_hood(active_row_y)
    wolfram_env.user.tell("\nChecking agents in row " + str(active_row_y)
                          + " against the rule...")
    if active_row_y < 1:
        wolfram_env.user.error_message["run"] = (' '.join([
            "You have exceeded the ",
            "maximum height ",
            "and cannot run the model ",
            "for more periods.\n",
            "Please pick one of the ",
            "other options."]))
        wolfram_env.exclude_menu_item("run")
    else:
        next_row = wolfram_env.get_row_hood(active_row_y - 1)
        left_color = get_color(
            curr_row[get_str_key(0, active_row_y)].primary_group())
        x = 0

        for agent in curr_row:
            # print("Processing agent-{}, x-{}".format(agent, x))
            if DEBUG:
                print("Checking agent at", curr_row[agent])
            if (x > 0) and (x < wolfram_env.width - 1):
                middle_color = get_color(curr_row[agent].primary_group())
                right_color = get_color(
                    curr_row[get_str_key(x + 1, active_row_y)].primary_group())
                # print("Primary group - left - {}, middle - {}, right - {}".format(
                #     curr_row[get_str_key(0, active_row_y)].primary_group(), curr_row[agent].primary_group(),
                #     curr_row[get_str_key(x + 1, active_row_y)].primary_group()))
                if DEBUG:
                    print("  Left: %d, middle: %d, right: %d" %
                          (left_color, middle_color, right_color))
                if next_color(rule_dict, left_color, middle_color,
                              right_color):
                    # print("Adding switch for active_row-{} for agent-{}".format(active_row_y, agent))
                    wolfram_env.add_switch(next_row[
                                               get_str_key(x,
                                                           active_row_y - 1)],
                                           get_group(WHITE), get_group(BLACK))
                    next_row[get_str_key(x, active_row_y - 1)].set_prim_group(get_group(BLACK))
                left_color = middle_color
            x += 1
        # curr_row = next_row

    set_env_attr("curr_row_idx", active_row_y - 1)
    return True


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """

    init_props(MODEL_NAME, props)

    width = get_prop('grid_width', DEF_WIDTH)

    rule_num = get_prop('rule_number', DEF_RULE)

    rule_dict = get_rule(rule_num)

    height = (width // 2) + (width % 2)

    white = Composite(WHITE, {"color": WHITE})

    black = Composite(BLACK, {"color": BLACK, "marker": SQUARE})

    groups = [get_group(WHITE), get_group(BLACK)]

    for y in range(height):
        for x in range(width):
            groups[W] += create_wolf_cell(x, y)
    wolfram_env = Env(MODEL_NAME,
                      action=wolfram_action,
                      height=height,
                      width=width,
                      members=groups,
                      attrs={"size": 50,
                             "hide_grid_lines": True,
                             "hide_legend": True},
                      random_placing=False)
    get_env().exclude_menu_item("line_graph")

    '''
    This switch needs to happen before the environment is executed.
    Using add switch doesn't process the switch until after the environment is executed
    which breaks the model.
    '''
    switch(get_env().get_agent_at(width // 2, height - 1).name, WHITE, BLACK)
    get_env().get_agent_at(width // 2, height - 1).set_prim_group(get_group(BLACK))
    set_env_attr("curr_row_idx", get_env().height - 1)


def main():
    set_up()
    get_env()()
    return 0


if __name__ == "__main__":
    main()
