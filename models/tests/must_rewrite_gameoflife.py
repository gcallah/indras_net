from unittest import TestCase

from propargs.propargs import PropArgs

import models.gameoflife as g
from indra.composite import Composite
from indra.env import Env
from models.gameoflife import DEF_HEIGHT, DEF_WIDTH
from models.gameoflife import apply_live_rules, check_for_new_agents
from models.gameoflife import set_up, create_game_cell

TEST_X = 1
TEST_Y = 1


class GameOfLifeTestCase(TestCase):
    def setUp(self):
        self.pa = PropArgs.create_props('gameoflife_props',
                                        ds_file='props/gameoflife.props.json')
        (g.groups) = set_up()
        pass

    def tearDown(self):
        g.groups = None
        pass

    def test_create_agent(self):
        """
        Creates an agent and checks that it has the correct name,
        which is its (x, y) corrdinates.
        """
        agent = create_game_cell(TEST_X, TEST_Y)
        test_name = "(" + str(TEST_X) + "," + str(TEST_Y) + ")"
        self.assertEqual(agent.name, test_name)

    def test_apply_live_rules(self):
        """
        Creates three agents.
        All three agents are alive.
        Assign one agent to be a neighbor to another agent, 
        and check if apply_live_rules returns True.
        Add another agent to be their neighbors,
        and check if apply_live_rules returns False.
        """
        a = create_game_cell(TEST_X, TEST_Y)
        b = create_game_cell(TEST_X - 1, TEST_Y)
        c = create_game_cell(TEST_X + 1, TEST_Y)
        g.groups = []
        g.groups.append(Composite("black"))
        g.groups[0] += a
        g.groups[0] += b
        g.groups[0] += c
        neighbors = Composite("agent_neighbors")
        neighbors += b
        a.neighbors = neighbors
        self.assertEqual(apply_live_rules(a), True)
        # neighbors += c
        # a.neighbors = neighbors
        # self.assertEqual(apply_live_rules(a), False)

    def test_apply_dead_rules(self):
        """
        Creates three agents initially as neighbors and add it to a compsite, 
        and run that composite through apply_dead_rules_composite.
        It should return True because there are three neighbors.
        Add another agent to the composite and run it through apply_dead_rules_composite,
        which should return False as there are four neighbors.
        """
        pass

    def test_check_for_new_agents(self):
        """
        Create an agent and run it thorugh check_for_new_agent, which should return an empty list
        because there is only one agent in the enviornment.
        """
        a = create_game_cell(TEST_X, TEST_Y)
        g.gameoflife_env.place_member(a, xy=(TEST_X, TEST_Y))
        g.groups = []
        g.groups.append(Composite("black"))
        g.groups[0] += a
        self.assertEqual(check_for_new_agents(a), [])

    def test_populate_board_glider(self):
        black = Composite("black")
        g.groups = []
        g.groups.append(black)
        Env("Game of Life",
            action=g.gameoflife_action,
            height=DEF_HEIGHT,
            width=DEF_WIDTH,
            members=g.groups,
            random_placing=False)
        g.populate_board_glider(DEF_WIDTH, DEF_HEIGHT)
        self.assertEqual(len(g.gameoflife_env.members["black"]), 5)

    def test_populate_board_small_exploder(self):
        black = Composite("black")
        g.groups = []
        g.groups.append(black)
        g.gameoflife_env = Env("Game of Life",
                               action=g.gameoflife_action,
                               height=DEF_HEIGHT,
                               width=DEF_WIDTH,
                               members=g.groups,
                               random_placing=False)
        g.populate_board_small_exploder(DEF_WIDTH, DEF_HEIGHT)
        self.assertEqual(len(g.gameoflife_env.members["black"]), 7)

    def test_populate_board_exploder(self):
        black = Composite("black")
        g.groups = []
        g.groups.append(black)
        g.gameoflife_env = Env("Game of Life",
                               action=g.gameoflife_action,
                               height=DEF_HEIGHT,
                               width=DEF_WIDTH,
                               members=g.groups,
                               random_placing=False)
        g.populate_board_exploder(DEF_WIDTH, DEF_HEIGHT)
        self.assertEqual(len(g.gameoflife_env.members["black"]), 12)

    def test_populate_board_n_horizontal_row(self):
        black = Composite("black")
        g.groups = []
        g.groups.append(black)
        g.gameoflife_env = Env("Game of Life",
                               action=g.gameoflife_action,
                               height=DEF_HEIGHT,
                               width=DEF_WIDTH,
                               members=g.groups,
                               random_placing=False)
        g.populate_board_n_horizontal_row(DEF_WIDTH, DEF_HEIGHT)
        self.assertEqual(len(g.gameoflife_env.members["black"]), 9)

    def test_populate_board_n_vertical_row(self):
        black = Composite("black")
        g.groups = []
        g.groups.append(black)
        g.gameoflife_env = Env("Game of Life",
                               action=g.gameoflife_action,
                               height=DEF_HEIGHT,
                               width=DEF_WIDTH,
                               members=g.groups,
                               random_placing=False)
        g.populate_board_n_vertical_row(DEF_WIDTH, DEF_HEIGHT)
        self.assertEqual(len(g.gameoflife_env.members["black"]), 9)

    def test_populate_board_lightweight_spaceship(self):
        black = Composite("black")
        g.groups = []
        g.groups.append(black)
        g.gameoflife_env = Env("Game of Life",
                               action=g.gameoflife_action,
                               height=DEF_HEIGHT,
                               width=DEF_WIDTH,
                               members=g.groups,
                               random_placing=False)
        g.populate_board_lightweight_spaceship(DEF_WIDTH, DEF_HEIGHT)
        self.assertEqual(len(g.gameoflife_env.members["black"]), 9)

    def test_populate_board_tumbler(self):
        black = Composite("black")
        g.groups = []
        g.groups.append(black)
        g.gameoflife_env = Env("Game of Life",
                               action=g.gameoflife_action,
                               height=DEF_HEIGHT,
                               width=DEF_WIDTH,
                               members=g.groups,
                               random_placing=False)
        g.populate_board_tumbler(DEF_WIDTH, DEF_HEIGHT)
        self.assertEqual(len(g.gameoflife_env.members["black"]), 22)
