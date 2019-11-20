"""
A basic model.
Places two groups of agents in the enviornment randomly
and moves them around randomly.
"""

from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import RED, BLUE
from indra.env import Env
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.utils import get_props

MODEL_NAME = "edgeworthbox"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_CAGENTS = 1
DEF_NUM_WAGENTS = 1
DEF_NUM_CHEESE = 10
DEF_NUM_WINE = 10

wine_group = None
cheese_group = None
env = None


def util_func(qty):
    return 10 - 0.5 * qty


def marginal_util(has_amt, want_amt):
    gain_util = util_func(want_amt + 1)
    loss_util = util_func(has_amt - 1)
    return gain_util - loss_util


def seek_a_trade(agent):
    if agent.name[0:4] == "Wine":
        nearby_agent = env.get_neighbor_of_groupX(agent,
                                                  cheese_group,
                                                  hood_size=4)
        has = "wine"
        want = "cheese"

    else:
        nearby_agent = env.get_neighbor_of_groupX(agent,
                                                  wine_group,
                                                  hood_size=4)
        want = "cheese"
        has = "wine"

    if nearby_agent is not None:
        env.user.tell("I'm " + agent.name + " and I find "
                      + nearby_agent.name)

        # agent has is what nearby agent want
        agent_has_amt = agent[has]
        agent_want_amt = agent[want]
        nearby_agent_has_amt = nearby_agent[want]
        nearby_agent_want_amt = nearby_agent[has]

        # if agent has something to trade --> calculate marginal util
        if (agent_has_amt - 1) >= 0 and (nearby_agent_has_amt - 1) >= 0:
            agent_marginal_util = marginal_util(agent_has_amt, agent_want_amt)
            nearby_agent_marginal_util = marginal_util(nearby_agent_has_amt,
                                                       nearby_agent_want_amt)

            # checking marginal utility of two agent grester than 0
            if agent_marginal_util >= 0 and nearby_agent_marginal_util >= 0:
                agent[has] -= 1
                agent[want] += 1
                nearby_agent[has] += 1
                nearby_agent[want] -= 1

    env.user.tell("I'm " + agent.name
                  + ". I have " + str(agent["wine"]) + " wine and "
                  + str(agent["cheese"]) + " cheese.")
    # return False means to move
    return False


def create_wagent(name, i, props=None):
    start_wine = DEF_NUM_WINE
    if props is not None:
        start_wine = props.get('start_wine',
                               DEF_NUM_WINE)
    return Agent(name + str(i), action=seek_a_trade,
                 attrs={"wine": start_wine, "cheese": 0})


def create_cagent(name, i, props=None):
    start_cheese = DEF_NUM_CHEESE
    if props is not None:
        start_cheese = props.get('start_cheese',
                                 DEF_NUM_CHEESE)
    return Agent(name + str(i), action=seek_a_trade,
                 attrs={"wine": 0, "cheese": start_cheese})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    pa = get_props(MODEL_NAME, props, model_dir="capital")
    cheese_group = Composite("Cheese holders", {"color": BLUE},
                             member_creator=create_cagent,
                             props=pa,
                             num_members=pa.get('num_cagents',
                                                DEF_NUM_CAGENTS))
    wine_group = Composite("Wine holders", {"color": RED},
                           member_creator=create_wagent,
                           props=pa,
                           num_members=pa.get('num_wagents',
                                              DEF_NUM_WAGENTS))

    env = Env("env",
              height=pa.get('grid_height', DEF_HEIGHT),
              width=pa.get('grid_width', DEF_WIDTH),
              members=[cheese_group, wine_group],
              props=pa)

    return (env, cheese_group, wine_group)


def main():
    global wine_group
    global cheese_group
    global env

    (env, cheese_group, wine_group) = set_up()

    if DEBUG2:
        env.user.tell(env.__repr__())

    env()
    return 0


if __name__ == "__main__":
    main()
