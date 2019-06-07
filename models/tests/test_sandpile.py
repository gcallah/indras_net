from unittest import TestCase, main
from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env
from models.sandpile import set_up, create_agent, add_grain, topple
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

    def test_change_color(self):
        ...

    def test_get_next_group(self):
        ...

    def test_add_grain(self):
        agent = create_agent(TEST_ANUM)
        init_amt = agent['grains']
        add_grain(agent)
        self.assertEqual(agent['grains'], init_amt + 1)

    def test_place_action(self):
        pass

    def test_sandpile_action(self):
        ...

    def test_topple(self):
        agent = create_agent(TEST_ANUM)
        topple(agent)
        self.assertEqual(agent['grains'], 0)



