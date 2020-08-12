"""
    This is a financial market model written in indra.
    It is intended to demonstrate how the interaction of value
    investors and trend followers can produce cyclical price
    changes.
"""

from math import isclose

from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import BLUE, RED
from indra.env import Env, UNLIMITED
from registry.execution_registry import CLI_EXEC_KEY
from registry.execution_registry import get_exec_key, init_exec_key
from registry.registry import get_env, get_prop, set_env_attr
from registry.registry import run_notice, user_log_notif
from indra.utils import gaussian
from indra.utils import init_props

MODEL_NAME = "fmarket"
DEF_NUM_TREND_FOLLOWER = 10
DEF_NUM_VALUE_INVESTOR = 10
DEF_CAPITAL = 1000
DEF_PRICE = 8  # a starting point
DEF_PERIODS = 3
DEF_NUM_ASSET = 10
DEF_MIN_PRICE_MOVE = .2
DEF_MAX_PRICE_MOVE = .4
INF = 1000000000  # just some very big num!
DEF_REAL_VALUE = 10
DEF_DISCOUNT = .002
DEF_SIGMA = .8
MARKET_MAKER = "market_maker"
ASSET_PRICE = "Asset Price"


def trend_direction(agent, cur_price, price_hist):
    """
    Calculate the trend.
    If the trend is upward,return 1
    Else return 0.
    """
    period = agent["change_period"]
    if round(len(price_hist) - period) >= 0:
        prev_price = price_hist[round(len(price_hist) - period)]
    else:
        prev_price = INF

    if cur_price > prev_price:
        return 1
    else:
        return 0


def buy(agent, **kwargs):
    exec_key = get_exec_key(kwargs=kwargs)
    market_maker = get_env(execution_key=exec_key)[MARKET_MAKER]

    price = market_maker["asset_price"] * DEF_NUM_ASSET
    if agent["capital"] >= price:
        agent["capital"] -= price
        agent["num_stock"] += DEF_NUM_ASSET
        market_maker["buy"] += 1


def sell(agent, **kwargs):
    execution_key = get_exec_key(kwargs=kwargs)
    market_maker = get_env(execution_key=execution_key)[MARKET_MAKER]

    price = market_maker["asset_price"] * DEF_NUM_ASSET
    if agent["num_stock"] >= DEF_NUM_ASSET:
        market_maker["sell"] += 1
        agent["capital"] += price
        agent["num_stock"] -= DEF_NUM_ASSET


def market_report(env, execution_key=CLI_EXEC_KEY):
    market_maker = get_env(execution_key=execution_key)[MARKET_MAKER]
    return "Asset price on the market: " \
           + str(round(market_maker["asset_price"], 4)) + "\n"


def calc_price_change(ratio, min_price_move=DEF_MIN_PRICE_MOVE,
                      max_price_move=DEF_MAX_PRICE_MOVE):
    """
    Make the price move in proportion to the ratio, up to a ceiling
    of max_price_move.
    """
    direction = 1
    if isclose(ratio, 1.0):
        return 0

    if ratio < 1:
        if ratio == 0:
            ratio = INF
        else:
            ratio = 1 / ratio
        direction = -1

    return direction * min(max_price_move, min_price_move * ratio)


def create_market_maker(name, **kwargs):
    """
    Create a market maker.
    """
    execution_key = get_exec_key(kwargs=kwargs)
    market_maker = Agent(name, action=market_maker_action,
                         execution_key=execution_key)
    market_maker["buy"] = 0
    market_maker["sell"] = 0
    market_maker["asset_price"] = DEF_PRICE
    market_maker["prev_asset_price"] = DEF_PRICE
    market_maker["price_hist"] = [DEF_PRICE]
    return market_maker


def create_trend_follower(name, i, **kwargs):
    """
    Create a trend follower.
    """
    execution_key = get_exec_key(kwargs=kwargs)
    average_period = get_prop("average_period", DEF_PERIODS,
                              execution_key=execution_key)
    dev = get_prop("deviation_follower", DEF_SIGMA,
                   execution_key=execution_key)
    trend_follower = Agent(name + str(i),
                           action=trend_follower_action,
                           execution_key=execution_key)
    trend_follower["change_period"] = gaussian(average_period, dev)

    trend_follower["capital"] = DEF_CAPITAL
    trend_follower["num_stock"] = 0
    return trend_follower


