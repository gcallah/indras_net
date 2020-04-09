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
from indra.registry import get_env, get_prop
from indra.utils import gaussian  # , get_func_name
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


def buy(agent):
    market_maker = get_env()[MARKET_MAKER]

    price = market_maker["asset_price"] * DEF_NUM_ASSET
    if agent["capital"] >= price:
        agent["capital"] -= price
        agent["num_stock"] += DEF_NUM_ASSET
        market_maker["buy"] += 1


def sell(agent):
    market_maker = get_env()[MARKET_MAKER]

    price = market_maker["asset_price"] * DEF_NUM_ASSET
    if agent["num_stock"] >= DEF_NUM_ASSET:
        market_maker["sell"] += 1
        agent["capital"] += price
        agent["num_stock"] -= DEF_NUM_ASSET


def market_report(env):
    market_maker = get_env()[MARKET_MAKER]
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


def plot_asset_price(env):
    market_maker = get_env()[MARKET_MAKER]

    data = {}
    data_hist = market_maker["price_hist"]
    data["asset_price"] = {}
    data["asset_price"]["data"] = data_hist
    data["asset_price"]["color"] = RED
    period = len(data_hist)
    return (period, data)


def create_market_maker(name):
    """
    Create a market maker.
    """
    market_maker = Agent(name, action=market_maker_action)
    market_maker["buy"] = 0
    market_maker["sell"] = 0
    market_maker["asset_price"] = DEF_PRICE
    market_maker["prev_asset_price"] = DEF_PRICE
    market_maker["price_hist"] = [DEF_PRICE]
    return market_maker


def create_trend_follower(name, i):
    """
    Create a trend follower.
    """
    average_period = get_prop("average_period", DEF_PERIODS)
    dev = get_prop("deviation_follower", DEF_SIGMA)
    trend_follower = Agent(name + str(i),
                           action=trend_follower_action)
    trend_follower["change_period"] = gaussian(average_period, dev)

    trend_follower["capital"] = DEF_CAPITAL
    trend_follower["num_stock"] = 0
    return trend_follower


def create_value_investor(name, i):
    """
    Create a value investor.
    """
    value_investor = Agent(name + str(i), action=value_investor_action)
    mean_price = get_prop("discount", DEF_DISCOUNT)
    dev = get_prop("deviation_investor", DEF_SIGMA)
    low_val_percentage = gaussian(mean_price, dev)
    high_val_percentage = gaussian(mean_price, dev)
    value_investor["low_price"] = DEF_REAL_VALUE * (1 - low_val_percentage)
    value_investor["high_price"] = DEF_REAL_VALUE * (1 + high_val_percentage)

    value_investor["capital"] = DEF_CAPITAL
    value_investor["num_stock"] = 0
    return value_investor


def market_maker_action(agent):
    # Determine the current price asset
    market_maker = get_env()[MARKET_MAKER]

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


def trend_follower_action(agent):
    # Determine if trend followers should buy
    # or sell the stock
    market_maker = get_env()[MARKET_MAKER]

    if trend_direction(agent, market_maker["asset_price"],
                       market_maker["price_hist"]) == 1:
        buy(agent)
    else:
        sell(agent)

    return True


def value_investor_action(agent):
    # Determine if value investors should buy or sell the stock
    market_maker = get_env()[MARKET_MAKER]

    if market_maker["asset_price"] >= agent["high_price"]:
        sell(agent)
    elif market_maker["asset_price"] <= agent["low_price"]:
        buy(agent)

    return True


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    init_props(MODEL_NAME, props)
    groups = []

    groups.append(Composite("value_investors", {"color": BLUE},
                            member_creator=create_value_investor,
                            num_members=get_prop("value_investors",
                                                 DEF_NUM_VALUE_INVESTOR)))
    groups.append(Composite("trend_followers", {"color": RED},
                            member_creator=create_trend_follower,
                            num_members=get_prop("trend_followers",
                                                 DEF_NUM_TREND_FOLLOWER)))
    groups.append(create_market_maker(MARKET_MAKER))
    Env("fmarket",
        members=groups,
        width=UNLIMITED,
        height=UNLIMITED,
        line_data_func=plot_asset_price)
    # we need to put this back in, but that involves
    # re-doing the whole function registry
    #    census=get_func_name(market_report),
    get_env().exclude_menu_item("scatter_plot")


def main():
    set_up()
    get_env()()
    return 0


if __name__ == "__main__":
    main()
