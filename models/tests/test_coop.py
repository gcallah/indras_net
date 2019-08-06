"""
This is the test suite for space.py.
"""

from propargs.propargs import PropArgs
from unittest import TestCase, main
from indra.env import Env
from indra.composite import Composite
from models.coop import set_up, create_babysitter, create_central_bank
from models.coop import classify_goal, classify_group, exchange
from models.coop import distribute_coupons, coop_action, act, DEF_COUPON
from models.coop import DEF_SIGMA, DEF_DISTRIBUTING_COUPON, DEF_PERCENT
from models.coop import babysitter_action, central_bank_action, CENTRAL_BANK
import models.coop as coop
import random

TEST_BABYSITTER_NUM = 3
TEST_CENTRAL_BANK_NUM = 3

class coopTestCase(TestCase):
    def setUp(self):
        self.pa = PropArgs.create_props('coop_props',
                                        ds_file='props/coop.props.json')
        (coop.coop_env, coop.groups, coop.group_indices) = set_up()

    def tearDown(self):
        coop.coop_env = None
        coop.groups = None
        coop.group_indices = None

    def test_create_babysitter(self):
        """
         Test to see if babysitter is created
        """
        new_babysitter = create_babysitter("babysitters", 0, self.pa)
        self.assertTrue(new_babysitter["min_holding"] >= 0)

    def test_create_central_bank(self):
        """
        Test to see if central bank is created
        """
        new_central_bank = create_central_bank("central_bank", 0, self.pa)
        self.assertTrue(new_central_bank["percent_change"] >= 0)

    def test_classify_goal(self):
        coop.groups = []
        coop.groups.append(Composite("BBSIT"))
        coop.groups.append(Composite("GO_OUT"))
        coop.groups.append(Composite("B_HOME"))
        coop.groups.append(Composite("G_HOME"))
        new_babysitter0 = create_babysitter("babysitters", 0, self.pa)
        new_babysitter0["goal"] = "BABYSITTING"
        coop.groups[0] += new_babysitter0
        (b_group, g_group) = classify_goal(coop.coop_env)
        self.assertTrue(len(b_group) == 1)

    def test_classify_group(self):
        coop.groups = []
        coop.groups.append(Composite("BBSIT"))
        coop.groups.append(Composite("GO_OUT"))
        coop.groups.append(Composite("B_HOME"))
        coop.groups.append(Composite("G_HOME"))
        new_babysitter0 = create_babysitter("babysitters", 0, self.pa)
        new_babysitter0["goal"] = "BABYSITTING"
        coop.groups[0] += new_babysitter0
        (b_group, g_group) = classify_goal(coop.coop_env)
        classify_group(b_group, g_group)
        self.assertTrue(len(coop.groups[0]) == 1)

    def test_exchange(self):
        coop.groups = []
        coop.groups.append(Composite("BBSIT"))
        coop.groups.append(Composite("GO_OUT"))
        coop.groups.append(Composite("B_HOME"))
        coop.groups.append(Composite("G_HOME"))
        new_babysitter0 = create_babysitter("babysitters", 0, self.pa)
        new_babysitter0["goal"] = "BABYSITTING"
        coop.groups[0] += new_babysitter0
        (b_group, g_group) = classify_goal(coop.coop_env)
        classify_group(b_group, g_group)
        exchange(coop.coop_env)
        self.assertTrue(len(coop.groups[0]) == 0)
        self.assertTrue(len(coop.groups[1]) == 0)
        self.assertTrue(len(coop.groups[2]) == 1)
        self.assertTrue(len(coop.groups[3]) == 0)

    def test_distribute_coupons(self):
        coop.groups = []
        coop.groups.append(Composite("BBSIT"))
        coop.groups.append(Composite("GO_OUT"))
        coop.groups.append(Composite("B_HOME"))
        coop.groups.append(Composite("G_HOME"))
        coop.groups.append(Composite("CENTRAL_BANK"))
        new_babysitter0 = create_babysitter("babysitters", 0, self.pa)
        new_babysitter0["coupons"] = DEF_COUPON
        coop.groups[0] += new_babysitter0
        new_central_bank = create_central_bank("CENTRAL_BANK", 0, self.pa)
        new_central_bank["extra_coupons"] = DEF_DISTRIBUTING_COUPON
        new_central_bank["extra_dev"] = DEF_SIGMA
        new_babysitter0["coupons"] = DEF_COUPON
        distribute_coupons(new_central_bank)
        print(new_babysitter0["coupons"])
        self.assertTrue(new_babysitter0["coupons"] > DEF_COUPON)

    def test_act(self):
        new_babysitter0 = create_babysitter("babysitters", 0, self.pa)
        new_babysitter0["goal"] = None
        new_babysitter0["coupons"] = DEF_COUPON - 1
        new_babysitter0["min_holding"] = DEF_COUPON
        act(new_babysitter0)
        self.assertEqual(new_babysitter0["goal"], "BABYSITTING")

    def test_coup_action(self):
        pass

    def test_babysitter_action(self):
        '''
        Test the babysitter action
        '''
        new_babysitter0 = create_babysitter("babysitters", 0, self.pa)
        new_babysitter0["coupons"] = 0
        babysitter_action(new_babysitter0)
        self.assertTrue(new_babysitter0["sitting"] == True)
        

    def test_central_bank_action(self):
        '''
        Test the central bank action
        '''
        pass


    if __name__ == '__main__':
        main()
