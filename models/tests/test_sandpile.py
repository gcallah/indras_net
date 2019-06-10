from unittest import TestCase, main
from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env
from models.sandpile import set_up, create_agent, next_group, topple
from models.sandpile import NUM_GROUPS, SAND_PREFIX

TEST_ANUM = 999999

REP_RAND_TESTS = 20

SMALL_GRID = 4

class SandpileTestCase(TestCase):
    def setUp(self):
        set_up()
        self.test_agent = create_agent(TEST_ANUM)
        pass

    def tearDown(self):
        self.test_agent = None
        pass

    def test_create_agent(self):
        agent = create_agent(TEST_ANUM)
        self.assertEqual(agent.name, SAND_PREFIX + str(TEST_ANUM))

    def test_next_group(self):
        """
        Test to make sure next_group() return is always in range.
        """
        for i in range(NUM_GROUPS * 3):
            self.assertTrue(next_group(i) < NUM_GROUPS)
            self.assertTrue(next_group(i) >= 0)
