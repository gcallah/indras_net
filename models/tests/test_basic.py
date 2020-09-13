"""
This is the test suite for space.py.
"""

from unittest import TestCase, main

from propargs.propargs import PropArgs

import models.basic as ba


class BasicTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_main(self):
        # a way to see what version nose is running:
        import platform
        print("Python version: ", platform.python_version())
        self.assertEqual(ba.main(), 0)

    if __name__ == '__main__':
        main()
