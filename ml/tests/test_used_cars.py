"""
This is the test suite for flocking.py.
"""
import random
from unittest import TestCase, main
from propargs.propargs import PropArgs
from indra.env import Env
from ml.used_cars import *
from ml.used_cars import MIN_GOOD_CAR_LIFE, MAX_CAR_LIFE
from ml.used_cars import MIN_CAR_LIFE, MAX_BAD_CAR_LIFE

TEST_RAND_AMT = 20


class UsedCarTestCase(TestCase):
    def setUp(self):
        self.pa = PropArgs.create_props('used_car_props',
                                        ds_file='props/used_cars.props.json')
        (self.car_market, self.dealers, self.buyers) = set_up()

    def tearDown(self):
        (self.car_market, self.dealers, self.buyers) = (None, None, None)

    def test_is_dealer(self):
        dealer = create_dealer("Dealers", 1, None)
        buyer = create_buyer("Buyers",0, None)
        self.assertTrue(is_dealer(buyer,self.dealers) is False)
        self.assertTrue(is_dealer(dealer,self.dealers) is True)
        
    def test_get_car_life(self):
        dealer = create_dealer("Dealers", 0, None)
        feed_car_life= random.randint(0,5)
        dealer["curr_car_life"] = feed_car_life
        car_life = get_car_life(dealer)
        self.assertEqual(car_life, feed_car_life)
    
    def test_get_dealer_car(self):
        result = get_dealer_car("good")
        self.assertGreaterEqual(result, MIN_GOOD_CAR_LIFE)
        self.assertLessEqual(result, MAX_CAR_LIFE)
        result = get_dealer_car("bad")
        self.assertGreaterEqual(result, MIN_CAR_LIFE)
        self.assertLessEqual(result, MAX_BAD_CAR_LIFE)
        
    

    def test_is_mature(self):
        buyer = create_buyer("Buyer", 0, None)
        self.assertFalse(is_mature(buyer))
        buyer["dealer_hist"] = [1] * MATURE_BOUND
        buyer["dealer_hist"].append(1)
        self.assertTrue(is_mature(buyer))

    def test_create_dealer(self):
        dealer = create_dealer("Dealer", 0, None)
        self.assertEqual(dealer["num_sales"], 0)
        self.assertEqual(dealer["avg_car_life_sold"], None)
        self.assertEqual(dealer["curr_car_life"], 0)
        self.assertEqual(dealer["return_rate"], 0)
        self.assertEqual(dealer["num_completed_services"], 0)  
        self.assertEqual(dealer["emoji_used"], None)
        self.assertEqual(dealer["dealer_characteristic"], None)
    
    def test_create_buyer(self):
        buyer = create_buyer("Buyer", 0, None)
        self.assertFalse(buyer["has_car"])
        self.assertEqual(buyer["car_life"], None)
        self.assertEqual(buyer["interaction_res"], None)
        self.assertEqual(buyer["dealer_hist"], [])
        self.assertEqual(buyer["emoji_carlife_assoc"], {})
        self.assertEqual(buyer["emoji_life_avg"], {})  
        self.assertEqual(buyer["emoji_indicator"], {})




    
    if __name__ == '__main__':
        main()
    

        
