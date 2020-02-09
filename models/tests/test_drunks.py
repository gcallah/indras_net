"""
This is the test suite for drunks.py.
"""

from unittest import TestCase, main

import models.drunks as drunks
from models.drunks import set_up


class DrunksTestCase(TestCase):
    def setUp(self):
        (self.drinkers, self.nondrinkers) = set_up()
        self.agent = drunks.create_drinker("drunk", 1)

    def tearDown(self):
        (self.drinkers, self.nondrinkers) = (None, None)

    def test_get_decision(self):
        val = drunks.get_decision(self.agent)
        self.assertEqual(isinstance(val, bool), True)

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

    def test_discourage(self):
        discouraged = drunks.discourage(1)
        self.assertEqual(discouraged, 1)

    if __name__ == '__main__':
        main()