def create_value_investor(name, i, **kwargs):
    """
    Create a value investor.
    """
    execution_key = get_exec_key(kwargs=kwargs)
    value_investor = Agent(name + str(i), action=value_investor_action,
                           execution_key=execution_key)
    mean_price = get_prop("discount", DEF_DISCOUNT,
                          execution_key=execution_key)
    dev = get_prop("deviation_investor", DEF_SIGMA,
                   execution_key=execution_key)
    low_val_percentage = gaussian(mean_price, dev)
    high_val_percentage = gaussian(mean_price, dev)
    value_investor["low_price"] = DEF_REAL_VALUE * (1 - low_val_percentage)
    value_investor["high_price"] = DEF_REAL_VALUE * (1 + high_val_percentage)

    value_investor["capital"] = DEF_CAPITAL
    value_investor["num_stock"] = 0
    return value_investor


def market_maker_action(agent, **kwargs):
    # Determine the current price asset
    execution_key = get_exec_key(kwargs=kwargs)
    market_maker = get_env(execution_key=execution_key)[MARKET_MAKER]

    market_maker["prev_asset_price"] = market_maker["asset_price"]
    ratio = 1
    if agent["sell"] == 0:
        if agent["buy"] != 0:
            ratio = INF
    else:
        ratio = agent["buy"] / agent["sell"]

    agent["asset_price"] += calc_price_change(ratio)

    agent["price_hist"].append(round(agent["asset_price"], 4))
    agent["buy"] = 0
    agent["sell"] = 0

    return True


def trend_follower_action(agent, **kwargs):
    # Determine if trend followers should buy
    # or sell the stock
    execution_key = get_exec_key(kwargs=kwargs)
    market_maker = get_env(execution_key=execution_key)[MARKET_MAKER]

    if trend_direction(agent, market_maker["asset_price"],
                       market_maker["price_hist"]) == 1:
        buy(agent, **kwargs)
    else:
        sell(agent, **kwargs)

    return True


def value_investor_action(agent, **kwargs):
    # Determine if value investors should buy or sell the stock
    execution_key = get_exec_key(kwargs=kwargs)
    market_maker = get_env(execution_key=execution_key)[MARKET_MAKER]

    if market_maker["asset_price"] >= agent["high_price"]:
        sell(agent, **kwargs)
    elif market_maker["asset_price"] <= agent["low_price"]:
        buy(agent, **kwargs)

    return True


def initial_price(pop_hist):
    """
    Set up our pop hist object to record exchanges per period.
    """
    pop_hist.record_pop(ASSET_PRICE, DEF_PRICE)


def record_price(pop_hist, execution_key=CLI_EXEC_KEY):
    """
    This is our hook into the env to record the number of exchanges each
    period.
    """
    market_maker = get_env(execution_key=execution_key)[MARKET_MAKER]
    pop_hist.record_pop(ASSET_PRICE, market_maker["asset_price"])


def set_env_attrs(execution_key=CLI_EXEC_KEY):
    user_log_notif("Setting env attrs for " + MODEL_NAME)
    set_env_attr("pop_hist_func", record_price, execution_key=execution_key)
    set_env_attr("census_func", market_report, execution_key=execution_key)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    init_props(MODEL_NAME, props)
    exec_key = init_exec_key(props)
    groups = []

    groups.append(Composite("value_investors", {"color": BLUE},
                            member_creator=create_value_investor,
                            num_members=get_prop("value_investors",
                                                 DEF_NUM_VALUE_INVESTOR,
                                                 execution_key=exec_key),
                            execution_key=exec_key)
                  )
    groups.append(Composite("trend_followers", {"color": RED},
                            member_creator=create_trend_follower,
                            num_members=get_prop("trend_followers",
                                                 DEF_NUM_TREND_FOLLOWER,
                                                 execution_key=exec_key),
                            execution_key=exec_key),
                  )
    groups.append(create_market_maker(MARKET_MAKER))
    Env(MODEL_NAME,
        members=groups,
        width=UNLIMITED,
        height=UNLIMITED,
        pop_hist_setup=initial_price,
        execution_key=exec_key)
    get_env(execution_key=exec_key).exclude_menu_item("scatter_plot")
    set_env_attrs(execution_key=exec_key)


def main():
    set_up()
    run_notice(MODEL_NAME)
    get_env()()
    return 0


if __name__ == "__main__":
    main()
