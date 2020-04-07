"""
This is the test suite for trade.py.
"""

from unittest import TestCase, main

import capital.trade_utils as tu
import capital.complementary as cp
from capital.complementary import COMPLEMENTS

from capital.trade_utils import AMT_AVAILABLE, seek_a_trade
from capital.trade_utils import gen_util_func, trade, DEF_MAX_UTIL
from capital.trade_utils import rec_offer, utility_delta, adj_add_good


class tradeTestCase(TestCase):
    def setUp(self, props=None):
        self.goodA = {AMT_AVAILABLE: 10, COMPLEMENTS: "b"}
        self.goodB = {AMT_AVAILABLE: 10}
        self.trader = {"goods": {"a": self.goodA, "b": self.goodB}}
        self.goods = {"a": self.goodA, "b": self.goodB}

    def tearDown(self):
        self.goodA = None
        self.goodB = None
        self.trader = None
        self.goods = None
        
    def test_create_trader(self):
        trader = cp.create_trader("trader", 0)
        name = trader.name
        incr = trader["goods"]["truck"]["incr"]
        self.assertEqual(incr, 0)


    if __name__ == '__main__':
        main()
