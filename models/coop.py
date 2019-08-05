"""
This is babysitting co-op rewritten in Indra.
"""

import random
from indra.utils import get_props
from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env, UNLIMITED

MODEL_NAME = 'coop'

DEF_BABYSITTER = 10
DEF_MIN_HOLDING = 1
DEF_COUPON = 2
DEF_NUM_STAGNANT = 3
DEF_DISTRIBUTING_COUPON = 2

groups = None
group_indices = None
coop_env = None


def coop_action(coop_env):
    num_babysitter = len(groups[0])
    num_going_out = len(groups[1])
    exchange_num = min(num_babysitter, num_going_out)

    cnt_0 = 0
    cnt_1 = 0
    for agent in groups[0]:
        if cnt_0 < exchange_num:
            cnt_0 += 1
            groups[0][agent]['sitting'] = False
            groups[0][agent]['coupons'] += 1

    for agent in groups[1]:
        if cnt_1 < exchange_num:
            cnt_1 += 1
            groups[1][agent]['going_out'] = False
            groups[1][agent]['coupons'] -= 1

    cur_index = -1
    if num_babysitter > exchange_num:
        cur_index = 0
    else:
        cur_index = 1

    swiches = []
    for agent in groups[cur_index]:
        if (groups[cur_index][agent]['sitting'] is True or groups[cur_index][agent]['going_out'] is True):  # noqa: E501
            swiches.append(groups[cur_index][agent])

    for agent in swiches:
        coop_env.now_switch(agent, groups[cur_index], groups[2])

    print(
        'Inside coop_action: ',
        len(groups[0]),
        ' and ',
        len(groups[1]),
        ' and ',
        len(groups[2]))


def coop_report(coop_env):
    num_babysitter = len(groups[0])
    num_going_out = len(groups[1])
    num_staying_home = len(groups[2])
    return 'Number of babysitters is: ' + str(num_babysitter) \
        + ', number of people going out is: ' + str(num_going_out) \
        + ', number of people staying home is: ' \
        + str(num_staying_home) + '\n'


def act(agent):
    cur_index = group_indices[agent.primary_group().name]
    if agent['coupons'] < agent['min_holding']:
        agent['sitting'] = True
    elif agent['coupons'] > agent['min_holding']:
        if random.random() > .5:
            agent['going_out'] = True
        else:
            agent['sitting'] = True

    cur_index = group_indices[agent.primary_group().name]
    if agent['sitting'] is True:
        coop_env.add_switch(agent, groups[cur_index], groups[0])
    else:
        coop_env.add_switch(agent, groups[cur_index], groups[1])


def distribute_coupons(group):
    for member in group.members:
        group[member]['coupons'] += DEF_DISTRIBUTING_COUPON


def babysitter_action(agent):
    act(agent)
    print(
        'babysitting: ',
        agent['sitting'],
        ' and going_out ',
        agent['going_out'],
        ' and I have ',
        agent['coupons'],
        ' coupons')

    # return False means to move

    return False


def central_bank_action(agent):
    if len(groups[0]) == 0:
        central_bank['stagnant_period'] += 1
    if central_bank['stagnant_period'] >= DEF_NUM_STAGNANT:
        print('stagnant_period reaches the threshold')


def create_babysitter(name, i):
    """
  Create a babysitter.
  """

    babysitter = Agent(name + str(i), action=babysitter_action)
    babysitter['sitting'] = False
    babysitter['going_out'] = False
    babysitter['coupons'] = DEF_COUPON
    babysitter['min_holding'] = DEF_MIN_HOLDING
    return babysitter


def create_central_bank(name):
    """
  Create the central bank to distribute the coupons
  """

    central_bank = Agent(name, action=central_bank_action)
    central_bank['stagnant_period'] = 0
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

    groups.append(Composite('Babysitting'))
    groups.append(Composite('Going_out'))
    groups.append(Composite('Staying_home'))

    for i in range(3):
        group_indices[groups[i].name] = i

    for i in range(num_members):
        groups[0] += create_babysitter('Babysitters', i)

    central_bank = create_central_bank('central_bank')
    coop_env = Env(
        'coop_env',
        members=[groups[0], groups[1], groups[2], central_bank],
        action=coop_action,
        width=UNLIMITED,
        height=UNLIMITED,
        census=coop_report,
        props=pa)

    return (coop_env, groups, group_indices, central_bank)


def main():
    global groups
    global group_indices
    global central_bank
    global coop_env

    (coop_env, groups, group_indices, central_bank) = set_up()

    coop_env()
    return 0


if __name__ == '__main__':
    main()
