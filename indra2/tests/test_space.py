"""
This is the test suite for space.py.
"""

from unittest import TestCase, main

from indra2.space import Space, distance, out_of_bounds
from indra2.space import DEF_HEIGHT, DEF_WIDTH
from indra2.agent import Agent
from indra2.tests.test_agent import create_newton, create_hardy, create_leibniz
from indra2.tests.test_agent import create_ramanujan


def create_space():
    space = Space("test space")
    newton = create_newton()
    space += newton
    space += create_hardy()
    space += create_leibniz()
    return (space, newton)

def create_teeny_space():
    """
    This space should be full!
    """
    space = Space("test space", 2, 2)
    space += create_newton()
    space += create_hardy()
    space += create_leibniz()
    space += create_ramanujan()
    return space

class SpaceTestCase(TestCase):
    def setUp(self):
        (self.space, self.newton) = create_space()
        self.teeny_space = create_teeny_space()

    def tearDown(self):
        self.space = None
        self.teeny_space = None

    def test_constrain_x(self):
        """
        Test keeping x in bounds.
        """
        self.assertEqual(self.space.constrain_x(-10), 0)
        self.assertEqual(self.space.constrain_x(DEF_WIDTH * 2), DEF_WIDTH - 1)

    def test_constrain_y(self):
        """
        Test keeping y in bounds.
        """
        self.assertEqual(self.space.constrain_y(-10), 0)
        self.assertEqual(self.space.constrain_x(DEF_HEIGHT * 2),
                         DEF_HEIGHT - 1)

    def test_grid_size(self):
        """
        Make sure we calc grid size properly.
        """
        self.assertEqual(self.space.grid_size(), DEF_HEIGHT * DEF_WIDTH)

    def test_is_full(self):
        """
        See if the grid is full.
        """
        self.assertFalse(self.space.is_full())
        self.assertTrue(self.teeny_space.is_full())

    def test_place_members(self):
        """
        Test place_members() by making sure all agents have a pos
        when done.
        """
        for agent in self.space:
            self.assertTrue(self.space[agent].islocated())

    def test_rand_x(self):
        """
        Make sure randomly generated X pos is within grid.
        If constrained, make sure it is within constraints.
        """
        x = self.space.rand_x()
        self.assertTrue(x >= 0)
        self.assertTrue(x < self.space.width)
        x2 = self.space.rand_x(low=4, high=8)
        self.assertTrue(x2 >= 4)
        self.assertTrue(x2 <= 8)

    def test_rand_y(self):
        """
        Make sure randomly generated Y pos is within grid.
        """
        y = self.space.rand_y()
        self.assertTrue(y >= 0)
        self.assertTrue(y < self.space.height)
        y2 = self.space.rand_y(low=4, high=8)
        self.assertTrue(y2 >= 4)
        self.assertTrue(y2 <= 8)

    def test_location(self):
        """
        Test that an added agent has a location.
        """
        n = create_newton()
        self.space += n
        self.assertTrue(self.space.locations[n.pos] == n)

    def test_add_location(self):
        """
        Can we add an agent to a location?
        """
        n_add = create_newton()
        x, y = self.space.rand_x(), self.space.rand_y()
        if (x, y) not in self.space.locations:
            n_add.set_pos(x, y)
            self.space.add_location(x, y, n_add)
        self.assertTrue(self.space.locations[n_add.pos] == n_add)

    def test_move_location(self):
        """
        Can we move agent from one location to another?
        """
        x, y = self.space.rand_x(), self.space.rand_y()
        self.space.move_location(x, y, self.newton.get_x(), self.newton.get_y())
        self.assertTrue(self.space.locations[(x, y)] == self.newton)

    def test_remove_location(self):
        """
        Test removing location from locations.
        """
        (x, y) = (self.newton.get_x(), self.newton.get_y())
        self.space.remove_location(x, y)
        self.assertTrue((x, y) not in self.space.locations)


if __name__ == '__main__':
    main()
