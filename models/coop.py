"""
This is babysitting co-op rewritten in Indra.
"""
import random

from indra.utils import get_props
from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env, UNLIMITED
from indra.display_methods import BLUE, ORANGE, RED, PURPLE, BLACK
from indra.space import gaussian_distribution

MODEL_NAME = 'coop'

DEF_BABYSITTER = 10
DEF_MIN_HOLDING = 3
DEF_COUPON = 2
DEF_DISTRIBUTING_COUPON = 2
DEF_SIGMA = 0.2
DEF_PERCENT = 10

BSIT_INDEX = 0
GO_OUT_INDEX = 1
B_HOME = 2
G_HOME = 3
CENTRAL_BANK = 4

groups = None
group_indices = None
coop_env = None


def classify_goal(coop_env):
    b_group = []
    g_group = []
    for i in range(4):
        for agent in groups[i]:
            if groups[i][agent]["goal"] == "BABYSITTING":
                groups[i][agent]["sitting"] = True
                groups[i][agent]["goal"] = None
                b_group.append(groups[i][agent])

            elif groups[i][agent]["goal"] == "GOING_OUT":
                groups[i][agent]["going_out"] = True
                groups[i][agent]["goal"] = None
                g_group.append(groups[i][agent])
    return (b_group, g_group)


def classify_group(b_group, g_group):
    for agent in b_group:
        if agent.primary_group() is not None:
            index = group_indices[agent.primary_group().name]
            coop_env.now_switch(agent, groups[index], groups[BSIT_INDEX])

    for agent in g_group:
        if agent.primary_group() is not None:
            index = group_indices[agent.primary_group().name]
            coop_env.now_switch(agent, groups[index], groups[GO_OUT_INDEX])


def exchange(coop_env):
    num_babysitter = len(groups[BSIT_INDEX])
    num_going_out = len(groups[GO_OUT_INDEX])
    exchange_num = min(num_babysitter, num_going_out)

    cnt_0 = 0
    cnt_1 = 0
    for agent in groups[BSIT_INDEX]:
        if cnt_0 < exchange_num:
            cnt_0 += 1
            groups[BSIT_INDEX][agent]['sitting'] = False
            groups[BSIT_INDEX][agent]['coupons'] += 1

    for agent in groups[GO_OUT_INDEX]:
        if cnt_1 < exchange_num:
            cnt_1 += 1
            groups[GO_OUT_INDEX][agent]['going_out'] = False
            groups[GO_OUT_INDEX][agent]['coupons'] -= 1

    cur_index = -1
    action = ""
    if num_babysitter > exchange_num:
        cur_index = 0
        action = "sitting"
    else:
        cur_index = 1
        action = "going_out"

    swiches = []
    for agent in groups[cur_index]:
        if groups[cur_index][agent][action] is True:
            swiches.append(groups[cur_index][agent])

    for agent in swiches:
        coop_env.now_switch(agent, groups[cur_index], groups[2 + cur_index])


def distribute_coupons(agent):
    for i in range(4):
        for bbsit in groups[i]:
            groups[i][bbsit]["coupons"] += int(gaussian_distribution(agent["extra_coupons"], agent["extra_dev"]))  # NOQA E501


def coop_action(coop_env):
    (b_group, g_group) = classify_goal(coop_env)
    classify_group(b_group, g_group)
    exchange(coop_env)


def coop_report(coop_env):
    num_babysitter = len(groups[BSIT_INDEX])
    num_going_out = len(groups[GO_OUT_INDEX])
    return 'Number of babysitters is: ' + str(num_babysitter) \
        + ', number of people going out is: ' + str(num_going_out) \
        + ', number of people staying home_B is: ' \
        + str(len(groups[B_HOME])) \
        + ', number of people staying home_G is: ' \
        + str(len(groups[G_HOME])) + '\n'


def act(agent):
    if agent['coupons'] <= agent['min_holding']:
        agent['goal'] = "BABYSITTING"
        agent['sitting'] = True
    else:
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
    print(agent.name,
          'babysitting: ',
          agent['sitting'],
          ' and going_out ',
          agent['going_out'],
          ' and I have ',
          agent['coupons'],
          ' coupons')
    return False


def central_bank_action(agent):
    num_home = len(groups[G_HOME]) + len(groups[B_HOME])
    hist = groups[CENTRAL_BANK]["CENTRAL_BANK"]["num_hist"]
    if len(hist) > 0:
        prev_num_home = hist[-1]
        if prev_num_home != 0:
            if (num_home / prev_num_home * 100) >= groups[CENTRAL_BANK]["CENTRAL_BANK"]["percent_change"]:  # NOQA E501
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
    babysitter['min_holding'] = props.get("min_holding", DEF_MIN_HOLDING)
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

    num_members = num_members = pa.get('num_babysitter', DEF_BABYSITTER)

    # There are 4 groups: group of babysitters, group of people going out,
    # group of people who want to babysit but cannot,
    # group of people who want to go out but cannot.

    groups.append(Composite("BBSIT", {"color": BLUE}))
    groups.append(Composite("GO_OUT", {"color": RED}))
    groups.append(Composite("B_HOME", {"color": PURPLE}))
    groups.append(Composite("G_HOME", {"color": ORANGE}))
    groups.append(Composite("CENTRAL_BANK", {"color": BLACK},
                            props=pa,
                            member_creator=create_central_bank,
                            num_members=1))

    for i in range(4):
        group_indices[groups[i].name] = i

    for i in range(num_members):
        groups[BSIT_INDEX] += create_babysitter('Babysitters', i, pa)

    coop_env = Env('coop_env', members=groups,
                   action=coop_action, width=UNLIMITED,
                   height=UNLIMITED,
                   census=coop_report,
                   props=pa,
                   exclude_member="CENTRAL_BANK")

    return (coop_env, groups, group_indices)


def main():
    global groups
    global group_indices
    global central_bank
    global coop_env

    (coop_env, groups, group_indices) = set_up()

    coop_env()
    return 0


if __name__ == '__main__':
    main()
