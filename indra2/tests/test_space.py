"""
This is the test suite for space.py.
"""

from unittest import TestCase, main

from indra2.space import Space, distance, out_of_bounds
from indra2.agent import Agent
from indra2.tests.test_agent import create_newton, create_hardy, create_leibniz
from indra2.tests.test_agent import create_ramanujan


def create_space():
    space = Space("test space")
    space += create_newton()
    space += create_hardy()
    space += create_leibniz()
    return space


class SpaceTestCase(TestCase):
    def test_place_members(self):
        """
        Test place_members() by making sure all agents have a pos
        when done.
        """
        space = create_space()
        for agent in space:
            self.assertTrue(space[agent].islocated())

    def test_rand_x(self):
        """
        Make sure randomly generated pos is within grid.
        """
        space = Space("test space")
        x = space.rand_x()
        self.assertTrue(x >= 0)
        self.assertTrue(x < space.width)

    def test_rand_y(self):
        """
        Make sure randomly generated pos is within grid.
        """
        space = Space("test space")
        y = space.rand_y()
        self.assertTrue(y >= 0)
        self.assertTrue(y < space.height)

    def test_location(self):
        """
        Test all methods regarding the location of positions
        TODO: some of them are not used yet
        """
        space = Space("test space")
        n = create_newton()
        space += n
        # check if the agent is placed at the right location
        self.assertTrue(space.locations[n.pos] == n)

if __name__ == '__main__':
    main()
