"""
    This is financial market model re-written in indra.
"""

from math import isclose
import random
from propargs.propargs import PropArgs

from indra.utils import get_prop_path
from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env
from indra.display_methods import BLUE, RED

MODEL_NAME = "fmarket"
DEBUG = False  # turns deeper debugging code on or off
DEF_NUM_TREND_FOLLOWER = 10
DEF_NUM_VALUE_INVESTOR = 10
DEF_CAPITAL = 1000
DEF_PRICE = 8  # a starting point
DEF_MOVING_PERIODS = 3
DEF_STAGNANT_PERIODS = 8
DEF_NUM_ASSET = 10
DEF_MIN_PRICE_MOVE = .2
DEF_MAX_PRICE_MOVE = .4
INF_RATIO = 1000000000  # just some very big num!
DEF_REAL_VALUE = 10
DEF_PRICE_TARGET = .002
DEF_SIGMA = .8

trend_followers = None
value_investors = None
market_maker = None


def trend_direction(agent):
    """
    Calculate the trend.
    If the price is increasing,return True
    Else return false.
    """

    if agent["asset_price"] > agent["prev_asset_price"]:
        return 1
    elif agent["asset_price"] < agent["prev_asset_price"]:
        return -1
    else:
        return 0


def buy(agent):
    price = float(market_maker["asset_price"] * DEF_NUM_ASSET)
    print("This is", agent.name, " buying with", agent["capital"],
          "and the current asset price is", price)
    if agent["capital"] >= price:
        agent["capital"] -= price
        agent["num_stock"] += DEF_NUM_ASSET
        market_maker["buy"] += 1


def sell(agent):
    price = float(market_maker["asset_price"] * DEF_NUM_ASSET)
    print("This is", agent.name, " selling with", agent["num_stock"],
          agent["capital"], "and the current asset price is", price)
    if agent["num_stock"] >= DEF_NUM_ASSET:
        market_maker["sell"] += 1
        agent["capital"] += price
        agent["num_stock"] -= DEF_NUM_ASSET
    print("This is", agent.name, " with ", agent["capital"], "after selling")


def num_increasing_period(agent):
    if trend_direction(agent) == 1:
        agent["num_period"] += 1
    elif trend_direction(agent) == -1:
        agent["num_period"] = 0
    else:
        if agent["num_period"] <= -1:
            agent["num_period"] -= 1
        else:
            agent["num_period"] = -1


def market_report(env):
    return "Asset price on the market: " \
        + str(market_maker["asset_price"]) + "\n"


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
            ratio = INF_RATIO
        else:
            ratio = 1 / ratio
        direction = -1

    return direction * min(max_price_move, min_price_move * ratio)


def get_price_target(default_price_target, sigma):
    price1 = random.gauss(default_price_target, sigma)
    price2 = random.gauss(default_price_target, sigma)

    if price1 < 0:
        price1 *= -1

    if price2 < 0:
        price2 *= -1

    low_price = 0
    high_price = 0

    low_price = DEF_REAL_VALUE * (1 - price1)
    high_price = DEF_REAL_VALUE * (1 + price2)

    return (low_price, high_price)


def create_market_maker(name):
    """
    Create a market maker.
    """

    market_maker = Agent(name, action=market_maker_action)
    market_maker["buy"] = 0
    market_maker["sell"] = 0
    market_maker["asset_price"] = DEF_PRICE
    market_maker["prev_asset_price"] = DEF_PRICE
    market_maker["num_period"] = 0
    market_maker["price_hist"] = [DEF_PRICE]
    return market_maker


def create_trend_follower(name, i):
    """
    Create a trend follower.
    """

    trend_follower = Agent(name + str(i), action=trend_follower_action)
    trend_follower["capital"] = DEF_CAPITAL
    trend_follower["num_stock"] = 0
    return trend_follower


def create_value_investor(name, i, mean_price, dev):
    """
    Create a value investor.
    """
    value_investor = Agent(name + str(i), action=value_investor_action)
    (low_price, high_price) = get_price_target(mean_price, dev)
    value_investor["low_price"] = low_price
    value_investor["high_price"] = high_price
    value_investor["capital"] = DEF_CAPITAL
    value_investor["num_stock"] = 0
    return value_investor


def market_maker_action(agent):
    # Determine the current price asset

    market_maker["prev_asset_price"] = market_maker["asset_price"]
    ratio = 1
    if agent["sell"] == 0:
        if agent["buy"] != 0:
            ratio = INF_RATIO
        else:
            if agent["num_period"] == DEF_STAGNANT_PERIODS * -1:
                ratio = DEF_MIN_PRICE_MOVE
    else:
        ratio = agent["buy"] / agent["sell"]

    agent["asset_price"] += calc_price_change(ratio)

    num_increasing_period(agent)
    agent["price_hist"].append(round(agent["asset_price"], 4))
    print("This is price hist:", agent["price_hist"])
    print("buy", agent["buy"])
    print("sell", agent["sell"])
    agent["buy"] = 0
    agent["sell"] = 0

    return True


def trend_follower_action(agent):
    # Determine if trend followers should buy or sell the stock

    if trend_direction(market_maker) == 1:
        if market_maker["num_period"] >= DEF_MOVING_PERIODS:
            agent["buy"] = True
            agent["sell"] = False
            buy(agent)
    elif trend_direction(market_maker) == -1:
        if market_maker["num_period"] == 0:
            agent["buy"] = False
            agent["sell"] = True
            sell(agent)
    else:
        if market_maker["num_period"] == DEF_STAGNANT_PERIODS * -1:
            agent["buy"] = False
            agent["sell"] = True
            sell(agent)

    return True


def value_investor_action(agent):
    # Determine if value investors should buy or sell the stock
    print("This is the high_price", agent["high_price"])
    print("This is the low_price", agent["low_price"])
    if market_maker["asset_price"] >= agent["high_price"]:
        print("value investor starts selling")
        agent["sell"] = True
        agent["buy"] = False
        sell(agent)
    elif market_maker["asset_price"] <= agent["low_price"]:
        print("value investor starts buying")
        agent["sell"] = False
        agent["buy"] = True
        buy(agent)

    return True


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """

    global market_maker
    ds_file = get_prop_path(MODEL_NAME)
    if props is None:
        pa = PropArgs.create_props(MODEL_NAME, ds_file=ds_file)
    else:
        pa = PropArgs.create_props(MODEL_NAME, prop_dict=props)

    value_investors = Composite("value_investors", {"color": BLUE})
    trend_followers = Composite("trend_followers", {"color": RED},
                                member_creator=create_trend_follower,
                                num_members=pa.get("trend_followers",
                                DEF_NUM_TREND_FOLLOWER))
    for i in range(pa.get("value_investors", DEF_NUM_VALUE_INVESTOR)):
        value_investors += create_value_investor("value_investors", i,
                                                 pa.get("mean_price",
                                                        DEF_PRICE_TARGET),
                                                 pa.get("deviation", DEF_SIGMA)
                                                 )
    market_maker = create_market_maker("market_maker")
    market = Env("env",
                 members=[value_investors, trend_followers, market_maker],
                 props=pa,
                 census=market_report)
    market.user.exclude_choices(["scatter_plot", "line_graph"])
    return (market, value_investors, trend_followers, market_maker)


def main():
    global trend_followers
    global value_investors
    global market_maker
    global market

    (market, trend_followers, value_investors, market_maker) = set_up()

    if DEBUG:
        print(market.__repr__())

    market()
    return 0


if __name__ == "__main__":
    main()
