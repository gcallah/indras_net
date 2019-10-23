"""
This is babysitting co-op rewritten in Indra.
"""
import random

from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import BLUE, ORANGE, RED, PURPLE, BLACK
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

BSIT_INDEX = 0
GO_OUT_INDEX = 1
B_HOME = 2
G_HOME = 3
CENTRAL_BANK = 4
NUM_OF_GROUPS = 4

BABYSIT = "BABYSITTING"
GO_OUT = "GOING_OUT"


groups = None
group_indices = None
coop_env = None

coop_members = None

last_period_exchanges = 0


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


def classify_goal(coop_env):
    b_group = []
    g_group = []
    for i in range(NUM_OF_GROUPS):
        for agent in groups[i]:
            if groups[i][agent]["goal"] == BABYSIT:
                groups[i][agent]["sitting"] = True
                groups[i][agent]["goal"] = None
                b_group.append(groups[i][agent])
            elif groups[i][agent]["goal"] == GO_OUT:
                groups[i][agent]["going_out"] = True
                groups[i][agent]["goal"] = None
                g_group.append(groups[i][agent])
    return (b_group, g_group)


def classify_group(b_group, g_group):
    classify_agent_group(b_group, BSIT_INDEX)
    classify_agent_group(g_group, GO_OUT_INDEX)


def classify_agent_group(group, index):
    for agent in group:
        if agent.primary_group() is not None:
            index = group_indices[agent.primary_group().name]
            coop_env.now_switch(agent, groups[index], groups[index])


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


def exchange(coop_env):

    global last_period_exchanges
    global coop_members
    # sitters = groups[BSIT_INDEX].subset(wants_to_sit)
    # going_out = coop_members.members.subset(wants_to_go_out)
    sitters = groups[BSIT_INDEX]
    going_out = groups[GO_OUT_INDEX]
    exchanges = min(len(sitters), len(going_out))

    for i in range(exchanges):
        # going out agent gives one coupon to babysitting agent
        sitter = sitters['Babysitters' + str(i + 1)]
        sitter['sitting'] = False
        sitter['coupons'] += 1
        going_outer = going_out['Babysitters' + str(i + 1)]
        going_outer['goint_out'] = False
        going_outer['coupons'] -= 1

    # record exchanges in population history
    # last_period_exchanges = exchanges


def distribute_coupons(agent):
    """
    Distribute coupons from central bank randomly to each babysitter.
    Coupons are gaussian distributed based on extra_coupons and extra_dev.
    """

    for i in range(NUM_OF_GROUPS):
        for bbsit in groups[i]:
            groups[i][bbsit]["coupons"] += int(gaussian_distribution(
                agent["extra_coupons"], agent["extra_dev"]))


def coop_action(coop_env):
    (b_group, g_group) = classify_goal(coop_env)
    classify_group(b_group, g_group)
    exchange(coop_env)


def coop_report(coop_env):
    num_babysitter = len(groups[BSIT_INDEX])
    return 'Number of babysitters is: ' + str(num_babysitter) \
           + ', number of people staying home_B is: ' \
           + str(len(groups[B_HOME])) \
           + ', number of people staying home_G is: ' \
           + str(len(groups[G_HOME])) + '\n'


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
        agent['sitting'] = True
    else:
        print(str(agent), "is not in first if!")
        if random.random() > .5:
            agent['goal'] = "GOING_OUT"
            agent['sitting'] = True

        else:
            agent['goal'] = "BABYSITTING"
            agent['going_out'] = True


def babysitter_action(agent):
    agent['sitting'] = False
    agent['going_out'] = False
    act(agent)
    return False


def central_bank_action(agent):
    num_home = len(groups[G_HOME]) + len(groups[B_HOME])
    hist = groups[CENTRAL_BANK]["CENTRAL_BANK"]["num_hist"]
    if len(hist) > 0:
        prev_num_home = hist[-1]
        if prev_num_home != 0:
            if ((num_home / prev_num_home * 100)
                    >= groups[CENTRAL_BANK]["CENTRAL_BANK"]["percent_change"]):
                distribute_coupons(agent)
    groups[CENTRAL_BANK]["CENTRAL_BANK"]["num_hist"].append(num_home)


def create_babysitter(name, i, props=None):
    """
    Create a babysitter.
    """
    babysitter = Agent(name + str(i), action=babysitter_action)
    mean_coupons = props.get("average_coupons", DEF_COUPON)
    dev = props.get("deviation", DEF_SIGMA)
    babysitter['sitting'] = False
    babysitter['going_out'] = False
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
    central_bank["num_hist"] = []
    return central_bank


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    global coop_env
    global groups
    global group_indices
    pa = get_props(MODEL_NAME, props)

    groups = []
    group_indices = {}

    num_members = pa.get('num_babysitter', DEF_BABYSITTER)

    # There are 4 groups: group of babysitters, group of people going out,
    # group of people who want to babysit but cannot,
    # group of people who want to go out but cannot.

    # groups.append(Composite("COOP_MEMBERS"))

    groups.append(Composite("BBSIT", {"color": BLUE}))
    groups.append(Composite("GO_OUT", {"color": RED}))
    groups.append(Composite("B_HOME", {"color": PURPLE}))
    groups.append(Composite("G_HOME", {"color": ORANGE}))
    groups.append(Composite("CENTRAL_BANK", {"color": BLACK},
                            props=pa,
                            member_creator=create_central_bank,
                            num_members=1))

    for i in range(NUM_OF_GROUPS):
        group_indices[groups[i].name] = i

    for i in range(num_members):
        groups[BSIT_INDEX] += create_babysitter('Babysitters', i, pa)
        i += 1
        if i < num_members:
            groups[GO_OUT_INDEX] += create_babysitter('Babysitters', i, pa)

    coop_env = Env('coop_env', members=groups,
                   action=coop_action, width=UNLIMITED,
                   height=UNLIMITED,
                   census=coop_report,
                   props=pa,
                   pop_hist_setup=initial_exchanges,
                   pop_hist_func=record_exchanges,
                   exclude_member="CENTRAL_BANK")

    return (coop_env, groups, group_indices)


def main():
    global groups
    global group_indices
    global central_bank
    global coop_env
    global coop_members

    (coop_env, groups, group_indices) = set_up()
    coop_members = groups[BSIT_INDEX]

    coop_env()
    return 0


if __name__ == '__main__':
    main()
