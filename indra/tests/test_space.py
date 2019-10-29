"""
This is the test suite for space.py.
"""

from unittest import TestCase, main, skip

from indra.agent import Agent
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.space import Space, distance
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
        self.test_agent = Agent("test agent")
        self.test_agent2 = Agent("test agent 2")
        self.test_agent3 = Agent("test agent 3")
        self.test_agent4 = Agent("test agent 4")

    def tearDown(self):
        self.space = None
        self.teeny_space = None
        self.test_agent = None
        self.test_agent2 = None
        self.test_agent3 = None
        self.test_agent4 = None

    def test_get_closest_agent(self):
        closest = self.space.get_closest_agent(self.newton)
        self.assertTrue(distance(self.newton, closest) <=
                        self.space.get_max_distance())

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

    def test_rand_place_members(self):
        """
        Test rand_place_members() by making sure all agents have a pos
        when done.
        """
        for agent in self.space:
            self.assertTrue(self.space[agent].is_located())

    def test_place_member_xy(self):
        """
        Test placing an agent at a particular x, y spot.
        We will run this DEF_HEIGHT times, to test multiple
        possible placements.
        """
        space = Space("test space")
        for i in range(DEF_HEIGHT):
            spot = space.place_member(mbr=self.test_agent, xy=(i, i))
            if spot is not None:
                # the print output will usually be captured by nose,
                # but that can be turned off with --nocapture.
                (x, y) = (self.test_agent.get_x(),
                          self.test_agent.get_y())
                self.assertEqual((x, y), (i, i))

    def test_get_agent_at(self):
        """
        Test getting an agent from some locale.
        """
        space = Space("test space")
        # before adding agent, all cells are empty:
        self.assertEqual(space.get_agent_at(1, 1), None)
        for i in range(DEF_HEIGHT):
            spot = space.place_member(mbr=self.test_agent, xy=(i, i))
            whos_there = space.get_agent_at(i, i)
            self.assertEqual(whos_there, self.test_agent)

    def test_rand_x(self):
        """
        Make sure randomly generated X pos is within grid.
        If constrained, make sure it is within constraints.
        """
        x = self.space.rand_x()
        self.assertTrue(x >= 0)
        self.assertTrue(x <= self.space.width)
        x2 = self.space.rand_x(low=4, high=8)
        self.assertTrue(x2 >= 4)
        self.assertTrue(x2 <= 8)

    def test_rand_y(self):
        """
        Make sure randomly generated Y pos is within grid.
        """
        y = self.space.rand_y()
        self.assertTrue(y >= 0)
        self.assertTrue(y <= self.space.height)
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
        for i in range(REP_RAND_TESTS):
            #test with different random positions
            x, y = self.space.rand_x(), self.space.rand_y()
            if (x, y) not in self.space.locations:
                self.newton.set_pos(self.space, x, y)
                self.space.add_location(x, y, self.newton)
                self.assertTrue(self.space.locations[self.newton.pos] ==
                                self.newton)

    # def test_move_location(self):
    #     """
    #     Can we move agent from one location to another?
    #     This test sometimes fails: we need to explore!
    #     """
    #     for i in range(REP_RAND_TESTS):
            #test with different random positions
            # print("Trying a new location: ", i, "th iteration")
            # print("Previous newton is at ", self.newton.get_x(), self.newton.get_y())
            # x, y = self.space.rand_x(), self.space.rand_y()
            # print("new x, y = ", x, y)
            # self.space.move_location(x, y, self.newton.get_x(), self.newton.get_y())
            # print("Now newton is at ", self.newton.get_x(), self.newton.get_y())
            # self.assertTrue(self.space.locations[(x, y)] == self.newton)

    def test_remove_location(self):
        """
        Test removing location from locations.
        """
        (x, y) = (self.newton.get_x(), self.newton.get_y())
        self.space.remove_location(x, y)
        self.assertTrue((x, y) not in self.space.locations)

    def test_move(self):
        """
        Test whether moving an agent stays within its max move.
        """
        for i in range(REP_RAND_TESTS):
            # test with different max moves:
            max_move = (i // 2) + 1
            (old_x, old_y) = (self.newton.get_x(), self.newton.get_y())
            self.newton.move(max_move)
            (new_x, new_y) = (self.newton.get_x(), self.newton.get_y())
            self.assertTrue(abs(new_x - old_x) <= max_move)
            self.assertTrue(abs(new_y - old_y) <= max_move)

    def test_is_empty(self):
        """
        Is cell empty?
        """
        (x, y) = (self.newton.get_x(), self.newton.get_y())
        self.assertFalse(self.space.is_empty(x, y))

    @skip("Skipping von neumann test")
    def test_get_vonneumann_hood(self):
        """
        Get von Neumann neighborhood.
        """
        space = Space("test space")
        space += self.test_agent
        space += self.test_agent2
        space += self.test_agent3
        space += self.test_agent4

        for i in range(REP_RAND_TESTS):
            print("Looping in von Neumann")

            space.place_member(mbr=self.test_agent, xy=(0, 0))
            space.place_member(mbr=self.test_agent2, xy=(0, 1))
            hood = space.get_vonneumann_hood(self.test_agent)
            self.assertTrue(self.test_agent2.name in hood)

            space.place_member(mbr=self.test_agent3, xy=(1, 0))
            hood = space.get_vonneumann_hood(self.test_agent)
            self.assertTrue(self.test_agent3.name in hood)

            space.place_member(mbr=self.test_agent4, xy=(0, DEF_HEIGHT))
            hood = space.get_vonneumann_hood(self.test_agent)
            self.assertTrue(self.test_agent4.name not in hood)


if __name__ == '__main__':
    main()
