"""
    This is financial market model re-written in indra.
"""

from math import isclose
import random

from indra.utils import get_props
from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env, UNLIMITED
from indra.display_methods import BLUE, RED

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

trend_followers = None
value_investors = None
market_maker = None


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
    price = float(market_maker["asset_price"] * DEF_NUM_ASSET)
    if agent["capital"] >= price:
        agent["capital"] -= price
        agent["num_stock"] += DEF_NUM_ASSET
        market_maker["buy"] += 1


def sell(agent):
    price = float(market_maker["asset_price"] * DEF_NUM_ASSET)
    if agent["num_stock"] >= DEF_NUM_ASSET:
        market_maker["sell"] += 1
        agent["capital"] += price
        agent["num_stock"] -= DEF_NUM_ASSET


def market_report(env):
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


def gaussian_distribution(default_target, sigma):
    new_target = random.gauss(default_target, sigma)
    if new_target < 0:
        new_target *= -1
    return new_target


def plot_asset_price(env):
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


def create_trend_follower(name, i, props=None):
    """
    Create a trend follower.
    """
    average_period = props.get("average_period", DEF_PERIODS)
    dev = props.get("deviation_follower", DEF_SIGMA)
    trend_follower = Agent(name + str(i), action=trend_follower_action)
    trend_follower["change_period"] = gaussian_distribution(average_period,
                                                            dev)
    if trend_follower["change_period"] < 0:
        trend_follower["change_period"] *= -1

    trend_follower["capital"] = DEF_CAPITAL
    trend_follower["num_stock"] = 0
    return trend_follower


def create_value_investor(name, i, props=None):
    """
    Create a value investor.
    """
    value_investor = Agent(name + str(i), action=value_investor_action)
    mean_price = props.get("discount", DEF_DISCOUNT)
    dev = props.get("deviation_investor", DEF_SIGMA)
    low_val_percentage = gaussian_distribution(mean_price, dev)
    high_val_percentage = gaussian_distribution(mean_price, dev)
    value_investor["low_price"] = DEF_REAL_VALUE * (1 - low_val_percentage)
    value_investor["high_price"] = DEF_REAL_VALUE * (1 + high_val_percentage)

    value_investor["capital"] = DEF_CAPITAL
    value_investor["num_stock"] = 0
    return value_investor


def market_maker_action(agent):
    # Determine the current price asset

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
    if trend_direction(agent, market_maker["asset_price"],
                       market_maker["price_hist"]) == 1:
        buy(agent)
    else:
        sell(agent)

    return True


def value_investor_action(agent):
    # Determine if value investors should buy or sell the stock
    if market_maker["asset_price"] >= agent["high_price"]:
        sell(agent)
    elif market_maker["asset_price"] <= agent["low_price"]:
        buy(agent)

    return True


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """

    global market_maker

    pa = get_props(MODEL_NAME, props)

    value_investors = Composite("value_investors", {"color": BLUE},
                                props=pa, member_creator=create_value_investor,
                                num_members=pa.get("value_investors",
                                                   DEF_NUM_VALUE_INVESTOR))
    trend_followers = Composite("trend_followers", {"color": RED}, props=pa,
                                member_creator=create_trend_follower,
                                num_members=pa.get("trend_followers",
                                                   DEF_NUM_TREND_FOLLOWER))
    market_maker = create_market_maker("market_maker")
    market = Env("env",
                 members=[value_investors, trend_followers, market_maker],
                 props=pa,
                 width=UNLIMITED,
                 height=UNLIMITED,
                 census=market_report,
                 line_data_func=plot_asset_price)
    market.exclude_menu_item("scatter_plot")
    return (market, value_investors, trend_followers, market_maker)


def main():
    global trend_followers
    global value_investors
    global market_maker
    global market

    (market, trend_followers, value_investors, market_maker) = set_up()

    market()
    return 0


if __name__ == "__main__":
    main()
