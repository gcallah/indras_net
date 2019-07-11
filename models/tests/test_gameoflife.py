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
        """
        Creates an agent and checks that it has the correct name,
        which is its (x, y) corrdinates.
        """
        agent = create_agent(TEST_X, TEST_Y)
        test_name = "(" + str(TEST_X) + "," + str(TEST_Y) + ")"
        self.assertEqual(agent.name, test_name)

    def test_change_color(self):
        """
        Changes a color of a white agent using change_color method
        and checks that it is black.
        Also changes it back to white and checks if it did.
        """
        g.change_color(g.gameoflife_env.get_agent_at(0, 0))
        self.assertEqual((g.gameoflife_env.get_agent_at(0, 0)).primary_group(), g.groups[1])
        g.change_color(g.gameoflife_env.get_agent_at(0, 0))
        self.assertEqual((g.gameoflife_env.get_agent_at(0, 0)).primary_group(), g.groups[0])

    def test_apply_live_rules(self):
        """
        Creates three agents.
        All three agents are alive.
        Assign one agent to be a neighbor to another agent, 
        and check if apply_live_rules returns True.
        Add another agent to be their neighbors,
        and check if apply_live_rules returns False.
        """
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
        """
        Creates four agents.
        Three agents are alive while the other is dead.
        Assign two live agents to be neighbors to the dead agent, 
        and check if apply_dead_rules returns False.
        Add another agent to be their neighbors,
        and check if apply_dead_rules returns True.
        """
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
