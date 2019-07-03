from unittest import TestCase, main
from indra.agent import Agent
from indra.composite import Composite
from indra.space import Space
from indra.env import Env
from models.gameoflife import create_agent, set_up
from models.gameoflife import change_color, apply_live_rules, apply_dead_rules, gameoflife_action, agent_action
from models.gameoflife import populate_board_glider
import models.gameoflife as g

TEST_X = 1
TEST_Y = 1

class GameOfLifeTestCase(TestCase):
    def setUp(self):
        (g.gameoflife_env, g.groups) = set_up()
        pass

    def tearDown(self):
        g.gameoflife_env = None
        g.groups = None
        pass

    def test_create_agent(self):
        agent = create_agent(TEST_X, TEST_Y)
        test_name = "(" + str(TEST_X) + "," + str(TEST_Y) + ")"
        self.assertEqual(agent.name, test_name)

    def test_change_color(self):
        # agent = create_agent(TEST_X, TEST_Y)
        # groups = []
        # groups.append(Composite("white"))
        # groups.append(Composite("black"))
        # g.groups[0] += agent
        g.change_color(g.gameoflife_env.get_agent_at(0, 0))
        self.assertEqual((g.gameoflife_env.get_agent_at(0, 0)).primary_group(), g.groups[1])
        g.change_color(g.gameoflife_env.get_agent_at(0, 0))

    def test_apply_live_rules(self):
        a = create_agent(TEST_X, TEST_Y)
        b = create_agent(TEST_X - 1, TEST_Y)
        c = create_agent(TEST_X + 1, TEST_Y)
        g.groups = []
        g.groups.append(Composite("white"))
        g.groups.append(Composite("black"))
        g.groups[1] += a
        g.groups[1] += b
        g.groups[1] += c
        neighbors = Composite("agent_neighbors")
        neighbors += b
        a.neighbors = neighbors
        self.assertEqual(apply_live_rules(a), True)
        neighbors += c
        a.neighbors = neighbors
        self.assertEqual(apply_live_rules(a), False)

    def test_apply_dead_rules(self):
        a = create_agent(TEST_X, TEST_Y)
        b = create_agent(TEST_X - 1, TEST_Y)
        c = create_agent(TEST_X + 1, TEST_Y)
        d = create_agent(TEST_X, TEST_Y + 1)
        g.groups = []
        g.groups.append(Composite("white"))
        g.groups.append(Composite("black"))
        g.groups[0] += a
        g.groups[1] += b
        g.groups[1] += c
        g.groups[1] += d
        neighbors = Composite("agent_neighbors")
        neighbors += b
        neighbors += c
        a.neighbors = neighbors
        self.assertEqual(apply_dead_rules(a), False)
        neighbors += d
        a.neighbors = neighbors
        self.assertEqual(apply_dead_rules(a), True)

    def test_gameoflife_action(self):
        a = create_agent(TEST_X, TEST_Y)
        b = create_agent(TEST_X - 1, TEST_Y)
        c = create_agent(TEST_X + 1, TEST_Y)
        d = create_agent(TEST_X, TEST_Y + 1)
        g.groups = []
        g.groups.append(Composite("white"))
        g.groups.append(Composite("black"))
        g.groups[0] += a
        g.groups[1] += b
        g.groups[1] += c
        g.groups[1] += d
        neighbors_composite = Composite("neighbors_composite")
        neighbors_composite += b
        neighbors_composite += c
        neighbors_composite += d
        a.neighbors = neighbors_composite
        gameoflife_action()
        # self.assertEqual(a.primary_group(), g.groups[1])
        # fix to check the colors
        self.assertEqual(len(a.neighbors), 3)

    # def test_agent_action(self):
    #     a = create_agent(TEST_X, TEST_Y)
    #     b = create_agent(TEST_X - 1, TEST_Y)
    #     c = create_agent(TEST_X + 1, TEST_Y)
    #     d = create_agent(TEST_X, TEST_Y + 1)
    #     g.groups = []
    #     g.groups.append(Composite("Group" + str(0)))
    #     g.groups += a
    #     g.groups += b
    #     g.groups += c
    #     g.groups += d
    #     neighbors = Composite("neighbors")
    #     neighbors += b
    #     neighbors += c
    #     neighbors += d
    #     g.gameoflife_env = Env("gameoflife", members = g.groups)
    #     agent_action(a)
    #     for i in a.neighbors:
    #     assertEqual(a.neighbors, neighbors)

    # def test_populate_board_glider(self):
    #     #self.assertEqual((g.gameoflife_env.get_agent_at(15, 15)).primary_group(), g.groups[0])
    #     #self.assertEqual((g.gameoflife_env.get_agent_at(14, 16)).primary_group(), g.groups[0])
    #     #self.assertEqual((g.gameoflife_env.get_agent_at(15, 14)).primary_group(), g.groups[0])
    #     g.populate_board_glider(30, 30)
    #     #self.assertEqual((g.gameoflife_env.get_agent_at(15, 15)).primary_group(), g.groups[1])
    #     #self.assertEqual((g.gameoflife_env.get_agent_at(14, 16)).primary_group(), g.groups[1])
    #     self.assertEqual((g.gameoflife_env.get_agent_at(15, 14)).primary_group(), g.groups[1])









