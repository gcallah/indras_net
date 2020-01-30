"""
This is the test suite for flocking.py.
"""
import random
from unittest import TestCase, main
from propargs.propargs import PropArgs
from indra.env import Env
from ml.used_cars import *
from ml.used_cars import MIN_GOOD_CAR_LIFE, MAX_CAR_LIFE


TEST_RAND_AMT = 20


class UsedCarTestCase(TestCase):
    def setUp(self):
        self.pa = PropArgs.create_props('used_car_props',
                                        ds_file='props/used_cars.props.json')
        (self.car_market, self.dealers, self.buyers) = set_up(10)  # noqa: F405

    def tearDown(self):
        (self.car_market, self.dealers, self.buyers) = (None, None, None)

    def test_is_dealer(self):
        dealer = create_dealer("Dealers", 1, None)
        buyer = create_buyer("Buyers", 0, None)
        self.assertTrue(is_dealer(buyer, self.dealers) is False)
        self.assertTrue(is_dealer(dealer, self.dealers) is True)

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

    def test_get_dealer_characteristic(self):
        charac = get_dealer_characteristic()
        self.assertTrue(charac == "good" or charac == "bad")

    def test_set_emoji_indicator(self):
        buyer1 = create_buyer("Buyers",0, None)
        buyer2 = create_buyer("Buyers",1, None)
        buyer1["emoji_life_avg"] = {"unnatural": 1}
        buyer2["emoji_life_avg"] = {"relaxing": 5}
        set_emoji_indicator(buyer1)
        set_emoji_indicator(buyer2)
        self.assertEqual(buyer1["emoji_indicator"]["unnatural"], "bad")
        self.assertEqual(buyer2["emoji_indicator"]["relaxing"], "good")
        
    def test_get_dealer_emoji(self):
        emoji1 = get_dealer_emoji("good")
        emoji2 = get_dealer_emoji("bad")
        self.assertIn(emoji1, POS_EMOJIS)
        self.assertIn(emoji2, NEG_EMOJIS)
        
    def test_update_dealer_sale(self):
        dealer1 = create_dealer("Dealers", 0, None)
        dealer2 = create_dealer("Dealers", 1, None)
        num_sales = random.randint(1,100)
        dealer2["num_sales"] = num_sales
        new_car_life = random.randint(0,5)
        avg_life = round(random.randrange(1,5),2)
        dealer2["avg_car_life_sold"] = avg_life
        update_dealer_sale(dealer1, new_car_life)
        update_dealer_sale(dealer2, new_car_life)
        self.assertEqual(dealer1["num_sales"], 1 )
        self.assertEqual(dealer2["num_sales"], num_sales + 1)
        self.assertEqual(dealer1["num_sales"], 1 )
        self.assertEqual(dealer1["avg_car_life_sold"],new_car_life)
        self.assertEqual(dealer2["avg_car_life_sold"],
                         round((avg_life + new_car_life) / (num_sales + 1), 2))
        
    def test_is_mature(self):
        buyer = create_buyer("Buyer", 0, None)
        self.assertFalse(is_mature(buyer))
        buyer["dealer_hist"] = [1] * MATURE_BOUND
        buyer["dealer_hist"].append(1)
        self.assertTrue(is_mature(buyer))
        
    def test_is_credible(self):
        buyer = create_buyer("Buyer", 0, None)
        dealer = create_dealer("Dealer", 0, None)
        self.assertTrue(is_credible(dealer,buyer))
        emoji = random.choice(POS_EMOJIS + NEG_EMOJIS)
        score = random.randint(1,5)
        buyer["emoji_life_avg"] = {emoji:score}
        buyer["dealer_hist"] = [1] * (MATURE_BOUND+1)
        dealer["emoji_used"] = emoji        
        if score >= MIN_GOOD_CAR_LIFE:
            self.assertTrue(is_credible(dealer, buyer))
        else:
            self.assertFalse(is_credible(dealer, buyer))
            
    def test_cal_avg_life(self):
        buyer = create_buyer("Buyer", 0, None)
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
        
    def test_create_dealer(self):
        dealer = create_dealer("Dealer", 0, None)
        self.assertEqual(dealer["num_sales"], 0)
        self.assertIsNone(dealer["avg_car_life_sold"])
        self.assertEqual(dealer["curr_car_life"], 0)
        self.assertEqual(dealer["return_rate"], 0)
        self.assertEqual(dealer["num_completed_services"], 0)  
        self.assertIsNone(dealer["emoji_used"])
        self.assertIsNone(dealer["dealer_characteristic"])

    def test_create_buyer(self):
        """
        # Will fix this test case later
        # kept here for temp storage
        def test_buy_from_dealer(self):
        buyer = create_buyer("Buyer", 0, None)
        dealer = create_dealer("Dealer", 0, None)
        orig_assoc_length = len(buyer["emoji_carlife_assoc"])
        buy_from_dealer(buyer, dealer)
        is_deal_hist = len(buyer["dealer_hist"]) > 0
        dealer_emoji = dealer["emoji_used"]
        updated_assoc_length = len(buyer["emoji_carlife_assoc"])
        is_assoc_added = updated_assoc_length > orig_assoc_length
        self.assertEqual(buyer["has_car"], True)
        self.assertEqual(is_deal_hist, True)
        self.assertEqual(buyer["interaction_res"], dealer_emoji)
        self.assertEqual(is_assoc_added, True)
        """
        buyer = create_buyer("Buyer", 0, None)
        self.assertFalse(buyer["has_car"])
        self.assertIsNone(buyer["car_life"])
        self.assertIsNone(buyer["interaction_res"])
        self.assertEqual(buyer["dealer_hist"], [])
        self.assertEqual(buyer["emoji_carlife_assoc"], {})
        self.assertEqual(buyer["emoji_life_avg"], {})  
        self.assertEqual(buyer["emoji_indicator"], {})

    if __name__ == '__main__':
        main()
