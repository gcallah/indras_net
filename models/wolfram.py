"""
Wolfram's cellular automata model.
"""

import ast
import os

from indra.agent import Agent, switch, DONT_MOVE
from indra.composite import Composite
from indra.display_methods import BLACK, WHITE, SQUARE
from indra.env import Env
from indra.space import DEF_WIDTH
from indra.utils import init_props
from registry.registry import get_prop, get_env, get_group
from registry.registry import set_env_attr, get_env_attr, get_registration
from registry.execution_registry \
    import CLI_EXEC_KEY, EXEC_KEY

MODEL_NAME = "wolfram"
DEBUG = False  # Turns debugging code on or off
DEF_RULE = 30

# Group codes:
W = 0
B = 1


def create_wolf_cell(x, y, execution_key=None):
    """
    Create an agent with the passed x, y value as its name.
    """
    return Agent(name=("(%d,%d)" % (x, y)), execution_key=execution_key)


def get_color(group, execution_key=None):
    """
    Returns W or B, W for white and B for black
        when passed in a group.
    W and B are integer values:- 0 and 1, respectively.
    """
    if group == get_group(WHITE, execution_key):
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
    rules_file = os.path.join(os.getenv("INDRA_HOME",
                                        "/home/indrasnet/indras_net"),
                              "models", "wolfram_rules.txt")
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
    return rule_dict[str((left, middle, right))]


def agent_nm_from_xy(x, y):
    return ("(%d,%d)" % (x, y))


def top_row(execution_key=None):
    return get_env(execution_key=execution_key).height - 1


def gone_far_enough():
    get_env().user.error_message["run"] = (' '.join([
        "You have reached the ",
        "maximum height ",
        "and cannot run the model ",
        "for more periods.\n",
        "Please pick one of the ",
        "other options."]))
    get_env().exclude_menu_item("run")


def agent_color(x=None, y=None, agent_nm=None, execution_key=None):
    if x is not None:
        agent_nm = agent_nm_from_xy(x, y)
    agent = get_registration(agent_nm, execution_key)
    return get_color(agent.primary_group(), execution_key)


def wolfram_action(wolf_env, **kwargs):
    """
    The action that will be taken every period.
    """
    execution_key = kwargs[EXEC_KEY]

    row_above_idx = get_env_attr("prev_row_idx", execution_key=execution_key)

    active_row_idx = wolf_env.height - wolf_env.get_periods()

    wolf_env.user.tell(
        "Checking agents in row {} against the rule {}"
            .format(active_row_idx,
                    get_env_attr("rule_num", execution_key=execution_key)))

    if active_row_idx < 1:
        gone_far_enough()
        return DONT_MOVE
    else:
        next_row_idx = active_row_idx - 1

        next_row = wolf_env.get_row_hood(next_row_idx)

        left_color = \
            agent_color(x=0, y=active_row_idx, execution_key=execution_key)

        x = 0

        row_above = wolf_env.get_row_hood(row_above_idx)

        for agent_nm in row_above:
            if DEBUG:
                print("Checking agent at", row_above[agent_nm])
            if (x > 0) and (x < wolf_env.width - 1):
                middle_color = agent_color(agent_nm=agent_nm,
                                           execution_key=execution_key)
                right_color = agent_color(x=x + 1, y=active_row_idx,
                                          execution_key=execution_key)
                if DEBUG:
                    print("  Left: %d, middle: %d, right: %d" %
                          (left_color, middle_color, right_color))
                if next_color(
                        get_env_attr("rule_dict", execution_key=execution_key),
                        left_color, middle_color, right_color):
                    wolf_env.add_switch(next_row[
                                            agent_nm_from_xy(x, next_row_idx)],
                                        get_group(WHITE, execution_key),
                                        get_group(BLACK, execution_key))
                left_color = middle_color
            x += 1

    set_env_attr("prev_row_idx", next_row_idx, execution_key=execution_key)
    return DONT_MOVE


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    init_props(MODEL_NAME, props)
    execution_key = int(props[EXEC_KEY].val) \
        if props is not None else CLI_EXEC_KEY

    width = get_prop('grid_width', DEF_WIDTH, execution_key=execution_key)
    height = (width // 2) + (width % 2)

    groups = [Composite(WHITE, {"color": WHITE}, execution_key=execution_key),
              Composite(BLACK, {"color": BLACK, "marker": SQUARE},
                        execution_key=execution_key)]

    for y in range(height):
        for x in range(width):
            groups[W] += create_wolf_cell(x, y, execution_key)
    wolfram_env = Env(MODEL_NAME,
                      action=wolfram_action,
                      height=height,
                      width=width,
                      members=groups,
                      attrs={"size": 50,
                             "hide_grid_lines": True,
                             "hide_legend": True},
                      random_placing=False,
                      execution_key=execution_key
                      )

    rule_num = get_prop('rule_number', DEF_RULE, execution_key=execution_key)
    wolfram_env.set_attr("rule_num", rule_num)
    wolfram_env.set_attr("rule_dict", get_rule(rule_num))
    wolfram_env.exclude_menu_item("line_graph")

    '''
    This switch needs to happen before the environment is executed.
    Using add switch doesn't process the switch until after
    the environment is executed which breaks the model.
    '''
    top_center_agent = \
        wolfram_env.get_agent_at(width // 2, top_row(execution_key))
    switch(top_center_agent.name, WHITE, BLACK, execution_key=execution_key)

    # top row is the "previous" because we just processed it
    set_env_attr("prev_row_idx", top_row(execution_key),
                 execution_key=execution_key)


def main():
    set_up()
    get_env(execution_key=CLI_EXEC_KEY)()
    return 0


if __name__ == "__main__":
    main()
