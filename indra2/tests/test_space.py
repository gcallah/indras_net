"""
This is the test suite for agent.py.
"""

from unittest import TestCase, main

from indra2.space import Space


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


if __name__ == '__main__':
    main()
