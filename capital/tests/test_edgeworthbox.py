"""
This is the test suite for drunks.py.
"""

from unittest import TestCase, main

import capital.edgeworthbox as edge


class EdgeworthboxTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_gen_util_func(self):
        util = edge.gen_util_func(0)
        self.assertEqual(util, edge.DEF_MAX_UTIL)

    if __name__ == '__main__':
        main()
