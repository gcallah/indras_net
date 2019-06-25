from unittest import TestCase, main
from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env
from models.sandpile import set_up, create_agent, get_next_group_idx
from models.sandpile import topple, get_curr_group_idx, change_group, place_action
from models.sandpile import NUM_GROUPS, SAND_PREFIX
import models.sandpile as sp

TEST_ANUM = 999999

REP_RAND_TESTS = 20

SMALL_GRID = 4

sandpile = None

class SandpileTestCase(TestCase):
    def setUp(self):
        # (sp.groups, sp.group_indices, sp.sandpile) = set_up()
        self.test_agent = create_agent(TEST_ANUM, TEST_ANUM)
        pass

    def tearDown(self):
        self.test_agent = None
        sp.groups = None
        sp.group_indices = None
        sp.sandpile = None
        pass

    def test_create_agent(self):
        agent = create_agent(TEST_ANUM, TEST_ANUM)
        test_name = "(" + str(TEST_ANUM) + "," + str(TEST_ANUM) + ")"
        self.assertEqual(agent.name, test_name)

    def test_get_curr_group_idx(self):
        a = create_agent(TEST_ANUM, TEST_ANUM)
        # groups = []
        # groups.append(Composite("Group" + str(0)))
        # groups[0]+= a
        # self.assertEqual(get_curr_group_idx(a), 0)

    def test_get_next_group_idx(self):
        a = create_agent(TEST_ANUM, TEST_ANUM)
        self.assertEqual(get_next_group_idx(0), 1)

#    def test_change_group(self):
#        a = create_agent(TEST_ANUM, TEST_ANUM)
#        groups = []
#        groups.append(Composite("Group" + str(0)))
#        groups.append(Composite("Group" + str(1)))
#        groups[0] += a
#        change_group(a, sandpile, 0, 1)
#        self.assertEqual(get_curr_group_idx(a), 1)

    def test_place_action(self):
#        a = agent at 0,0
#        place_action(a)
#        self.assertNotEqual(agent.neighbors, None)
        pass

    def test_next_group(self):
        """
        Test to make sure next_group() return is always in range.
        """
        for i in range(NUM_GROUPS * 3):
            self.assertTrue(get_next_group_idx(i) < NUM_GROUPS)
            self.assertTrue(get_next_group_idx(i) >= 0)
