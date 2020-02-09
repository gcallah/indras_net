"""
This is the test suite for flocking.py.
"""

from unittest import TestCase, main

from propargs.propargs import PropArgs

from models.flocking import BIRD_GROUP
from models.flocking import set_up, create_bird

TEST_BNAME = "Birds"
TEST_BNUM1 = 5
TEST_BNUM2 = 6


# TEST_DESIRED_DISTANCE = 2
# TEST_ACCEPTABLE_DEV = .05

class FlockingTestCase(TestCase):
    def setUp(self):
        self.pa = PropArgs.create_props('flocking_props',
                                        ds_file='props/flocking.props.json')
        (self.flock) = set_up()
        self.bird_a = create_bird(TEST_BNAME, TEST_BNUM1, props=self.pa)
        self.bird_b = create_bird(TEST_BNAME, TEST_BNUM2, props=self.pa)

    def tearDown(self):
        (self.flock) = (None)

    def test_create_bird(self):
        """
        Test to see if bird is created
        """
        new_bird = create_bird(TEST_BNAME, 1, props=self.pa)
        self.assertEqual(new_bird.name, BIRD_GROUP + str(1))

    if __name__ == '__main__':
        main()
