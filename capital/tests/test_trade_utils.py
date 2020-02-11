"""
This is the test suite for trade.py.
"""

from unittest import TestCase, main

from capital.trade_utils import endow, is_depleted, AMT_AVAILABLE


class TradeUtilsTestCase(TestCase):
    def setUp(self, props=None):
        pass

    def tearDown(self):
        pass

    def test_endow(self):
        """
        See capital.trade_utils for description of what a
        `trader` and `goods` must look like.
        """
        goodA = {AMT_AVAILABLE: 10}
        goodB = {AMT_AVAILABLE: 10}
        trader = {"goods": {}}
        goods = {"a": goodA, "b": goodB}
        endow(trader, goods)
        self.assertFalse(is_depleted(trader["goods"]))

    if __name__ == '__main__':
        main()
