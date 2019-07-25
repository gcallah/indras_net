"""
This is the test suite for space.py.
"""

from propargs.propargs import PropArgs
from unittest import TestCase, main
from indra.env import Env
from indra.composite import Composite
from models.fmarket import set_up, create_market_maker, create_trend_follower, create_value_investor, DEF_PRICE, trend_direction, trend_follower_action, calculate_low_price, calculate_high_price, DEF_REAL_VALUE, value_investor_action, DEF_MIN_PRICE_MOVE, DEF_MAX_PRICE_MOVE, market_maker_action, calc_price_change, num_increasing_period, buy, sell, DEF_NUM_ASSET, market_report, DEF_WIDTH, DEF_HEIGHT
import models.fmarket as fm

TEST_INVESTOR_NUM = 3
TEST_FOLLOWER_NUM = 3

class FMarketTestCase(TestCase):
    def setUp(self):
        self.pa = PropArgs.create_props('fmarket_props',
                                        ds_file='props/fmarket.props.json')
        (fm.market,fm.value_investors, fm.trend_followers, fm.market_maker) = set_up()
        self.value_investor = create_value_investor("value_investors", TEST_INVESTOR_NUM)
        self.trend_follower = create_trend_follower("trend_followers", TEST_FOLLOWER_NUM)
        self.market_maker = create_market_maker("market_maker")

    def tearDown(self):
        self.test_value_investors = None
        self.test_trend_followers = None
        self.test_market_maker = None

    def test_create_trend_follower(self):
        """
         Test to see if trend_follower is created
        """
        new_trend_follower = create_trend_follower("trend_followers", 0)
        self.assertTrue(new_trend_follower["capital"] >= 0)
        self.assertTrue(new_trend_follower["num_stock"] == 0)

    def test_create_value_investor(self):
        """
         Test to see if value_investor is created
        """
        new_value_investor = create_value_investor("value_investors", 0)
        self.assertTrue(new_value_investor["capital"] >= 0)
        self.assertTrue(new_value_investor["num_stock"] == 0)

    def test_create_market_maker(self):
        """
        Test to see if market_maker is created
        """
        new_market_maker = create_market_maker("market_maker")
        self.assertTrue(new_market_maker["buy"] == 0)
        self.assertTrue(new_market_maker["sell"] == 0)
        self.assertTrue(new_market_maker["num_period"] == 0)
        self.assertTrue(new_market_maker["asset_price"] == DEF_PRICE)
        self.assertTrue(new_market_maker["prev_asset_price"] == DEF_PRICE)
        self.assertTrue(new_market_maker["price_hist"] == [DEF_PRICE])

    def test_buy(self):
        new_market_maker = create_market_maker("market_maker")
        new_value_investor = create_value_investor("value_investor", 0)
        new_market_maker["asset_price"] = DEF_PRICE
        new_value_investor["capital"] = DEF_PRICE * DEF_NUM_ASSET + 1
        price = new_market_maker["asset_price"] * DEF_NUM_ASSET
        buy(new_value_investor)
        self.assertTrue(new_value_investor["capital"] == 1)

    def test_sell(self):
        new_market_maker = create_market_maker("market_maker")
        new_value_investor = create_value_investor("value_investor", 0)
        new_market_maker["asset_price"] = DEF_PRICE
        new_value_investor["capital"] = 0
        new_value_investor["num_stock"] = DEF_NUM_ASSET + 1
        price = new_market_maker["asset_price"] * DEF_NUM_ASSET
        sell(new_value_investor)
        self.assertTrue(new_value_investor["capital"] == price)

    def test_calculate_low_price(self):
        new_market_maker = create_market_maker("market_maker")
        new_market_maker["asset_price"] = DEF_REAL_VALUE * 0.9 - 1
        self.assertTrue(calculate_low_price(new_market_maker))

    def test_calculate_high_price(self):
        new_market_maker = create_market_maker("market_maker")
        new_market_maker["asset_price"] = DEF_REAL_VALUE * 1.1 + 1
        self.assertTrue(calculate_high_price(new_market_maker))

    def test_calc_price_change(self):
        new_market_maker = create_market_maker("market_maker")
        new_market_maker["sell"] = 2
        new_market_maker["buy"]  = 4
        ratio = new_market_maker["buy"] / new_market_maker["sell"]
        self.assertTrue(calc_price_change(ratio) > 0)

    def test_market_report(self):
        self.pa = PropArgs.create_props('fmarket_props',
                                        ds_file='props/fmarket.props.json')
        new_market_maker = create_market_maker("market_maker")
        value_investors = Composite("value_investors")
        trend_followers = Composite("trend_followers")
        market = Env("env",                  
                     height=self.pa.get("grid_height", DEF_HEIGHT),
                     width=self.pa.get("grid_width", DEF_WIDTH),
                     members=[value_investors, trend_followers, new_market_maker],
                     props=self.pa,
                     census=market_report)
        self.assertEqual(market_report(market), "Asset price on the market: " \
        + str(DEF_PRICE) + "\n")

    def test_trend_follower_action(self):
        new_market_maker = create_market_maker("market_maker")
        new_trend_follower = create_trend_follower("trend_follower", 0)
        trend_follower_action(new_trend_follower)
        trend = trend_direction(new_market_maker)
        self.assertEqual(trend, "stagnant")

    def test_value_investor_action(self):
        new_market_maker = create_market_maker("market_maker")
        new_market_maker["asset_price"] = DEF_REAL_VALUE * 0.8
        new_value_investor = create_value_investor("value_investor", 0)
        value_investor_action(new_value_investor)
        print(new_value_investor["buy"], new_value_investor["sell"])
        self.assertEqual(new_value_investor["buy"], True)
        self.assertEqual(new_value_investor["sell"], False)

    def test_market_maker_action(self):
        new_market_maker = create_market_maker("market_maker")
        new_market_maker["sell"] = 2
        new_market_maker["buy"]  = 4
        ratio = new_market_maker["buy"] / new_market_maker["sell"]
        new_market_maker["asset_price"] = DEF_REAL_VALUE
        market_maker_action(new_market_maker)
        price_change = calc_price_change(ratio)
        self.assertTrue(new_market_maker["asset_price"] == DEF_REAL_VALUE + price_change)

    def test_trend_direction(self):
        new_market_maker = create_market_maker("market_maker")
        new_market_maker["asset_price"] = DEF_REAL_VALUE
        new_market_maker["prev_asset_price"] = DEF_REAL_VALUE * 1.1
        self.assertEqual(trend_direction(new_market_maker), "down")

    def test_num_increasing_period(self):
        new_market_maker = create_market_maker("market_maker")
        new_market_maker["asset_price"] = DEF_REAL_VALUE
        new_market_maker["prev_asset_price"] = DEF_REAL_VALUE * 1.1
        num_increasing_period(new_market_maker)
        self.assertTrue(new_market_maker["num_period"] == 0)



    if __name__ == '__main__':
        main()
