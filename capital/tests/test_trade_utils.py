"""
This is the test suite for trade.py.
"""

from unittest import TestCase, main

# from indra.agent import Agent

from capital.trade_utils import endow, get_rand_good, is_depleted, AMT_AVAILABLE, transfer
import capital.trade_utils as tu

class TradeUtilsTestCase(TestCase):
    def setUp(self, props=None):
        self.goodA = {AMT_AVAILABLE: 10}
        self.goodB = {AMT_AVAILABLE: 10}
        self.trader = {"goods": {}}
        # self.agent = Agent()
        self.goods = {"a": self.goodA, "b": self.goodB}
        self.goods_dict_empty = {}

    def tearDown(self):
        self.goodA = None
        self.goodB = None
        self.trader = None
        self.goods = None

    def test_gen_util_func(self):
        util = tu.gen_util_func(0)
        self.assertEqual(util, tu.DEF_MAX_UTIL)

    def test_endow(self):
        """
        See capital.trade_utils for description of what a
        `trader` and `goods` must look like.
        """
        endow(self.trader, self.goods)
        self.assertFalse(is_depleted(self.trader["goods"]))

    def test_is_depleted(self):
        goodA = {AMT_AVAILABLE: 0}
        goodB = {AMT_AVAILABLE: 0}
        goods_dict_zeros = {"a": goodA, "b": goodB}
        self.assertTrue(is_depleted(self.goods_dict_empty))
        self.assertTrue(is_depleted(goods_dict_zeros))

    def test_get_rand_good(self):
        """
        Test getting random good from goods dict.
        """
        self.assertIsNone(get_rand_good(self.goods_dict_empty))
        self.assertIsNotNone(get_rand_good(self.goods))

    def test_transfer(self):
        transfer(self.trader["goods"], self.goods, "a")
        self.assertEqual(self.goods["a"][AMT_AVAILABLE], 0)
        self.assertEqual(self.trader["goods"]["a"][AMT_AVAILABLE], 10)

    if __name__ == '__main__':
        main()
