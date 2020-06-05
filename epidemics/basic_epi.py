"""
A model to simulate the spread of virus in a city.
"""

from indra.agent import Agent
from indra.agent import prob_state_trans
from indra.composite import Composite
from indra.display_methods import RED, GREEN, BLACK
from indra.display_methods import SPRINGGREEN, TOMATO, TREE
from indra.display_methods import BLUE
from indra.env import Env
from registry.registry import get_env, get_prop
from registry.registry import user_log_err, run_notice, user_log_notif 
from indra.utils import init_props

MODEL_NAME = "basic_epi"
DEBUG = False  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

NEARBY = 1.8

DEF_DIM = 30
DEF_DENSITY = .44

PERSON_PREFIX = "Person"

# health condition strings
# We need: CONTAGIOUS, DEAD, IMMUNE
HEALTHY = "Healthy"
INFECTED = "Infected"
CONTAGIOUS = "Contagious"
DEAD = "Dead"
IMMUNE = "Immune"

# state numbers: create as strings for JSON,
# convert to int when we need 'em that way
# these should be changed to 2 letter abbreviations of the above.
HE = "0"
IN = "1"
CN = "2"
DE = "3"
IM = "4"

STATE_TRANS = [
    [.985, .015, 0.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.06, 0.94],
    [0.0, 0.0, 0.0, 1.0, 0.0],
    [.10, 0.0, 0.0, 0.0, .90],
]

GROUP_MAP = "group_map"


def is_healthy(agent, *args):
    """
    Checking whether the state is healthy or not
    """
    return agent["state"] == HE


def is_contagious(agent, *args):
    """
    Checking whether the state is contagious or not
    """
    return agent["state"] == CN


def people_action(agent):
    """
    This is what people do each turn in the city.
    """
    old_state = agent["state"]
    if is_healthy(agent):
        neighbors = get_env().get_moore_hood(agent)
        if neighbors is not None:
            nearby_virus = neighbors.subset(is_contagious, agent)
            if len(nearby_virus) > 0:
                if DEBUG2:
                    user_log_notif("Infecting nearby people!")
                agent["state"] = IN

    # if we didn't catch disease above, do probabilistic transition:
    if old_state == agent["state"]:
        # we gotta do these str/int shenanigans with state cause
        # JSON only allows strings as dict keys
        agent["state"] = str(prob_state_trans(int(old_state), STATE_TRANS))
        if agent["state"] == IN:
            user_log_notif("Person spontaneously catching virus.")

    if old_state != agent["state"]:
        # if we entered a new state, then...
        group_map = get_env().get_attr(GROUP_MAP)
        if group_map is None:
            user_log_err("group_map is None!")
            return True
        agent.has_acted = True
        get_env().add_switch(agent,
                             group_map[old_state],
                             group_map[agent["state"]])
    return False


def create_person(name, i, state=HE):
    """
    Create a new person!
    By default, they start out healthy.
    """
    name = PERSON_PREFIX
    return Agent(name + str(i),
                 action=people_action,
                 attrs={"state": state,
                        "save_neighbors": True})


def set_env_attrs():
    user_log_notif("Setting env attrs for basic epidemic.")
    get_env().set_attr(GROUP_MAP,
                       {HE: HEALTHY,
                        IN: INFECTED,
                        CN: CONTAGIOUS,
                        DE: DEAD,
                        IM: IMMUNE})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    init_props(MODEL_NAME, props, model_dir="epidemics")

    city_height = get_prop('grid_height', DEF_DIM)
    city_width = get_prop('grid_width', DEF_DIM)
    city_density = get_prop('density', DEF_DENSITY)
    pop_cnt = int(city_height * city_width * city_density)
    groups = []
    groups.append(Composite(HEALTHY, {"color": GREEN},
                  member_creator=create_person,
                  num_members=pop_cnt))
    groups.append(Composite(INFECTED, {"color": TOMATO}))
    groups.append(Composite(CONTAGIOUS, {"color": RED}))
    groups.append(Composite(DEAD, {"color": BLACK}))
    groups.append(Composite(IMMUNE, {"color": BLUE}))

    Env(MODEL_NAME, height=city_height, width=city_width, members=groups)
    set_env_attrs()


def main():
    set_up()
    run_notice(MODEL_NAME)
    get_env()()
    return 0


if __name__ == "__main__":
    main()



