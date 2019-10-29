"""
This is the test suite for flocking.py.
"""

from unittest import TestCase, main

from propargs.propargs import PropArgs

from models.flocking import set_up


class FlockingTestCase(TestCase):
    def setUp(self):
        self.pa = PropArgs.create_props('flocking_props',
                                        ds_file='props/flocking.props.json')
        (self.the_sky,  self.flock) = set_up()

    def tearDown(self):
        (self.the_sky, self.flock) = (None, None)

    if __name__ == '__main__':
        main()
