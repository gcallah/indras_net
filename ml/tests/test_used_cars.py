"""
This is the test suite for flocking.py.
"""
import random
from unittest import TestCase, main
from propargs.propargs import PropArgs
import ml.used_cars as uc


TEST_RAND_AMT = 20
GROUP_SIZE = 10

class UsedCarTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_main(self):
        self.assertEqual(uc.main(), 0)

    if __name__ == '__main__':
        main()
