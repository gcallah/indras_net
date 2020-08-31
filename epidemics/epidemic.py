"""
A model to simulate the spread of virus in a city.
"""

from indra.agent import Agent, MOVE, DONT_MOVE
from indra.agent import prob_state_trans, set_trans
from indra.composite import Composite
from indra.display_methods import RED, GREEN, BLACK
from indra.display_methods import TOMATO
from indra.display_methods import BLUE, YELLOW
from indra.env import Env
from registry.execution_registry import CLI_EXEC_KEY, \
    EXEC_KEY, get_exec_key
from registry.registry import get_env, get_prop, set_env_attr
from registry.registry import user_log_err, run_notice, user_log_notif
from indra.utils import init_props
from indra.space import CircularRegion, exists_neighbor
from indra.space import distance, get_move_angle
from random import random
from math import log

MODEL_NAME = "epidemic"
DEBUG = False  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off
DEBUGSPEED = False  # turns off extra print statements to speed up modeling.

# Constants that are re-analyzed in setup
DEF_CON_DUR = 4
DEF_CON_PROB = 1 - (1 / DEF_CON_DUR)
DEF_DIM = 30
DEF_DENSITY = .20
DEF_DEATH_RATE = (1 / DEF_CON_DUR) * .06
DEF_INFEC = 0.5
DEF_IMMUNE_PER = 45
DEF_IM_HE_TRANS = 1 / DEF_IMMUNE_PER
DEF_IM_STAY = 1 - DEF_IM_HE_TRANS
DEF_SURV_RATE = (1 / DEF_CON_DUR) - DEF_DEATH_RATE
DEF_EX_HE_TRANS = 1 - DEF_INFEC
DEF_PERSON_MOVE = 3
DEF_DISTANCING = 3
DEF_INFEC = 0.02
DEF_INFEC_DIST = 2
DEF_MASK_RATE = 0.75

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
    [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # HE
    [DEF_EX_HE_TRANS, 0.0, DEF_INFEC, 0.0, 0.0, 0.0],  # EX
    [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],  # IN
    [0.0, 0.0, 0.0, DEF_CON_PROB, DEF_DEATH_RATE, DEF_SURV_RATE],  # CN
    [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],  # DEi
    [DEF_IM_HE_TRANS, 0.0, 0.0, 0.0, 0.0, DEF_IM_STAY],  # IM
]

GROUP_MAP = "group_map"
STATE = "state"


def is_isolated(agent, **kwargs):
    '''
    Checks if agent is maintaining distancing.
    '''
    execution_key = get_exec_key(kwargs=kwargs)
    return not exists_neighbor(agent,
                               size=get_prop('distancing', DEF_DISTANCING,
                                             execution_key=execution_key),
                               execution_key=execution_key)


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


def is_dead(agent, *args):
    """
    Checking whether the state is contagious or not
    """
    return agent[STATE] == DE


def epidemic_report(env, execution_key=CLI_EXEC_KEY):
    # taking data for each period using pop_hist
    pop_hist = get_env(execution_key=execution_key).pop_hist

    periods = len(pop_hist[INFECTED])
    print("period: " + str(periods))
    total_deaths = pop_hist[DEAD][periods - 1]
    curr_deaths = total_deaths - pop_hist[DEAD][periods - 2]
    curr_infected = pop_hist[INFECTED][periods - 1] - pop_hist[INFECTED][
        periods - 2]
    curr_infected = max(0, curr_infected)

    if periods > 2:
        a = max(1, (pop_hist[INFECTED][periods - 1] +
                    get_env(execution_key=execution_key).get_attr(
                        "total_cases")) /
                max(1, get_env(execution_key=execution_key).get_attr(
                    "total_cases")))
        R0_old = get_env(execution_key=execution_key).get_attr("R0")
        if (a != 1 and a != 2):
            R0 = R0_old - ((a - 2 + a ** (-R0_old)) / (log(a) * (a - 2)))
        else:
            R0 = R0_old
    else:
        R0 = 0
    if R0 < 0:
        R0 = R0_old
    get_env(execution_key=execution_key).set_attr("R0", R0)
    result = "Current period: " + str(periods - 1) + "\n"
    if DEBUGSPEED is False:
        result += "New cases: " + str(curr_infected) + "\n"

        if curr_infected > 0:
            cases = get_env(execution_key=execution_key).get_attr(
                     "total_cases")
            get_env(execution_key=execution_key).set_attr(
                    "total_cases", cases + curr_infected)

        result += "Total cases: " + \
                  str(get_env(execution_key=execution_key).get_attr(
                      "total_cases")) + "\n"
        result += "New deaths: " + str(curr_deaths) + "\n"
        result += "Total deaths: " + str(total_deaths) + "\n"

    result += "R0 value: " + str(R0) + "\n"

    return result


def social_distancing(agent, **kwargs):
    """
    This function sets a new angle for the agent's movement.
    """
    execution_key = get_exec_key(kwargs=kwargs)
    curr_region = CircularRegion(get_env(execution_key=execution_key),
                                 agent.get_pos(), DEF_PERSON_MOVE * 2)
    agents_in_range = curr_region.get_agents(
        get_env(execution_key=execution_key), pred=None)
    new_angle = get_move_angle(agent, agents_in_range)
    agent["angle"] = new_angle


