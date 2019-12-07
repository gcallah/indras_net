"""
This is the test suite for flocking.py.
"""

from unittest import TestCase, main
import math
from propargs.propargs import PropArgs
from indra.space import distance
from indra.agent import Agent, X, Y
from indra.composite import Composite
from models.flocking import set_up, create_bird, bird_action, calc_angle
from models.flocking import COMP_BIRD_NAME


TEST_BNAME = "Birds"
TEST_BNUM1 = 5
TEST_BNUM2 = 6
TEST_DESIRED_DISTANCE = 2
TEST_ACCEPTABLE_DEV = .05

class FlockingTestCase(TestCase):
    def setUp(self):
        self.pa = PropArgs.create_props('flocking_props',
                                        ds_file='props/flocking.props.json')
        (self.the_sky,  self.flock) = set_up()
        self.bird_a = create_bird(TEST_BNAME, TEST_BNUM1, props=self.pa)
        self.bird_b = create_bird(TEST_BNAME, TEST_BNUM2, props=self.pa)

    def tearDown(self):
        (self.the_sky, self.flock) = (None, None)

    def test_create_bird(self):
        """
        Test to see if bird is created
        """
        new_bird = create_bird(TEST_BNAME, 1, props=self.pa)
        self.assertEqual(new_bird.name, COMP_BIRD_NAME + str(1))
    
    def test_bird_action(self):
        """
        Test to see if birds flock properly **WIP**
        """

        previous_angle = self.bird_a["angle"]
        curr_distance = distance(self.bird_a, self.bird_b)
        if abs(curr_distance - TEST_DESIRED_DISTANCE) < (TEST_DESIRED_DISTANCE * TEST_ACCEPTABLE_DEV):
            self.assertTrue(bird_action(self.flock[0]))
        self.bird_a["angle"] = calc_angle(self.bird_a, self.bird_b)
        if curr_distance < DEF_DESIRED_DISTANCE:
            bird_action(self.bird_a)
            self.assertEqual(self.bird_a["angle"], invert_direction(previous_angle))


    if __name__ == '__main__':
        main()
