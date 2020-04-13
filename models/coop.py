"""
This is babysitting co-op rewritten in Indra.
The model presently has something horribly wrong with it:
    we should see only a few central bank interventions, because once
    there are enough coupons, employment should stay high.
    Instead we see them with great regularity.
"""
import random

from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env, UNLIMITED
from registry.registry import get_env, get_group, get_prop
from indra.utils import gaussian
from indra.user import user_tell, run_notice
from indra.utils import init_props

MODEL_NAME = 'coop'

DEF_BABYSITTER = 10
DEF_DESIRED_CASH_BAL = 8
DEF_COUPON = 2
DEF_DISTRIBUTING_COUPON = 2
DEF_SIGMA = 0.2
DEF_PERCENT = 10

CO_OP_MEMBERS = "Co-op members"

BABYSIT = "BABYSITTING"
GO_OUT = "GOING_OUT"

CB_intervention_points = []
num_of_rounds = 1

last_period_exchanges = 0
last_period_unemployed = 0


def wants_to_sit(agent, *args):
    """
    Checking whether the agent wants to sit
    """
    return agent["goal"] == BABYSIT


def wants_to_go_out(agent, *args):
    """
    Checking whether the agent wants to go out
    """
    return agent["goal"] == GO_OUT


def initial_exchanges(pop_hist):
    """
    Set up our pop hist object to record exchanges per period.
    """
    pop_hist.record_pop("Exchanges", 0)


def record_exchanges(pop_hist):
    """
    This is our hook into the env to record the number of exchanges each
    period.
    """
    global last_period_exchanges
    pop_hist.record_pop("Exchanges", last_period_exchanges)


def get_sitters(co_op_members):
    return co_op_members.subset(wants_to_sit)


def get_going_out(co_op_members):
    return co_op_members.subset(wants_to_go_out)


def coop_action(coop_env):
    global last_period_exchanges
    global last_period_unemployed

    sitters = get_sitters(get_group(CO_OP_MEMBERS))
    going_out = get_going_out(get_group(CO_OP_MEMBERS))

    exchanges = min(len(sitters), len(going_out))
    sitter_agents = [agent for agent in sitters]
    going_out_agents = [agent for agent in going_out]

    for i in range(exchanges):
        sitter, outer = sitter_agents[i], going_out_agents[i]
        sitters[sitter]['coupons'] += 1
        going_out[outer]['coupons'] -= 1

    last_period_exchanges = exchanges
    last_period_unemployed = max(len(sitters), len(going_out)) - exchanges
    return True


def distribute_coupons(agent):
    """
    Distribute coupons from central bank randomly to each babysitter.
    Coupons are gaussian distributed based on extra_coupons and extra_dev.
    """
    co_op_members = get_group(CO_OP_MEMBERS)
    for bbsit in co_op_members:
        co_op_members[bbsit]['coupons'] += int(gaussian(
            agent["extra_coupons"], agent["extra_dev"]))


def coop_report(coop_env):
    num_babysitter = len(get_sitters(get_group(CO_OP_MEMBERS)))
    return 'Number of babysitters is: ' + str(num_babysitter) + '\n'
    pass


def act(agent):
    """
    Co-op members act as follows:
    if their holding coupons are less than desired cash balance, they babysit,
    or there is a 50-50 chance for them to go out.
    """
    if agent['coupons'] <= agent['desired_cash']:
        agent['goal'] = "BABYSITTING"
    else:
        if random.random() > .5:
            agent['goal'] = "GOING_OUT"
        else:
            agent['goal'] = "BABYSITTING"


def babysitter_action(agent):
    act(agent)
    return False


def central_bank_action(agent):
    """
    If exchanges are down "enough", distribute coupons!
    Enough is a parameter.
    """
    global num_of_rounds
    global CB_intervention_points
    num_of_rounds += 1
    co_op_members = get_group(CO_OP_MEMBERS)
    unemployment_rates = last_period_unemployed / len(co_op_members) * 100
    unemployment_threshold = agent["percent_change"]
    if unemployment_rates >= unemployment_threshold:
        user_tell("Unemployment has risen to "
                  + str(unemployment_rates)
                  + " more than default value "
                  + str(unemployment_threshold)
                  + " CB Intervened")
        CB_intervention_points.append([num_of_rounds, last_period_exchanges])
        user_tell(CB_intervention_points)
        distribute_coupons(agent)


def create_babysitter(name, i):
    """
    Create a babysitter.
    """
    babysitter = Agent(name + str(i), action=babysitter_action)
    mean_coupons = get_prop("average_coupons", DEF_COUPON)
    dev = get_prop("deviation", DEF_SIGMA)
    babysitter["goal"] = None
    babysitter['coupons'] = int(gaussian(mean_coupons, dev))
    babysitter['desired_cash'] = get_prop("desired_cash",
                                          DEF_DESIRED_CASH_BAL)
    return babysitter


def create_central_bank(name, i):
    """
    Create the central bank to distribute the coupons
    """
    central_bank = Agent(name, action=central_bank_action)
    central_bank["percent_change"] = get_prop("percent_change",
                                              DEF_PERCENT)
    central_bank["extra_coupons"] = get_prop("extra_coupons", DEF_COUPON)
    central_bank["extra_dev"] = get_prop("extra_deviation", DEF_SIGMA)
    return central_bank


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    init_props(MODEL_NAME, props)

    num_members = get_prop('num_babysitter', DEF_BABYSITTER)
    co_op_members = Composite(CO_OP_MEMBERS, num_members=num_members,
                              member_creator=create_babysitter)
    central_bank = Composite("central_bank", num_members=1,
                             member_creator=create_central_bank)

    Env('coop_env', members=[co_op_members, central_bank],
        action=coop_action, width=UNLIMITED,
        height=UNLIMITED,
        census=coop_report,
        pop_hist_setup=initial_exchanges,
        pop_hist_func=record_exchanges,
        attrs={"show_special_points": CB_intervention_points,
               "special_points_name": "CB intervention points"})


def main():
    set_up()
    run_notice(MODEL_NAME)
    get_env()()
    return 0


if __name__ == '__main__':
    main()
