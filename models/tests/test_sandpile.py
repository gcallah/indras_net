from unittest import TestCase

import models.sandpile as sp
from indra.composite import Composite
from models.sandpile import set_up, create_grain, add_grain, topple, \
    sandpile_action

TEST_X = 1
TEST_Y = 1

REP_RAND_TESTS = 20

SMALL_GRID = 4

sandpile = None


class SandpileTestCase(TestCase):
    def setUp(self):
        (sp.sandpile, sp.groups, sp.group_indices) = set_up()

    def tearDown(self):
        self.test_agent = None
        sp.groups = None
        sp.group_indices = None
        sp.sandpile = None

    def test_create_agent(self):
        """
        Creates an agent and checks that it has the correct name,
        which is its (x, y) corrdinates.
        """
        agent = create_grain(TEST_X, TEST_Y)
        test_name = "(" + str(TEST_X) + "," + str(TEST_Y) + ")"
        self.assertEqual(agent.name, test_name)

    def test_add_grain(self):
        """
        Creates an agent, assign it to Group0,
        and checks if add_grain changed the agent to Group1.
        """
        a = create_grain(TEST_X, TEST_Y)
        sp.groups = []
        sp.groups.append(Composite("Group" + str(0)))
        sp.groups.append(Composite("Group" + str(1)))
        sp.groups[0] += a
        add_grain(a)
        self.assertEqual(a.primary_group(), sp.groups[1])

    def test_topple(self):
        """
        Creates two agents in Group0 and one in Group1
        topples the agent in Group1
        which should topple and spill over to the two agents in Group0.
        Checks that the neighbors have grains added to them.
        """
        a = create_grain(TEST_X, TEST_Y)
        b = create_grain(TEST_X - 1, TEST_Y)
        c = create_grain(TEST_X + 1, TEST_Y)
        sp.groups = []
        sp.groups.append(Composite("Group" + str(0)))
        sp.groups.append(Composite("Group" + str(1)))
        sp.groups[0] += b
        sp.groups[0] += c
        sp.groups[1] += a
        neighbors = Composite("agent_neighbors")
        neighbors += b
        neighbors += c
        a.neighbors = neighbors
        topple(a)
        self.assertEqual(a.primary_group(), sp.groups[1])
        self.assertEqual(b.primary_group(), sp.groups[1])
        self.assertEqual(c.primary_group(), sp.groups[1])

    def test_sandpile_action(self):
        """
        Checks that the agent in the center changes groups
        """
        self.assertEqual(sp.sandpile.attrs["center_agent"].primary_group(),
                         sp.groups[0])
        sandpile_action(sp.sandpile)
        self.assertEqual(sp.sandpile.attrs["center_agent"].primary_group(),
                         sp.groups[1])
