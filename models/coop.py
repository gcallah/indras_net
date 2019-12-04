"""
This is babysitting co-op rewritten in Indra.
"""
import random

from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env, UNLIMITED
from indra.space import gaussian_distribution
from indra.utils import get_props

MODEL_NAME = 'coop'

DEF_BABYSITTER = 10
DEF_DESIRED_CASH_BAL = 8
DEF_COUPON = 2
DEF_DISTRIBUTING_COUPON = 2
DEF_SIGMA = 0.2
DEF_PERCENT = 10
# DEF_DISTRIBUTE_THRESHOLD = 5

BSIT_INDEX = 0
GO_OUT_INDEX = 1
B_HOME = 2
G_HOME = 3
CENTRAL_BANK = 4
NUM_OF_GROUPS = 4

BABYSIT = "BABYSITTING"
GO_OUT = "GOING_OUT"
CB_intervention_points = []
# num_of_rounds = 0

coop_members = None
coop_env = None

last_period_exchanges = 0
last_period_unemployed = 0


def wants_to_sit(agent, *args):
    """
    Checking whether the state is healthy or not
    """
    return agent["goal"] == BABYSIT


def wants_to_go_out(agent, *args):
    """
    Checking whether the state is healthy or not
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


def get_sitters(coop_members):
    return coop_members.subset(wants_to_sit)


def get_going_out(coop_members):
    return coop_members.subset(wants_to_go_out)


def exchange(coop_env):
    # get exchange numbers
    global last_period_exchanges
    global last_period_unemployed
    global coop_members

    sitters = get_sitters(coop_members)
    going_out = get_going_out(coop_members)

    exchanges = min(len(sitters), len(going_out))
    sitter_agents = [agent for agent in sitters]
    going_out_agents = [agent for agent in going_out]

    for i in range(exchanges):
        sitter, outer = sitter_agents[i], going_out_agents[i]
        sitters[sitter]['coupons'] += 1
        going_out[outer]['coupons'] -= 1

    last_period_exchanges = exchanges
    last_period_unemployed = max(len(sitters), len(going_out)) - exchanges


def distribute_coupons(agent):
    """
    Distribute coupons from central bank randomly to each babysitter.
    Coupons are gaussian distributed based on extra_coupons and extra_dev.
    """
    global coop_members
    for bbsit in coop_members:
        coop_members[bbsit]['coupons'] += int(gaussian_distribution(
            agent["extra_coupons"], agent["extra_dev"]))


def coop_action(coop_env):
    exchange(coop_env)


def coop_report(coop_env):
    num_babysitter = len(get_sitters(coop_members))
    return 'Number of babysitters is: ' + str(num_babysitter) + '\n'
    pass


def act(agent):
    """
    Co-op members act as follows:
    if their holding coupons are less than desired cash balance, they babysit,
    or there is a 50-50 chance for them to go out.
    """
    print(str(agent), "coupons = ", agent['coupons'],
          "desired = ", agent['desired_cash'])
    if agent['coupons'] <= agent['desired_cash']:
        agent['goal'] = "BABYSITTING"
    else:
        # print(str(agent), "is not in first if!")
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
    global coop_members
    global num_of_rounds
    # num_of_rounds += 1
    # print("num_of_rounds: ", str(num_of_rounds))
    unemployment_rates = last_period_unemployed / len(coop_members) * 100
    unemployment_threshold = agent["percent_change"]
    if unemployment_rates >= unemployment_threshold:
        print("Unemployment has up to ", str(unemployment_rates),
              "more than default value " + str(unemployment_threshold),
              " CB Intervened")
        CB_intervention_points.append(last_period_exchanges)
        print(CB_intervention_points)
        distribute_coupons(agent)


def create_babysitter(name, i, props=None):
    """
    Create a babysitter.
    """
    babysitter = Agent(name + str(i), action=babysitter_action)
    mean_coupons = props.get("average_coupons", DEF_COUPON)
    dev = props.get("deviation", DEF_SIGMA)
    babysitter["goal"] = None
    babysitter['coupons'] = int(gaussian_distribution(mean_coupons, dev))
    babysitter['desired_cash'] = props.get("desired_cash",
                                           DEF_DESIRED_CASH_BAL)
    return babysitter


def create_central_bank(name, i, props=None):
    """
    Create the central bank to distribute the coupons
    """
    central_bank = Agent(name, action=central_bank_action)
    central_bank["percent_change"] = props.get("percent_change", DEF_PERCENT)
    central_bank["extra_coupons"] = props.get("extra_coupons", DEF_COUPON)
    central_bank["extra_dev"] = props.get("extra_deviation", DEF_SIGMA)
    # central_bank["distribute_threshold"] = props.get("distribute_threshold",
    #                                                  DEF_DISTRIBUTE_THRESHOLD)
    return central_bank


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    global coop_env
    global coop_members
    pa = get_props(MODEL_NAME, props)

    num_members = pa.get('num_babysitter', DEF_BABYSITTER)
    coop_members = Composite("Coop_members", num_members=num_members,
                             member_creator=create_babysitter,
                             props=pa)
    central_bank = Composite("central_bank", num_members=1,
                             member_creator=create_central_bank,
                             props=pa)

    coop_env = Env('coop_env', members=[coop_members, central_bank],
                   action=coop_action, width=UNLIMITED,
                   height=UNLIMITED,
                   census=coop_report,
                   props=pa,
                   pop_hist_setup=initial_exchanges,
                   pop_hist_func=record_exchanges,
                   attrs={"show_special_points": True})
    return (coop_env, coop_members, central_bank)


def main():
    global coop_env
    global coop_members
    global central_bank
    # global num_of_rounds

    (coop_env, coop_members, central_bank) = set_up()

    coop_env()
    return 0


if __name__ == '__main__':
    main()
