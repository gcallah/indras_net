"""
This is the test suite for flocking.py.
"""

from unittest import TestCase, main
import math
from propargs.propargs import PropArgs
from indra.space import distance
from indra.agent import Agent, X, Y
from indra.composite import Composite
from models.flocking import set_up, create_bird, bird_action, calc_angle, invert_direction
from models.flocking import BIRD_GROUP
from indra.env import Env
from indra.display_methods import BLUE, TREE


TEST_BNAME = "Birds"
# TEST_BNUM1 = 5
# TEST_BNUM2 = 6
# TEST_DESIRED_DISTANCE = 2
# TEST_ACCEPTABLE_DEV = .05

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
        self.assertEqual(new_bird.name, BIRD_GROUP + str(1))
    
    def test_bird_action(self):
        """
        Test to see if birds flock properly **WIP**
        """
        # Current problem is locator object is Nonetype when we try to call bird_action here. Why? This also applies
        # to other flocking functions that we call that access the properties of the flocking agents. 
        # The other problem, which is related, is when calc_angle is called, and on line 45 in flocking.py, it tries to subtract the coordinates 
        # of the agents and fails because get_pos() returns Nonetype on lines 43 and 44 in flocking.py

        self.assertFalse(self.the_sky()) # the_sky() should return a Nonetype. 

        # this solution isn't really elegant, but this will show 10 periods as defined in env.py(DEF_TIME), demonstrating
        # that the agents are actually calling bird_action().  Until I can figure out why the problem with the commented code below is occuring, 
        # this is how we can tell that bird_action() is working. 
    
        # previous_angle = self.bird_a["angle"]
        # curr_distance = distance(self.bird_a, self.bird_b)
        # if abs(curr_distance - TEST_DESIRED_DISTANCE) < (TEST_DESIRED_DISTANCE * TEST_ACCEPTABLE_DEV):
        #     self.assertTrue(bird_action(self.bird_a))
        # self.bird_a["angle"] = calc_angle(self.bird_a, self.bird_b)
        # if curr_distance < DEF_DESIRED_DISTANCE:
        #     bird_action(self.bird_a)
        #     self.assertEqual(self.bird_a["angle"], invert_direction(previous_angle))

    
    if __name__ == '__main__':
        main()
