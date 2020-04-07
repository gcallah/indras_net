"""
This is the test suite for trade.py.
"""

from unittest import TestCase, main

import capital.complementary as cp
import capital.trade_utils as tu
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


    if __name__ == '__main__':
        main()
