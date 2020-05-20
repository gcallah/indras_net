"""
This is the test suite for el_farol.py.
"""

from unittest import TestCase, main

import models.el_farol as el_farol
from models.el_farol import set_up, DRINKERS, NON_DRINKERS, MOTIV


class ElFarolTestCase(TestCase):
    def setUp(self):
        set_up()

    def tearDown(self):
        """
        This should undo what setup() does!
        """
        pass

    # an integration test:
    def test_main(self):
        self.assertEqual(el_farol.main(), 0)

    def test_create_non_drinker(self):
        """
        Test creating a non-drinker.
        """
        agent = el_farol.create_non_drinker(DRINKERS, 0)
        self.assertIn(MOTIV, agent)

    def test_create_drinker(self):
        """
        Test creating a drinker.
        """
        agent = el_farol.create_drinker(NON_DRINKERS, 0)
        self.assertIn(MOTIV, agent)

    def test_discourage(self):
        discouraged = el_farol.discourage(1)
        self.assertEqual(discouraged, 1)

    if __name__ == '__main__':
        main()
