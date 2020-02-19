"""
This is the test suite for trade.py.
"""

from unittest import TestCase, main

import capital.trade as td
import capital.trade_utils as tu
from capital.trade_utils import AMT_AVAILABLE


class tradeTestCase(TestCase):
    def setUp(self, props=None):
        self.goodA = {AMT_AVAILABLE: 10}
        self.goodB = {AMT_AVAILABLE: 10}
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

    if __name__ == '__main__':
        main()
