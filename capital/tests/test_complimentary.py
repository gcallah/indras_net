"""
This is the test suite for trade.py.
"""

from unittest import TestCase, main

import capital.trade as td
import capital.trade_utils as tu
# from capital.trade_utils import 

from capital.trade_utils import AMT_AVAILABLE, seek_a_trade
from capital.trade_utils import gen_util_func, trade, DEF_MAX_UTIL
from capital.trade_utils import rec_offer, utility_delta, adj_add_good


class tradeTestCase(TestCase):
    def setUp(self, props=None):
        # self.goodA = {AMT_AVAILABLE: 10}
        # self.goodB = {AMT_AVAILABLE: 10}
        # self.trader = {"goods": {}}
        # self.goods = {"a": self.goodA, "b": self.goodB}
        pass

    def tearDown(self):
        # self.goodA = None
        # self.goodB = None
        # self.trader = None
        # self.goods = None
        pass

    def test_create_trader(self):
        # agent = td.create_trader('trader', 0)
        # name = agent.name
        # pamt = agent["goods"]["penguin"][AMT_AVAILABLE]
        # camt = agent["goods"]["cat"][AMT_AVAILABLE]
        # bamt = agent["goods"]["bear"][AMT_AVAILABLE]
        # pfamt = agent["goods"]["pet food"][AMT_AVAILABLE]
        # self.assertEqual(name, "trader0")
        # self.assertEqual(camt, 0)
        # self.assertEqual(pamt, 0)
        # self.assertEqual(bamt, 0)
        # self.assertEqual(pfamt, 0)
        pass

    if __name__ == '__main__':
        main()
