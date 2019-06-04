from unittest import TestCase, main
from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env
from models.sandpile import set_up, create_agent
from models.sandpile import env_unfavorable, SAND_PREFIX

TEST_ANUM = 999999

REP_RAND_TESTS = 20

SMALL_GRID = 4

class SandpileTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_env_unfavorable(self):
        env_unfav = env_unfavorable(6)
        self.assertEqual(env_unfav, True)

        env_unfav = env_unfavorable(4)
        self.assertEqual(env_unfav, False)

    def test_create_agent(self):
        agent = create_agent(TEST_ANUM)
        self.assertEqual(agent.name, SAND_PREFIX + str(TEST_ANUM))
