"""
A model to simulate the spread of virus in a city.
"""
from random import randint
from math import atan, degrees

from indra.agent import Agent
from indra.agent import prob_state_trans, set_trans
from indra.composite import Composite
from indra.display_methods import RED, GREEN, BLACK
from indra.display_methods import TOMATO
from indra.display_methods import BLUE, YELLOW
from indra.env import Env
from registry.registry import get_env, get_prop
from registry.registry import user_log_err, run_notice, user_log_notif
from indra.utils import init_props
from indra.space import distance

MODEL_NAME = "epidemic"
DEBUG = False  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

NEARBY = 1.8


# Constants that are re-analyzed in setup
DEF_DIM = 30
DEF_DENSITY = .44
DEF_DEATH_RATE = .06
DEF_INFEC = 0.5
DEF_IMMUNE_PER = 10
DEF_IM_HE_TRANS = 1 / DEF_IMMUNE_PER
DEF_IM_STAY = 1 - DEF_IM_HE_TRANS
DEF_SURV_RATE = 1 - DEF_DEATH_RATE
DEF_EX_HE_TRANS = 1 - DEF_INFEC
DEF_PERSON_MOVE = 3
DEF_DISTANCING = 2

PERSON_PREFIX = "Person"

# health condition strings
HEALTHY = "Healthy"
EXPOSED = "Exposed"
INFECTED = "Infected"
CONTAGIOUS = "Contagious"
DEAD = "Dead"
IMMUNE = "Immune"

# state numbers: create as strings for JSON,
# convert to int when we need 'em that way
# these should be changed to 2 letter abbreviations of the above.
HE = "0"
EX = "1"
IN = "2"
CN = "3"
DE = "4"
IM = "5"


STATE_TRANS = [
    # HE    EX   IN   CN   DE    IM
    [.985, .015, 0.0, 0.0, 0.0,  0.0],  # HE
    [DEF_EX_HE_TRANS,  0.0,  DEF_INFEC, 0.0, 0.0,  0.0],  # EX
    [0.0,  0.0,  0.0, 1.0, 0.0,  0.0],  # IN
    [0.0,  0.0,  0.0, 0.0, DEF_DEATH_RATE, DEF_SURV_RATE],  # CN
    [0.0,  0.0,  0.0, 0.0, 1.0,  0.0],  # DE
    [DEF_IM_HE_TRANS,  0.0,  0.0, 0.0, 0.0,  DEF_IM_STAY],  # IM
]


GROUP_MAP = "group_map"
STATE = "state"


def is_isolated(agent):
    '''
    Checks if agent is maintaining distancing.
    '''
    return (distance(get_env().get_closest_agent(agent), agent) >=
            get_prop('distancing', DEF_DISTANCING))


def is_healthy(agent, *args):
    """
    Checking whether the state is healthy or not
    """
    return agent[STATE] == HE


def is_contagious(agent, *args):
    """
    Checking whether the state is contagious or not
    """
    return agent[STATE] == CN


def epidemic_report(env):
    return "epicdemic_report in progress"+"\n"


