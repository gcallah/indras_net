"""
This is the test suite for forestfire.py.
"""

from unittest import TestCase

import models.forestfire as ff
from indra.agent import possible_trans
from indra.registry import get_env
from models.forestfire import is_healthy, OF, set_up, STATE_TRANS, TREE_PREFIX
from models.forestfire import plant_tree

TEST_ANUM = 999999

TEST_REPS = 20


def print_sep():
    print("________________________", flush=True)


class ForestfireTestCase(TestCase):
    def setUp(self):
        self.test_tree = plant_tree(TREE_PREFIX, TEST_ANUM)
        (ff.group_map) = set_up()
        ff.healthy += self.test_tree
        get_env().place_member(self.test_tree)

    def tearDown(self):
        self.test_tree = None
        ff.forest = None
        ff.group_map = None

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

    def test_tree_action(self):
        for i in range(TEST_REPS):
            start_state = self.test_tree["state"]
            ret = self.test_tree()
            self.assertTrue(True)
            end_state = self.test_tree["state"]
            self.assertTrue(possible_trans(STATE_TRANS,
                                           start_state,
                                           end_state))
