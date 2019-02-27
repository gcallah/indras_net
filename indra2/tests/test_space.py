"""
This is the test suite for agent.py.
"""

from unittest import TestCase, main

from indra2.space import Space
from indra2.agent import Agent

class SpaceTestCase(TestCase):
    def test_place_members(self):
        """
        Test place_members() by making sure all agents have a pos
        when done.
        """
        space = Space("test space")
        # add members, then test that they all have a pos
        # self.assertEqual()

    def test_rand_x(self):
        space = Space("test space")
        x = space.rand_x()
        self.assertTrue(x >= 0)
        self.assertTrue(x < space.width)

    def test_neighborhood(self):
        pass

    def test_location(self):
        """
        Test all methods regarding the location of positions
        TODO: some of them are not used yet
        """
        space = Space("test space")
        n = Agent("Newton",
                  attrs={"place": 0.0, "time": 1658.0, "achieve": 43.9},
                  duration=30)
        space += n
        # check if the agent is placed at the right location
        self.assertTrue(space.locations[n.pos] == n)

if __name__ == '__main__':
    main()
