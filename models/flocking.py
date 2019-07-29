"""
    This is the flocking model written in indra.
"""

from propargs.propargs import PropArgs
from indra.utils import get_prop_path
from indra.agent import Agent
from indra.composite import Composite
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.env import Env
from indra.display_methods import BLUE, TREE

MODEL_NAME = "flocking"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_BIRDS = 10

bird_group = None
env = None


def agent_action(agent):
    # print("I'm " + agent.name + " and I'm acting.")
    # # return False means to move
    # return False
    if agent.neighbors is None:
        neighbors = agent.locator.get_moore_hood(agent, save_neighbors=False)

    if neighbors is not None:
        print("Creating Birds in a group")
    return False

    #  global on_fire

    # old_state = agent["state"]
    # if is_healthy(agent):
    #     nearby_fires = Composite(agent.name + "'s nearby fires")
    #     neighbors = agent.locator.get_moore_hood(agent,
    #                                              save_neighbors=True)
    #     if neighbors is not None:
    #         nearby_fires = neighbors.subset(is_on_fire, agent)
    #     if len(nearby_fires) > 0:
    #         if DEBUG2:
    #             print("Setting nearby tree on fire!")
    #         agent["state"] = NF

    # # if we didn't catch on fire above, do probabilistic transition:
    # if old_state == agent["state"]:
    #     agent["state"] = prob_state_trans(old_state, STATE_TRANS)

    # if old_state != agent["state"]:
    #     agent.has_acted = True
    #     agent.locator.add_switch(agent, group_map[old_state],
    #                              group_map[agent["state"]])
    # return True


def create_agent(color, i):
    """
    Create an agent.
    """
    return Agent(color + str(i), action=agent_action)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    ds_file = get_prop_path(MODEL_NAME)
    if props is None:
        pa = PropArgs.create_props(MODEL_NAME,
                                   ds_file=ds_file)
    else:
        pa = PropArgs.create_props(MODEL_NAME,
                                   prop_dict=props)

    bird_group = Composite("Birds", {"color": BLUE, "marker": TREE},
                           member_creator=create_agent,
                           num_members=pa.get('num_birds', DEF_NUM_BIRDS))

# class Space(name, width=DEF_WIDTH, height=DEF_HEIGHT,
# attrs=None, members=None, action=None, random_placing=True, serial_obj=None)

    env = Env("env",
              height=pa.get('grid_height', DEF_HEIGHT),
              width=pa.get('grid_width', DEF_WIDTH),
              members=[bird_group])
    return (bird_group, env)


def main():
    global bird_group
    global env

    (bird_group, env) = set_up()
    bird_group()
    return 0


if __name__ == "__main__":
    main()
