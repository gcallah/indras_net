"""
This is the test suite for flocking.py.
"""

from unittest import TestCase, main

from propargs.propargs import PropArgs

from models.flocking import set_up, create_bird
from models.flocking import COMP_BIRD_NAME

TEST_BNAME = "Birds"

class FlockingTestCase(TestCase):
    def setUp(self):
        self.pa = PropArgs.create_props('flocking_props',
                                        ds_file='props/flocking.props.json')
        (self.the_sky,  self.flock) = set_up()

    def tearDown(self):
        (self.the_sky, self.flock) = (None, None)

    def test_create_bird(self):
        """
        Test to see if bird is created
        """
        new_bird = create_bird(TEST_BNAME, 1, props=self.pa)
        self.assertEqual(new_bird.name, COMP_BIRD_NAME + str(1))


    if __name__ == '__main__':
        main()