def person_action(agent, **kwargs):
    """
    This is what people do each turn in the epidemic.
    """
    execution_key = get_exec_key(kwargs=kwargs)
    infec_dist = get_prop('infection_distance', DEF_INFEC_DIST,
                          execution_key=execution_key)
    old_state = agent[STATE]
    if is_healthy(agent):
        distance_mod = 1
        if agent["is_wearing_mask"]:
            distance_mod = 0.5
        curr_reg = CircularRegion(center=agent.get_pos(),
                                  radius=(2 * infec_dist * distance_mod),
                                  execution_key=execution_key)
        sub_reg = curr_reg.create_sub_reg(center=agent.get_pos(),
                                          radius=(infec_dist * distance_mod),
                                          execution_key=execution_key)
        agent_list = sub_reg.get_agents(exclude_self=True)
        if (agent_list is not None and (len(agent_list) > 0)):
            if DEBUG2:
                user_log_notif("Exposing nearby people!")
            agent[STATE] = EX
        else:
            for curr_agent in curr_reg.get_agents(exclude_self=True):
                curr_distance = (distance(curr_agent, agent) -
                                 DEF_INFEC_DIST)
                if (curr_distance > infec_dist and
                        curr_distance <= (infec_dist * 2)):
                    inverse_square_val = ((1 / (curr_distance ** 2)) *
                                          distance_mod)
                    if inverse_square_val > 0:
                        r = random()
                        if inverse_square_val / 100 > r:
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
        group_map = get_env(execution_key=execution_key).get_attr(GROUP_MAP)
        if group_map is None:
            user_log_err("group_map is None!")
            return DONT_MOVE
        agent.has_acted = True
        get_env(execution_key=execution_key).add_switch(agent,
                                                        group_map[old_state],
                                                        group_map[
                                                            agent[STATE]])

    if is_dead(agent):
        return DONT_MOVE

    if not is_isolated(agent, **kwargs):
        social_distancing(agent, **kwargs)
    return MOVE


def create_person(name, i, state=HE, **kwargs):
    """
    Create a new person!
    By default, they start out healthy.
    """
    execution_key = get_exec_key(kwargs=kwargs)
    mask_chance = random()
    mask_bool = False
    if mask_chance < get_prop("mask_rate", DEF_MASK_RATE,
                              execution_key=execution_key):
        mask_bool = True
    person = Agent(name + str(i), action=person_action,
                   attrs={STATE: state, "angle": None,
                          "max_move":
                              get_prop('person_move', DEF_PERSON_MOVE,
                                       execution_key=execution_key),
                          "is_wearing_mask": mask_bool},
                   execution_key=execution_key)
    return person


def set_env_attrs(execution_key=CLI_EXEC_KEY):
    user_log_notif("Setting env attrs for " + MODEL_NAME)
    set_env_attr(GROUP_MAP,
                 {HE: HEALTHY,
                  EX: EXPOSED,
                  IN: INFECTED,
                  CN: CONTAGIOUS,
                  DE: DEAD,
                  IM: IMMUNE}, execution_key)
    set_env_attr("census_func", epidemic_report, execution_key)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    init_props(MODEL_NAME, props, model_dir="epidemics")

    execution_key = int(props[EXEC_KEY].val) \
        if props is not None else CLI_EXEC_KEY

    city_height = get_prop('grid_height', DEF_DIM, execution_key=execution_key)
    city_width = get_prop('grid_width', DEF_DIM, execution_key=execution_key)
    city_density = get_prop('density', DEF_DENSITY,
                            execution_key=execution_key)
    immune_per = get_prop('immune_per', DEF_IMMUNE_PER,
                          execution_key=execution_key)
    death_rate = get_prop('death_rate', DEF_DEATH_RATE,
                          execution_key=execution_key)
    initial_infected = get_prop('initial_infected', DEF_INFEC,
                                execution_key=execution_key)
    contagious_duration = get_prop('contagious_duration', DEF_CON_DUR,
                                   execution_key=execution_key)
    infec = get_prop('infec', DEF_INFEC, execution_key=execution_key)
    immune_rate = 1 / immune_per

    # Replace state trans values with updated values

    set_trans(STATE_TRANS, EX, IN, infec, HE)
    set_trans(STATE_TRANS, CN, DE, (1 / contagious_duration) * death_rate)
    set_trans(STATE_TRANS, CN, IM,
              (1 / contagious_duration) * (1 - death_rate))
    set_trans(STATE_TRANS, CN, CN, 1 - (1 / contagious_duration))
    set_trans(STATE_TRANS, IM, HE, immune_rate, IM)

    pop_cnt = int(city_height * city_width * city_density)
    groups = []
    groups.append(Composite(HEALTHY, {"color": GREEN},
                            member_creator=create_person,
                            num_members=int(pop_cnt * (1 - initial_infected)),
                            state=HE, execution_key=execution_key))
    groups.append(Composite(EXPOSED, {"color": YELLOW},
                            member_creator=create_person,
                            num_members=1,
                            state=EX, execution_key=execution_key))
    groups.append(Composite(INFECTED, {"color": TOMATO},
                            member_creator=create_person,
                            num_members=int(pop_cnt * initial_infected),
                            state=IN, execution_key=execution_key))
    groups.append(Composite(CONTAGIOUS, {"color": RED},
                            member_creator=create_person,
                            num_members=1,
                            state=CN, execution_key=execution_key))
    groups.append(Composite(DEAD, {"color": BLACK},
                            member_creator=create_person,
                            num_members=1,
                            state=DE, execution_key=execution_key))
    groups.append(Composite(IMMUNE, {"color": BLUE},
                            member_creator=create_person,
                            num_members=1,
                            state=IM, execution_key=execution_key))

    Env(MODEL_NAME, height=city_height, width=city_width, members=groups,
        execution_key=execution_key)
    get_env(execution_key=execution_key).set_attr("total_cases", 0)
    set_env_attrs(execution_key=execution_key)


def main():
    set_up()
    run_notice(MODEL_NAME)
    get_env()()
    return 0


if __name__ == "__main__":
    main()
