"""
This is the test suite for forestfire.py.
"""

from unittest import TestCase

import models.forestfire as ff
from indra.agent import possible_trans
from registry.registry import get_env
from models.forestfire import is_healthy, OF, set_up, TREE_PREFIX
from models.forestfire import plant_tree

TEST_ANUM = 999999

TEST_REPS = 20


def print_sep():
    print("________________________", flush=True)


class ForestfireTestCase(TestCase):
    def setUp(self):
        self.test_tree = plant_tree(TREE_PREFIX, TEST_ANUM)
        set_up()

    def tearDown(self):
        self.test_tree = None

    # an integration test:
    def test_main(self):
        self.assertEqual(ff.main(), 0)

    def test_is_healthy(self):
        """
        See if target tree is healthy.
        All trees should start out healthy!
        """
        self.assertTrue(is_healthy(self.test_tree))

    def test_plant_tree(self):
        new_tree = plant_tree(TREE_PREFIX, TEST_ANUM + 1)
        self.assertTrue(is_healthy(new_tree))
        new_tree = plant_tree(TREE_PREFIX, TEST_ANUM + 1, state=OF)
        self.assertFalse(is_healthy(new_tree))
