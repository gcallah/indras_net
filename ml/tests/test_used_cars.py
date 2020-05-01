"""
This is the test suite for flocking.py.
"""
import random
from unittest import TestCase, main
from propargs.propargs import PropArgs
from ml.used_cars import *


TEST_RAND_AMT = 20
GROUP_SIZE = 10

class UsedCarTestCase(TestCase):
    def setUp(self):
        set_up(GROUP_SIZE)
        
    def tearDown(self):
        pass
        self.pa = PropArgs.create_props('used_car_props',
                                        ds_file='props/used_cars.props.json')
        (self.car_market, self.dealers, self.buyers) = set_up(10)  # noqa: F405


    def tearDown(self):
        (self.car_market, self.dealers, self.buyers) = (None, None, None)


    if __name__ == '__main__':
        main()
