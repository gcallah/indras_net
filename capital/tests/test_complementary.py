"""
This is the test suite for trade.py.
"""

from unittest import TestCase, main, skip

import capital.trade_utils as tu
import capital.complementary as cp
from capital.complementary import COMPLEMENTS, DEF_NUM_RESOURCES

from capital.trade_utils import AMT_AVAIL, seek_a_trade
from capital.trade_utils import gen_util_func, trade, DEF_MAX_UTIL
from capital.trade_utils import UTIL_FUNC, GEN_UTIL_FUNC, AMT_AVAIL


class tradeTestCase(TestCase):
    def setUp(self, props=None):
        self.trader = cp.create_trader("trader", 0)
        self.goods = {
                     "truck": {AMT_AVAIL: 1,
                               UTIL_FUNC: "steep_util_func",
                               "incr": 0,
                               COMPLEMENTS: ["fuel", "land"]},
                     "penguin": {AMT_AVAIL: 1,
                                 UTIL_FUNC: "steep_util_func",
                                 "incr": 0,
                                 COMPLEMENTS: ["pet_food",
                                               "meat"]},
                     "pet_food": {AMT_AVAIL: 1,
                                  UTIL_FUNC: "steep_util_func",
                                  "incr": 0,
                                  COMPLEMENTS: ["penguin",
                                                "meat"]},
                     "fuel": {AMT_AVAIL: 1,
                              UTIL_FUNC: "steep_util_func",
                              "incr": 0,
                              COMPLEMENTS: ["truck", "land"]},
                     "land": {AMT_AVAIL: 1,
                              UTIL_FUNC: "steep_util_func",
                              "incr": 0,
                              COMPLEMENTS: ["truck", "fuel"]},
                     "meat": {AMT_AVAIL: 1,
                              UTIL_FUNC: "steep_util_func",
                              "incr": 0,
                              COMPLEMENTS: ["penguin",
                                            "pet_food"]}
                    }


    def tearDown(self):
        self.goodA = None
        self.goodB = None
        self.trader = None
        self.goods = None


    def test_main(self):
        print(cp.main())
        self.assertEqual(cp.main(), 0)


    def test_create_trader(self):
        self.trader = cp.create_trader("trader", 0)
        name = self.trader.name
        incr = self.trader["goods"]["truck"]["incr"]
        self.assertEqual(incr, 0)


    def test_allocate_resources(self):
        self.trader = cp.create_trader("trader", 0)
        cp.allocate_resources(self.trader, self.goods)
#         empty = tu.is_depleted(self.trader["goods"])
#         self.assertFalse(empty)
        self.assertIsNotNone(self.trader["goods"]["truck"][COMPLEMENTS])


    if __name__ == '__main__':
        main()
