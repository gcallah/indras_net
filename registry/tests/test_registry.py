"""
This is the test suite for registry.py.
"""

from unittest import TestCase, main

from registry.registry import Registry, REGISTRY, get_prop
from registry.registry import set_env, get_env, add_group, get_group

TEST_VAL_STR = "test_val"
TEST_VAL = 1


class RegisteryTestCase(TestCase):
    def setUp(self):
        self.reg = Registry()
        self.reg[TEST_VAL_STR] = TEST_VAL

    def tearDown(self):
        self.reg = None

    def test_get_item(self):
        self.assertEqual(TEST_VAL, self.reg[TEST_VAL_STR])

    def test_get_prop_no_pa(self):
        """
        No prop args set up... can we still get prop ok?
        """
        prop_val = get_prop("key", "default")
        self.assertEqual(prop_val, "default")

    def test_get_env(self):
        """
        We don't need to use "real" Env: just make sure get returns
        what set put in!
        """
        set_env("Test")
        env = get_env()
        self.assertEqual(env, "Test")

    def test_get_group(self):
        """
        Don't worry about using a "real" group: just make sure we
        get what was added!
        """
        add_group("Group name", "Test")
        grp = get_group("Group name")
        self.assertEqual(grp, "Test")