def people_action(agent):
    """
    This is what people do each turn in the city.
    """
    old_state = agent[STATE]
    if is_healthy(agent):
        neighbors = get_env().get_moore_hood(agent)
        if neighbors is not None:
            nearby_virus = neighbors.subset(is_contagious, agent)
            if len(nearby_virus) > 0:
                if DEBUG2:
                    user_log_notif("Exposing nearby people!")
                agent[STATE] = EX

    # if we didn't catch disease above, do probabilistic transition:
    if old_state == agent[STATE]:
        # we gotta do these str/int shenanigans with state cause
        # JSON only allows strings as dict keys
        agent[STATE] = str(prob_state_trans(int(old_state), STATE_TRANS))
        if agent[STATE] == EX:
            user_log_notif("Person spontaneously catching virus.")

    if old_state != agent[STATE]:
        # if we entered a new state, then...
        group_map = get_env().get_attr(GROUP_MAP)
        if group_map is None:
            user_log_err("group_map is None!")
            return True
        agent.has_acted = True
        get_env().add_switch(agent,
                             group_map[old_state],
                             group_map[agent[STATE]])

    if(not is_isolated(agent)):
        if agent["angle"] is None:
            new_angle = randint(0, 360)
        else:
            other_agent = get_env().get_closest_agent(agent)
            x_dif = other_agent.get_x() - agent.get_x()
            y_dif = other_agent.get_y() - agent.get_y()
            if (x_dif != 0 and y_dif != 0):
                if (x_dif > 0):
                    new_angle = 180 + degrees(atan(y_dif / x_dif))
                else:
                    new_angle = degrees(atan(y_dif / x_dif))
            elif (y_dif != 0):
                if(y_dif > 0):
                    new_angle = 270
                else:
                    new_angle = 90
            else:
                if(x_dif > 0):
                    new_angle = 180
                else:
                    new_angle = 0
        if (new_angle > 360):
            new_angle = new_angle % 360
        agent["angle"] = new_angle

    if agent[STATE] == DE:
        return True
    else:
        return False


def create_person(name, i, state=HE):
    """
    Create a new person!
    By default, they start out healthy.
    """
    name = PERSON_PREFIX

    person = Agent(name + str(i), action=people_action,
                   attrs={STATE: state, "save_neighbors": True})
    person["angle"] = None
    person["max_move"] = get_prop('person_move', DEF_PERSON_MOVE)
    return person


def set_env_attrs():
    user_log_notif("Setting env attrs for basic epidemic.")
    env = get_env()
    env.set_attr(GROUP_MAP,
                 {HE: HEALTHY,
                  EX: EXPOSED,
                  IN: INFECTED,
                  CN: CONTAGIOUS,
                  DE: DEAD,
                  IM: IMMUNE})
    env.set_attr("census_func", epidemic_report)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    init_props(MODEL_NAME, props, model_dir="epidemics")

    city_height = get_prop('grid_height', DEF_DIM)
    city_width = get_prop('grid_width', DEF_DIM)
    city_density = get_prop('density', DEF_DENSITY)
    immune_per = get_prop('immune_per', DEF_IMMUNE_PER)
    death_rate = get_prop('death_rate', DEF_DEATH_RATE)
    infec = get_prop('infec', DEF_INFEC)
    immune_rate = 1 / immune_per

    # Replace state trans values with updated values
    set_trans(STATE_TRANS, EX, IN, infec, HE)
    set_trans(STATE_TRANS, CN, DE, death_rate, IM)
    set_trans(STATE_TRANS, IM, HE, immune_rate, IM)

    pop_cnt = int(city_height * city_width * city_density)
    groups = []
    groups.append(Composite(HEALTHY, {"color": GREEN},
                            member_creator=create_person,
                            num_members=pop_cnt,
                            state=HE))
    groups.append(Composite(EXPOSED, {"color": YELLOW},
                            member_creator=create_person,
                            num_members=1,
                            state=EX))
    groups.append(Composite(INFECTED, {"color": TOMATO},
                            member_creator=create_person,
                            num_members=1,
                            state=IN))
    groups.append(Composite(CONTAGIOUS, {"color": RED},
                            member_creator=create_person,
                            num_members=1,
                            state=CN))
    groups.append(Composite(DEAD, {"color": BLACK},
                            member_creator=create_person,
                            num_members=1,
                            state=DE))
    groups.append(Composite(IMMUNE, {"color": BLUE},
                            member_creator=create_person,
                            num_members=1,
                            state=IM))
    Env(MODEL_NAME, height=city_height, width=city_width, members=groups)
    set_env_attrs()


def main():
    set_up()
    run_notice(MODEL_NAME)
    get_env()()
    return 0


if __name__ == "__main__":
    main()
