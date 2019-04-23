"""
This is the test suite for space.py.
"""

from unittest import TestCase, main
from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env
from models.forestfire import get_new_state, NUM_STATES, plant_tree
# from models.forestfire import GROUP_MAP

TEST_ANUM = 999999


def print_sep():
    print("________________________", flush=True)

class ForestfireTestCase(TestCase):
    def setUp(self):
        self.test_tree = plant_tree(TEST_ANUM)

    def tearDown(self):
        self.test_tree = None

    def test_get_new_state(self):
        """
        Make sure we change tree states in an orderly fashion.
        """
        for i in range(NUM_STATES):
            new_state = get_new_state(i)
            self.assertEqual(new_state, (i + 1) % NUM_STATES)
