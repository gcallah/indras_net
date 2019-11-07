"""
This is the test suite for registry.py.
"""

from unittest import TestCase, main

from indra.registry import Registry, REGISTRY

TEST_VAL_STR = "test_val"
TEST_VAL = 1


class RegisteryTestCase(TestCase):
    def setUp(self):
        self.reg = Registry()
        self.reg[TEST_VAL_STR] = TEST_VAL

    def tearDown(self):
        self.reg = None

    def test_repr(self):
        """
        Test our registry representation.
        """
        s = repr(self.reg)
        self.assertTrue(REGISTRY in s)

    def test_get_item(self):
        self.assertEqual(TEST_VAL, self.reg[TEST_VAL_STR])
