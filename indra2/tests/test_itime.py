"""
This is the test suite for entity.py.
"""

from unittest import TestCase, main

from indra2.itime import Time
from indra2.tests.test_composite import create_mathguys


class ITimeTestCase(TestCase):
    def test_call(self):
        mh = Time("History", members=[create_mathguys()])
        acts = mh(5)
        self.assertEqual(acts, 14)


if __name__ == '__main__':
    main()
