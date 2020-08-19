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
from indra.display_methods import RED, GREEN
from indra.env import Env, UNLIMITED
from registry.execution_registry import CLI_EXEC_KEY, \
    EXEC_KEY, get_exec_key
from registry.registry import get_env, get_group, get_prop
from registry.registry import get_env_attr, set_env_attr
from registry.registry import user_tell, run_notice, user_log_notif
from indra.utils import gaussian
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


def record_exchanges(pop_hist, **kwargs):
    """
    This is our hook into the env to record the number of exchanges each
    period.
    """
    execution_key = get_exec_key(kwargs=kwargs)
    pop_hist.record_pop("Exchanges",
                        get_env_attr("last_per_exchg",
                                     execution_key=execution_key))


def get_sitters(co_op_members):
    return co_op_members.subset(wants_to_sit)


def get_going_out(co_op_members):
    return co_op_members.subset(wants_to_go_out)


def coop_action(coop_env, **kwargs):
    execution_key = get_exec_key(kwargs=kwargs)
    sitters = get_sitters(
        get_group(CO_OP_MEMBERS, execution_key=execution_key))
    going_out = get_going_out(
        get_group(CO_OP_MEMBERS, execution_key=execution_key))

    exchanges = min(len(sitters), len(going_out))
    sitter_agents = [agent for agent in sitters]
    going_out_agents = [agent for agent in going_out]

    for i in range(exchanges):
        sitter, outer = sitter_agents[i], going_out_agents[i]
        sitters[sitter]['coupons'] += 1
        going_out[outer]['coupons'] -= 1

    set_env_attr("last_per_exchg", exchanges, execution_key=execution_key)
    set_env_attr("last_per_unemp",
                 max(len(sitters), len(going_out)) - exchanges,
                 execution_key=execution_key)
    return True


def distribute_coupons(agent, execution_key=CLI_EXEC_KEY):
    """
    Distribute coupons from central bank randomly to each babysitter.
    Coupons are gaussian distributed based on extra_coupons and extra_dev.
    """
    co_op_members = get_group(CO_OP_MEMBERS, execution_key=execution_key)
    for bbsit in co_op_members:
        co_op_members[bbsit]['coupons'] += int(gaussian(
            agent["extra_coupons"], agent["extra_dev"]))


def coop_report(coop_env, execution_key=CLI_EXEC_KEY):
    num_babysitter = len(
        get_sitters(get_group(CO_OP_MEMBERS, execution_key=execution_key)))
    return 'Number of babysitters is: ' + str(num_babysitter) + '\n'
    pass


def babysitter_action(agent, **kwargs):
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
    return True


def central_bank_action(agent, **kwargs):
    """
    If exchanges are down "enough", distribute coupons!
    Enough is a parameter.
    """
    execution_key = get_exec_key(kwargs=kwargs)
    CB_interven_pts = get_env_attr("CB_interven_pts",
                                   execution_key=execution_key)
    set_env_attr("num_rounds",
                 get_env_attr("num_rounds", execution_key=execution_key) + 1,
                 execution_key=execution_key)
    co_op_mbrs = get_group(CO_OP_MEMBERS, execution_key=execution_key)
    unemp_rate = get_env_attr("last_per_unemp", execution_key=execution_key,
                              default_value=0) / len(co_op_mbrs) * 100
    unemp_threshold = agent["percent_change"]
    if unemp_rate >= unemp_threshold:
        user_tell("Unemployment has risen to "
                  + str(unemp_rate)
                  + " more than default value "
                  + str(unemp_threshold)
                  + " CB Intervened")
        CB_interven_pts.append(
            [get_env_attr("num_rounds", execution_key=execution_key),
             get_env_attr("last_per_exchg", execution_key=execution_key)])
        distribute_coupons(agent, execution_key=execution_key)
    return True


def create_babysitter(name, i, **kwargs):
    """
    Create a babysitter.
    """
    execution_key = get_exec_key(kwargs=kwargs)
    babysitter = Agent(name + str(i), action=babysitter_action,
                       execution_key=execution_key)
    mean_coupons = get_prop("average_coupons", DEF_COUPON,
                            execution_key=execution_key)
    dev = get_prop("deviation", DEF_SIGMA, execution_key=execution_key)
    babysitter["goal"] = None
    babysitter['coupons'] = int(gaussian(mean_coupons, dev))
    babysitter['desired_cash'] = get_prop("desired_cash",
                                          DEF_DESIRED_CASH_BAL,
                                          execution_key=execution_key)
    return babysitter


def create_central_bank(name, i, **kwargs):
    """
    Create the central bank to distribute the coupons
    """
    execution_key = get_exec_key(kwargs=kwargs)
    central_bank = Agent(name, action=central_bank_action,
                         execution_key=execution_key)
    central_bank["percent_change"] = get_prop("percent_change",
                                              DEF_PERCENT,
                                              execution_key=execution_key)
    central_bank["extra_coupons"] = get_prop("extra_coupons", DEF_COUPON,
                                             execution_key=execution_key)
    central_bank["extra_dev"] = get_prop("extra_deviation", DEF_SIGMA,
                                         execution_key=execution_key)
    return central_bank


def set_env_attrs(execution_key=CLI_EXEC_KEY):
    user_log_notif("Setting env attrs for " + MODEL_NAME)
    set_env_attr("pop_hist_func", record_exchanges,
                 execution_key=execution_key)
    set_env_attr("census_func", coop_report, execution_key=execution_key)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    init_props(MODEL_NAME, props)
    execution_key = int(props[EXEC_KEY].val) \
        if props is not None else CLI_EXEC_KEY

    num_members = get_prop('num_babysitter', DEF_BABYSITTER,
                           execution_key=execution_key)
    co_op_members = Composite(CO_OP_MEMBERS,
                              {"color": RED},
                              num_members=num_members,
                              member_creator=create_babysitter,
                              execution_key=execution_key)
    central_bank = Composite("central_bank",
                             {"color": GREEN},
                             num_members=1,
                             member_creator=create_central_bank,
                             execution_key=execution_key)

    Env(MODEL_NAME, members=[co_op_members, central_bank],
        action=coop_action, width=UNLIMITED,
        height=UNLIMITED,
        pop_hist_setup=initial_exchanges,
        attrs={"last_per_exchg": 0,
               "last_per_unemp": 0,
               "num_rounds": 0,
               "CB_interven_pts": []}, execution_key=execution_key)
    set_env_attrs(execution_key=execution_key)


def main():
    set_up()
    run_notice(MODEL_NAME)
    get_env()()
    return 0


if __name__ == '__main__':
    main()
