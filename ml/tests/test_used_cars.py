"""
This is the test suite for flocking.py.
"""
import random
from unittest import TestCase, main
from propargs.propargs import PropArgs
from ml.used_cars import *


TEST_RAND_AMT = 20
GROUP_SIZE = 10

class UsedCarTestCase(TestCase):
    def setUp(self):
        set_up(GROUP_SIZE)
        
    def tearDown(self):
        pass
        self.pa = PropArgs.create_props('used_car_props',
                                        ds_file='props/used_cars.props.json')
        (self.car_market, self.dealers, self.buyers) = set_up(10)  # noqa: F405


    def tearDown(self):
        (self.car_market, self.dealers, self.buyers) = (None, None, None)

    def test_is_dealer(self):
        dealer = create_dealer(DEALER_GRP, 1, None)
        buyer = create_buyer(BUYER_GRP, 0, None)
        self.assertTrue(is_dealer(buyer) is False)
        self.assertTrue(is_dealer(dealer) is False)


    def test_is_mature(self):
        buyer = create_buyer(BUYER_GRP, 0, None)
        self.assertFalse(is_mature(buyer))


    def test_cal_avg_life(self):
        pass
        '''
        the following needs to be changed
        buyer = create_buyer(BUYER_GRP, 0, None)
        num = random.randint(0,10)
        emoji_carlife_lst1 = [num for i in range(10)]
        emoji1 = random.choice(POS_EMOJIS + NEG_EMOJIS)
        emoji_carlife_lst2 = [num for i in range(10)]
        emoji2 = random.choice(POS_EMOJIS + NEG_EMOJIS)
        buyer["emoji_carlife_assoc"]={emoji1: emoji_carlife_lst1,
                                      emoji2: emoji_carlife_lst2}
        buyer["emoji_life_avg"] = {emoji1: 0, emoji2: 0}
        cal_avg_life(buyer)
        for key in buyer["emoji_life_avg"]:
            self.assertEqual(buyer["emoji_life_avg"][key], round(num,2))
            '''


    def test_create_buyer(self):
        buyer = create_buyer(BUYER_GRP, 0, None)
        self.assertFalse(buyer["has_car"])
        self.assertIsNone(buyer["car_life"])
        self.assertIsNone(buyer["dealer"])
        self.assertEqual(buyer["emoji_carlife_assoc"], {})
        self.assertEqual(buyer["emoji_life_avg"], {})
        self.assertEqual(buyer["maturality"], 0)


    if __name__ == '__main__':
        main()
