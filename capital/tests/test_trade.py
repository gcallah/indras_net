"""
This is the test suite for trade.py.
"""

from unittest import TestCase, main

import capital.trade as td
import capital.trade_utils as tu
# from capital.trade_utils import 

from capital.trade_utils import AMT_AVAIL, seek_a_trade
from capital.trade_utils import gen_util_func, trade, DEF_MAX_UTIL
from capital.trade_utils import utility_delta, adj_add_good


class tradeTestCase(TestCase):
    def setUp(self, props=None):
        self.goodA = {AMT_AVAIL: 10}
        self.goodB = {AMT_AVAIL: 10}
        self.trader = {"goods": {}}
        self.goods = {"a": self.goodA, "b": self.goodB}

    def tearDown(self):
        self.goodA = None
        self.goodB = None
        self.trader = None
        self.goods = None

    def test_random_generate_resources(self):
        td.allocate_resources(self.trader, self.goods)
        self.assertFalse(tu.is_depleted(self.trader["goods"]))

    def test_create_trader(self):
        agent = td.create_trader('trader', 0)
        name = agent.name
        pamt = agent["goods"]["penguin"][AMT_AVAIL]
        camt = agent["goods"]["cat"][AMT_AVAIL]
        bamt = agent["goods"]["bear"][AMT_AVAIL]
        pfamt = agent["goods"]["pet food"][AMT_AVAIL]
        self.assertEqual(name, "trader0")
        self.assertEqual(camt, 0)
        self.assertEqual(pamt, 0)
        self.assertEqual(bamt, 0)
        self.assertEqual(pfamt, 0)

    if __name__ == '__main__':
        main()
