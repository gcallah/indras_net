from unittest import TestCase, main
from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env
from models.gameoflife import create_agent, set_up
from models.gameoflife import change_color, apply_live_rules, apply_dead_rules, gameoflife_action, agent_action, populate_board
import models.gameoflife as g

TEST_ANUM = 999999

gameoflife_env = None

class GameOfLifeTestCase(TestCase):
    def setUp(self):
        (g.groups, g.gameoflife_env) = set_up()
        pass

    def tearDown(self):
        g.gameoflife_env = None
        g.groups = None
        pass

    def test_create_agent(self):
        agent = create_agent(TEST_ANUM, TEST_ANUM)
        test_name = "(" + str(TEST_ANUM) + "," + str(TEST_ANUM) + ")"
        self.assertEqual(agent.name, test_name)

    def test_change_color(self):
        agent = create_agent(TEST_ANUM, TEST_ANUM)
        g.groups =[]
        g.groups.append(Composite("black"))
        g.groups.append(Composite("white"))
        g.groups[0] += agent
        change_color(g.gameoflife_env, agent)
        self.assertEqual(agent.primary_group(), g.groups[1])

    def test_apply_live_rules(self):
        a = create_agent(TEST_ANUM, TEST_ANUM)
        b = create_agent(TEST_ANUM - 1, TEST_ANUM)
        c = create_agent(TEST_ANUM + 1, TEST_ANUM)
        g.groups =[]
        g.groups.append(Composite("black"))
        g.groups.append(Composite("white"))
        g.groups[1] += a
        g.groups[1] += b
        g.groups[1] += c
        neighbors = []
        neighbors.append(b)
        a.neighbors = neighbors
        self.assertEqual(apply_live_rules(g.gameoflife_env, a), True)
        neighbors.append(c)
        a.neighbors = neighbors
        self.assertEqual(apply_live_rules(g.gameoflife_env, a), False)

    def test_apply_dead_rules(self):
        a = create_agent(TEST_ANUM, TEST_ANUM)
        b = create_agent(TEST_ANUM - 1, TEST_ANUM)
        c = create_agent(TEST_ANUM + 1, TEST_ANUM)
        d = create_agent(TEST_ANUM, TEST_ANUM + 1)
        g.groups =[]
        g.groups.append(Composite("black"))
        g.groups.append(Composite("white"))
        g.groups[0] += a
        g.groups[1] += b
        g.groups[1] += c
        g.groups[1] += d
        neighbors = []
        neighbors.append(b)
        neighbors.append(c)
        a.neighbors = neighbors
        self.assertEqual(apply_dead_rules(g.gameoflife_env, a), False)
        neighbors.append(d)
        a.neighbors = neighbors
        self.assertEqual(apply_dead_rules(g.gameoflife_env, a), True)









