"""
    This is financial market model re-written in indra.
"""
from propargs.propargs import PropArgs
from indra.utils import get_prop_path
from indra.agent import Agent
from indra.composite import Composite
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.env import Env
from indra.display_methods import BLUE, RED

MODEL_NAME = "fmarket"
DEBUG = False  # turns deeper debugging code on or off
DEF_NUM_TREND_FOLLOWER = 10
DEF_NUM_VALUE_INVESTOR = 10
DEF_CAPITAL = 1000
DEF_REAL_VALUE = 10
DEF_PRICE = 8  # a starting point
DEF_PERIOD = 3
DEF_NUM_ASSET = 100

trend_followers = None
value_investors = None
market_maker = None


def trend_direction(agent):
    """
    Calculate the trend.
    If the price is increasing,return True
    Else return false.
    """
    if agent["price_asset"] > agent["prev_price_asset"]:
        return True
    else:
        return False


def buy(agent):
    price = float(market_maker["price_asset"] * DEF_NUM_ASSET)
    if agent["capital"] >= price:
        agent["capital"] -= price
        agent["num_stock"] += DEF_NUM_ASSET
        market_maker["buy"] += 1


def sell(agent):
    price = float(market_maker["price_asset"] * DEF_NUM_ASSET)
    if agent["num_stock"] >= DEF_NUM_ASSET:
        market_maker["sell"] += 1
        agent["capital"] += price
        agent["num_stock"] -= DEF_NUM_ASSET


def num_increasing_period(agent):
    if trend_direction(agent):
        agent["num_period"] += 1
    else:
        agent["num_period"] = 0


def market_report(env):
    return ("Asset price on the market: "
            + str(market_maker["price_asset"]) + "\n")


def calculate_low_price(agent):
    """
    If the stock_price is 10% equal or below
    the real value: value_investors start buying, return True.
    Else return False
    """
    if agent["price_asset"] <= float(DEF_REAL_VALUE * 0.9):
        return True
    else:
        return False


def calculate_high_price(agent):
    """
    If the stock_price is 10% equal or above
    the real value: value_investors start buying, return True.
    Else return False
    """
    if agent["price_asset"] >= float(DEF_REAL_VALUE * 1.1):
        return True
    else:
        return False


# ======================================================================================================
# ======================================================================================================
# ======================================================================================================
def create_market_maker(name):
    """
    Create a market maker.
    """
    market_maker = Agent(name, action=market_maker_action)
    market_maker["buy"] = 0
    market_maker["sell"] = 0
    market_maker["price_asset"] = DEF_PRICE
    market_maker["prev_price_asset"] = DEF_PRICE
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


def create_value_investor(name, i):
    """
    Create a value investor.
    """
    value_investor = Agent(name + str(i), action=value_investor_action)
    value_investor["num_stock"] = 0
    return value_investor


# ======================================================================================================
# ======================================================================================================
# ======================================================================================================
def market_maker_action(agent):
    print("I'm" + agent.name + "and I'm manipulating the market.")

    # Determine the current price asset
    market_maker["prev_price_asset"] = market_maker["price_asset"]
    print("This is the buy: ", agent["buy"])
    print("This is the sell: ", agent["sell"])
    if agent["sell"] == 0:
        if agent["buy"] != 0:
            agent["price_asset"] = float(agent["price_asset"] * 1.01)
            print("This is the ratio: ", 0)
        else:
            agent["price_asset"] = float(agent["price_asset"] * 0.99)
    else:
        ratio = float(agent["buy"] / agent["sell"])
        print("This is the ratio: ", ratio)
        if ratio >= 1:
            agent["price_asset"] = float(agent["price_asset"] * 1.01)
        else:
            agent["price_asset"] = float(agent["price_asset"] * 0.99)

    num_increasing_period(agent)
    agent["price_hist"].append(agent["price_asset"])
    print("This is price hist:", agent["price_hist"])
    agent["buy"] = 0
    agent["sell"] = 0

    return False


def trend_follower_action(agent):
    print("I'm " + agent.name + " and I'm following the trend.")
    agent["capital"] = DEF_CAPITAL

    # Determine if trend followers should buy or sell the stock
    if market_maker["num_period"] >= DEF_PERIOD:
        agent["buy"] = True
        agent["sell"] = False
        buy(agent)
    elif (market_maker["num_period"] == 0
          and trend_direction(market_maker) is False
          and agent["capital"] < DEF_CAPITAL):
        agent["buy"] = False
        agent["sell"] = True
        sell(agent)

    return False


def value_investor_action(agent):
    print("I'm " + agent.name + " and I'm investing.")
    agent["capital"] = DEF_CAPITAL

    # Determine if value investors should buy or sell the stock
    low_price = calculate_low_price(market_maker)
    high_price = calculate_high_price(market_maker)

    if low_price:
        agent["buy"] = True
        agent["sell"] = False
        buy(agent)
    else:
        if high_price:
            agent["buy"] = False
            agent["sell"] = True
            sell(agent)
        else:
            agent["buy"] = False
            agent["sell"] = False
    return False


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    global market_maker
    ds_file = get_prop_path(MODEL_NAME)
    if props is None:
        pa = PropArgs.create_props(MODEL_NAME,
                                   ds_file=ds_file)
    else:
        pa = PropArgs.create_props(MODEL_NAME,
                                   prop_dict=props)

    value_investors = Composite("value_investors", {"color": BLUE},
                                member_creator=create_value_investor,
                                num_members=pa.get('value_investors',
                                                   DEF_NUM_VALUE_INVESTOR))
    trend_followers = Composite("trend_followers", {"color": RED},
                                member_creator=create_trend_follower,
                                num_members=pa.get('trend_followers',
                                                   DEF_NUM_TREND_FOLLOWER))
    market_maker = create_market_maker("market_maker")
    market = Env("env",
                 height=pa.get('grid_height', DEF_HEIGHT),
                 width=pa.get('grid_width', DEF_WIDTH),
                 members=[value_investors, trend_followers, market_maker],
                 props=pa, census=market_report)
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
