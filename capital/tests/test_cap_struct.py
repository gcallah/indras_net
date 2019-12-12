"""
This is the test suite for drunks.py.
"""

from unittest import TestCase, main

import capital.cap_struct as cap


class CapitalTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_entr(self):
        entr = cap.create_entr("Manxueying", 1)
        self.assertEqual(entr.name, "Manxueying1")

    if __name__ == '__main__':
        main()
