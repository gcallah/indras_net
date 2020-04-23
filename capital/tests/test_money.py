"""
This is the test suite for trade.py.
"""
import copy
from unittest import TestCase, main
# from indra.agent import Agent
from capital.trade_utils import endow, get_rand_good, is_depleted, AMT_AVAILABLE, transfer
from capital.trade_utils import rand_dist, equal_dist, GOODS
import capital.money as mn
import capital.trade_utils as tu

class MoneyTestCase(TestCase):
    def setUp(self, props=None):
        self.goodA = {AMT_AVAILABLE: 10, "durability":0.6}
        self.goodB = {AMT_AVAILABLE: 8, "durability":0.9}
        self.trader = {}
        self.goods = {"a": self.goodA, "b": self.goodB}
        self.goods_dict_empty = {}

    def tearDown(self):
        self.goodA = None
        self.goodB = None
        self.trader = None
        self.goods = None

    def test_main(self):
        self.assertEqual(mn.main(), 0)

    def test_create_trader(self):
        self.trader[0] = mn.create_trader('Trader', 0)
        self.assertEqual(self.trader[0].name, "Trader0")
        self.assertEqual(self.trader[0][GOODS], {})
        self.assertEqual(self.trader[0]["util"], 0)

    def test_nature_to_traders(self):
        self.trader[0] = mn.create_trader('Trader', 0)
        self.trader[1] = mn.create_trader('Trader', 1)
        mn.nature_to_traders(self.trader, self.goods)
        self.assertNotEqual(self.trader[0]["goods"], {})
        self.assertNotEqual(self.trader[1]["goods"], {})

    
    if __name__ == '__main__':
        main()
