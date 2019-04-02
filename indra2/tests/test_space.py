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

        space = Space("test space")
        n = create_newton()
        space += n
        self.assertTrue(Space.locations[n.pos] == n)

    def test_add_location(self):

        n_add = create_newton()
        x, y = self.rand_x(), self.rand_y()
        if (x, y) not in self.locations:
            n_add.set_pos(x, y)
            self.add_location(x, y, n_add)
        self.assertTrue(Space.locations[n_add.pos] == n_add)

    def test_move_location(self):
        n = create_newton()
        x0, y0 = self.rand_x(), self.rand_y()
        n.set_pos(x0, y0)
        x, y = self.rand_x(), self.rand_y()
        self.move_location(n, x0, y0, x, y)
        self.assertTrue(Space.locations[(x, y)] == n)

    def test_remove_location(self):

        n = create_newton()
        x, y = self.rand_x(), self.rand_y()
        n.set_pos(x, y)
        self.remove_location(x, y)
        self.assertTrue(Space.locations[(x, y)] != n)


if __name__ == '__main__':
    main()
