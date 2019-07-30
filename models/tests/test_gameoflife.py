from unittest import TestCase, main
from propargs.propargs import PropArgs
from indra.agent import Agent
from indra.composite import Composite
from indra.space import Space
from indra.env import Env
from models.gameoflife import set_up, create_agent, apply_live_rules, apply_dead_rules_composite
from models.gameoflife import check_for_new_agents, gameoflife_action, agent_action
from models.gameoflife import populate_board_glider, populate_board_exploder, populate_board_small_exploder
from models.gameoflife import populate_board_n_horizontal_row, populate_board_n_vertical_row
from models.gameoflife import populate_board_lightweight_spaceship, populate_board_tumbler
import models.gameoflife as g

TEST_X = 1
TEST_Y = 1

class GameOfLifeTestCase(TestCase):
    def setUp(self):
        self.pa = PropArgs.create_props('gameoflife_props',
                                        ds_file='props/gameoflife.props.json')
        (g.gameoflife_env, g.groups) = set_up()
        print()
        pass

    def tearDown(self):
        g.gameoflife_env = None
        g.groups = None
        pass

    def test_create_agent(self):
        """
        Creates an agent and checks that it has the correct name,
        which is its (x, y) corrdinates.
        """
        agent = create_agent(TEST_X, TEST_Y)
        test_name = "(" + str(TEST_X) + "," + str(TEST_Y) + ")"
        self.assertEqual(agent.name, test_name)

    def test_populate_board_glider(self):
        pass
        # white = Composite("white")
        # black = Composite("black")
        # g.groups = []
        # g.groups.append(white)
        # g.groups.append(black)
        # for y in range(DEF_HEIGHT):
        #         for x in range(DEF_WIDTH):
        #                 g.groups[0] += create_agent(x, y)
        # g.gameoflife_env=Env("Game of Life",
        #                  action=g.gameoflife_action,
        #                  height=DEF_HEIGHT,
        #                  width=DEF_WIDTH,
        #                  members=g.groups,
        #                  random_placing=False)
        # g.populate_board_glider(DEF_WIDTH, DEF_HEIGHT)
        # self.assertEqual(len(g.gameoflife_env.members["black"]),5)

    def test_populate_board_small_exploder(self):
        pass
        # white = Composite("white")
        # black = Composite("black")
        # g.groups = []
        # g.groups.append(white)
        # g.groups.append(black)
        # for y in range(DEF_HEIGHT):
        #         for x in range(DEF_WIDTH):
        #                 g.groups[0] += create_agent(x, y)
        # g.gameoflife_env=Env("Game of Life",
        #                  action=g.gameoflife_action,
        #                  height=DEF_HEIGHT,
        #                  width=DEF_WIDTH,
        #                  members=g.groups,
        #                  random_placing=False)
        # g.populate_board_small_exploder(DEF_WIDTH, DEF_HEIGHT)
        # self.assertEqual(len(g.gameoflife_env.members["black"]),7)

    def test_populate_board_exploder (self):
        pass
        # white = Composite("white")
        # black = Composite("black")
        # g.groups = []
        # g.groups.append(white)
        # g.groups.append(black)
        # for y in range(DEF_HEIGHT):
        #         for x in range(DEF_WIDTH):
        #                 g.groups[0] += create_agent(x, y)
        # g.gameoflife_env=Env("Game of Life",
        #                  action=g.gameoflife_action,
        #                  height=DEF_HEIGHT,
        #                  width=DEF_WIDTH,
        #                  members=g.groups,
        #                  random_placing=False)
        # g.populate_board_exploder(DEF_WIDTH, DEF_HEIGHT)
        # self.assertEqual(len(g.gameoflife_env.members["black"]),12)

    def test_populate_board_n_horizontal_row(self):
        pass
        # white = Composite("white")
        # black = Composite("black")
        # g.groups = []
        # g.groups.append(white)
        # g.groups.append(black)
        # for y in range(DEF_HEIGHT):
        #         for x in range(DEF_WIDTH):
        #                 g.groups[0] += create_agent(x, y)
        # g.gameoflife_env=Env("Game of Life",
        #                  action=g.gameoflife_action,
        #                  height=DEF_HEIGHT,
        #                  width=DEF_WIDTH,
        #                  members=g.groups,
        #                  random_placing=False)
        # g.populate_board_n_horizontal_row(DEF_WIDTH, DEF_HEIGHT)
        # self.assertEqual(len(g.gameoflife_env.members["black"]),9)

    def test_populate_board_n_vertical_row(self):
        pass
        # white = Composite("white")
        # black = Composite("black")
        # g.groups = []
        # g.groups.append(white)
        # g.groups.append(black)
        # for y in range(DEF_HEIGHT):
        #         for x in range(DEF_WIDTH):
        #                 g.groups[0] += create_agent(x, y)
        # g.gameoflife_env=Env("Game of Life",
        #                  action=g.gameoflife_action,
        #                  height=DEF_HEIGHT,
        #                  width=DEF_WIDTH,
        #                  members=g.groups,
        #                  random_placing=False)
        # g.populate_board_n_vertical_row(DEF_WIDTH, DEF_HEIGHT)
        # self.assertEqual(len(g.gameoflife_env.members["black"]),9)

    def test_populate_board_lightweight_spaceship(self):
        pass
        # white = Composite("white")
        # black = Composite("black")
        # g.groups = []
        # g.groups.append(white)
        # g.groups.append(black)
        # for y in range(DEF_HEIGHT):
        #         for x in range(DEF_WIDTH):
        #                 g.groups[0] += create_agent(x, y)
        # g.gameoflife_env=Env("Game of Life",
        #                  action=g.gameoflife_action,
        #                  height=DEF_HEIGHT,
        #                  width=DEF_WIDTH,
        #                  members=g.groups,
        #                  random_placing=False)
        # g.populate_board_lightweight_spaceship(DEF_WIDTH, DEF_HEIGHT)
        # self.assertEqual(len(g.gameoflife_env.members["black"]),9)

    def test_populate_board_tumbler(self):
        pass
        # white = Composite("white")
        # black = Composite("black")
        # g.groups = []
        # g.groups.append(white)
        # g.groups.append(black)
        # for y in range(DEF_HEIGHT):
        #         for x in range(DEF_WIDTH):
        #                 g.groups[0] += create_agent(x, y)
        # g.gameoflife_env=Env("Game of Life",
        #                  action=g.gameoflife_action,
        #                  height=DEF_HEIGHT,
        #                  width=DEF_WIDTH,
        #                  members=g.groups,
        #                  random_placing=False)
        # g.populate_board_tumbler(DEF_WIDTH, DEF_HEIGHT)
        # self.assertEqual(len(g.gameoflife_env.members["black"]),22)
         
    def test_apply_live_rules(self):
        pass
        """
        Creates three agents.
        All three agents are alive.
        Assign one agent to be a neighbor to another agent, 
        and check if apply_live_rules returns True.
        Add another agent to be their neighbors,
        and check if apply_live_rules returns False.
        """
        # a = create_agent(TEST_X, TEST_Y)
        # b = create_agent(TEST_X - 1, TEST_Y)
        # c = create_agent(TEST_X + 1, TEST_Y)
        # g.groups = []
        # g.groups.append(Composite("white"))
        # g.groups.append(Composite("black"))
        # g.groups[1] += a
        # g.groups[1] += b
        # g.groups[1] += c
        # neighbors = Composite("agent_neighbors")
        # neighbors += b
        # a.neighbors = neighbors
        # self.assertEqual(apply_live_rules(a), True)
        # neighbors += c
        # a.neighbors = neighbors
        # self.assertEqual(apply_live_rules(a), False)

    def test_apply_dead_rules(self):
        pass
        """
        Creates four agents.
        Three agents are alive while the other is dead.
        Assign two live agents to be neighbors to the dead agent, 
        and check if apply_dead_rules returns False.
        Add another agent to be their neighbors,
        and check if apply_dead_rules returns True.
        """
        # a = create_agent(TEST_X, TEST_Y)
        # b = create_agent(TEST_X - 1, TEST_Y)
        # c = create_agent(TEST_X + 1, TEST_Y)
        # d = create_agent(TEST_X, TEST_Y + 1)
        # g.groups = []
        # g.groups.append(Composite("white"))
        # g.groups.append(Composite("black"))
        # g.groups[0] += a
        # g.groups[1] += b
        # g.groups[1] += c
        # g.groups[1] += d
        # neighbors = Composite("agent_neighbors")
        # neighbors += b
        # neighbors += c
        # a.neighbors = neighbors
        # self.assertEqual(apply_dead_rules(a), False)
        # neighbors += d
        # a.neighbors = neighbors
        # self.assertEqual(apply_dead_rules(a), True)
