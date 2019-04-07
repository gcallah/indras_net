"""
This is the test suite for space.py.
"""

from unittest import TestCase, main

from indra.space import Space, distance, out_of_bounds
from indra.space import DEF_HEIGHT, DEF_WIDTH, DEF_MAX_MOVE
from indra.agent import Agent
from indra.tests.test_agent import create_newton, create_hardy, create_leibniz
from indra.tests.test_agent import create_ramanujan

REP_RAND_TESTS = 20


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

    def test_gen_new_pos(self):
        """
        Making sure new pos is within max_move of old pos.
        Since this test relies on random numbers, let's repeat it.
        """
        for i in range(REP_RAND_TESTS):
            # test with different max moves:
            max_move = (i // 2) + 1
            (old_x, old_y) = self.newton.get_pos()
            (new_x, new_y) = self.space.gen_new_pos(self.newton, max_move)
            if not abs(old_x - new_x) <= max_move:
                print("Failed test with ", old_x, " ", new_x)
            if not abs(old_y - new_y) <= max_move:
                print("Failed test with ", old_y, " ", new_y)
            self.assertTrue(abs(old_x - new_x) <= max_move)
            self.assertTrue(abs(old_y - new_y) <= max_move)

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
        x, y = self.space.rand_x(), self.space.rand_y()
        if (x, y) not in self.space.locations:
            self.newton.set_pos(self.space, x, y)
            self.space.add_location(x, y, self.newton)
            self.assertTrue(self.space.locations[self.newton.pos] ==
                            self.newton)

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

    def test_move(self):
        for i in range(REP_RAND_TESTS):
            print("Looping in test_move")
            # test with different max moves:
            max_move = (i // 2) + 1
            (old_x, old_y) = (self.newton.get_x(), self.newton.get_y())
            self.newton.move(max_move)
            (new_x, new_y) = (self.newton.get_x(), self.newton.get_y())
            if not abs(old_x - new_x) <= max_move:
                print("Failed x test with ", old_x, " ", new_x, " ", max_move)
            if not abs(old_y - new_y) <= max_move:
                print("Failed y test with ", old_y, " ", new_y, " ", max_move)
            self.assertTrue(abs(new_x - old_x) <= max_move)
            self.assertTrue(abs(new_y - old_y) <= max_move)

if __name__ == '__main__':
    main()
