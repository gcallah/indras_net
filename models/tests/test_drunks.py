"""
This is the test suite for drunks.py.
"""

from unittest import TestCase, main
from operator import gt, lt
from indra.agent import switch
from indra.env import Env
from models.drunks import set_up
import models.drunks as drunks


class DrunksTestCase(TestCase):
    def setUp(self):
        (self.bar, self.drinkers, self.nondrinkers) = set_up()

    def tearDown(self):
        (self.bar, self.drinkers, self.nondrinkers) = (None, None, None)

    def test_create_non_drinker(self):
        """
        Test creating a non-drinker.
        """
        agent = drunks.create_non_drinker("non-drunk", 0)
        self.assertEqual(agent.name, "non-drunk0")

    def test_create_drinker(self):
        """
        Test creating a drinker.
        """
        agent = drunks.create_drinker("drunk", 0)
        self.assertEqual(agent.name, "drunk0")

    if __name__ == '__main__':
        main()
