"""
This is the test suite for space.py.
"""

from unittest import TestCase, main
from indra.env import Env
from models.fmarket import set_up
import models.fmarket as fm


class FMarketTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_set_up(self):
        """
        Test setting up env.
        """
        (env, grp1, grp2, agent) = set_up()
        self.assertTrue(isinstance(env, Env))

    def test_create_market_maker(self):
        mm = fm.create_market_maker("Fred")
        self.assertTrue(mm["buy"] == 0)

    if __name__ == '__main__':
        main()
