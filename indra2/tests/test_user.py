"""
This is the test suite for env.py.
"""

from unittest import TestCase, main

from indra2.user import not_impl, NOT_IMPL, TermUser


class UserTestCase(TestCase):
    def setUp(self):
        # we will need to change env above from None ASAP!
        self.user = TermUser("TestUser", None)

    def tearDown(self):
        self.user = None

    def test_not_impl(self):
        self.assertEqual(not_impl(self.user), NOT_IMPL)

if __name__ == '__main__':
    main()
