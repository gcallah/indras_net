"""
This is the test suite for trade.py.
"""
import copy
from unittest import TestCase, main
# from indra.agent import Agent
from capital.trade_utils import endow, get_rand_good, is_depleted, AMT_AVAILABLE, transfer
from capital.trade_utils import rand_dist, equal_dist, good_decay
import capital.trade_utils as tu

class TradeUtilsTestCase(TestCase):
    def setUp(self, props=None):
        self.goodA = {AMT_AVAILABLE: 10}
        self.goodB = {AMT_AVAILABLE: 10}
        self.goodC = {AMT_AVAILABLE: 10, "durability": 0.6}
        self.goodD = {AMT_AVAILABLE: 10, "durability": 0.9}
        self.trader = {"goods": {}}
        # self.agent = Agent()
        self.goods = {"a": self.goodA, "b": self.goodB}
        self.goods_dict_du = {"c": self.goodC, "d": self.goodD}
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


    def test_goods_to_string(self):
        ans1 = 1
        ans0 = 0
        ans_str_1 = tu.answer_to_str(ans1)
        ans_str_0 =tu.answer_to_str(ans0)
        self.assertEqual(ans_str_1, "I accept")
        self.assertEqual(ans_str_0, "I'm indifferent about")


    def test_answer_to_string(self):
        pass

    
    def test_rand_dist(self):
        """
        Test if trader dic and nature dic are changed after random distribution trade
        """
        trader_before_trade = copy.deepcopy(self.trader["goods"])
        nature_before_trade = copy.deepcopy(self.goods)
        rand_dist(self.trader["goods"], self.goods)
        print(repr(nature_before_trade))
        print(repr(self.goods))
        self.assertNotEqual(self.trader["goods"], trader_before_trade)
        self.assertNotEqual(self.goods, nature_before_trade)


    def test_equal_dist(self):
        """
        Test if trader get equal amout of goods from 
        all availiable resources
        """
        self.setUp(self)
        nature_before_trade = copy.deepcopy(self.goods)
        equal_dist(2,self.trader["goods"], self.goods)
        self.assertEqual(self.trader["goods"]["a"][AMT_AVAILABLE],
                         nature_before_trade["a"][AMT_AVAILABLE]/2)
        self.assertEqual(self.trader["goods"]["b"][AMT_AVAILABLE],
                         nature_before_trade["b"][AMT_AVAILABLE]/2)

    def test_good_decay(self):
        """
        Test if the durability of the goods get decayed
        """
        good_decay(self.goods_dict_du)
        self.assertEqual(self.goods_dict_du['c']['durability'], 0.36)
        self.assertEqual(self.goods_dict_du['d']['durability'], 0.81)

    if __name__ == '__main__':
        main()
