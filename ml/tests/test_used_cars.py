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
        """
        See if an agent is a dealer or not.
        """
        dealer = create_dealer("Dealer", 0, None)
        self.assertFalse(is_dealer(agent, self.dealers))
        self.dealers += dealer
        self.assertTrue(is_dealer(agent, self.dealers))

    def test_is_mature(self):
        buyer = create_buyer("Buyer", 0, None)
        self.assertFalse(is_mature(buyer))
        buyer["dealer_hist"] = [1] * MATURE_BOUND
        buyer["dealer_hist"].append(1)
        self.assertTrue(is_mature(buyer))

    def test_get_dealer_car(self):
        result = get_dealer_car("good")
        self.assertGreaterEqual(result, MIN_GOOD_CAR_LIFE)
        self.assertLessEqual(result, MAX_CAR_LIFE)
        result = get_dealer_car("bad")
        self.assertTrue(result >= MIN_CAR_LIFE)
        self.assertTrue(result <= MAX_BAD_CAR_LIFE)

    def test_create_buyer(self):
        buyer = create_buyer("Buyer", 0, None)
        self.assertTrue(buyer["has_car"] is False)
        self.assertTrue(buyer["car_life"] is None)
        self.assertTrue(buyer["interaction_res"] is None)
        self.assertTrue(buyer["dealer_hist"] ==  [])
        self.assertTrue(buyer["emoji_carlife_assoc"] == {})
        self.assertTrue(buyer["emoji_life_avg"] == {})  
        self.assertTrue(buyer["emoji_indicator"] == {})

    def test_create_dealer(self):
        dealer = create_dealer("Dealer", 0, None)
        self.assertEqual(dealer["num_sales"], 0)
        self.assertTrue(dealer["avg_car_life_sold"] is None)
        self.assertTrue(dealer["curr_car_life"] ==  0)
        self.assertTrue(dealer["return_rate"] == 0)
        self.assertTrue(dealer["num_completed_services"] == 0)  
        self.assertTrue(dealer["emoji_used"] is None)
        self.assertTrue(dealer["dealer_characteristic"] is None)

    def test_get_car_life(self):
        dealer = create_dealer("Dealers", 0, None)
        feed_car_life= random.randint(0,5)
        dealer["curr_car_life"] = feed_car_life
        car_life = get_car_life(dealer)
        self.assertTrue(car_life == feed_car_life)


    def test_is_dealer(self):
        dealer = create_dealer("Dealers", 1, None)
        buyer = create_buyer("Buyers",0, None)
        self.assertTrue(is_dealer(buyer,self.dealers) is False)
        self.assertTrue(is_dealer(dealer,self.dealers) is True)



    
    if __name__ == '__main__':
        main()
    

        
