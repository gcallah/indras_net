from unittest import TestCase, main
from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env
from models.sandpile import main, create_agent, add_grain, topple, switch_groups, env_unfavorable, get_next_group
from models.sandpile import change_color
from models.sandpile import SAND_PREFIX, sandpile, group2

TEST_ANUM = 999999

REP_RAND_TESTS = 20

SMALL_GRID = 4

class SandpileTestCase(TestCase):
    def setUp(self):
        main()

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
        agent = create_agent(TEST_ANUM)
        sandpile.members[0] += agent
        change_color(agent, sandpile, group2)
        self.assertEqual(agent.primary_group(), group2)


    def test_switch_groups(self):
        agent = create_agent(TEST_ANUM)
        sandpile.members[0] += agent
        for i in range(1,len(sandpile.members)):
            switch_groups(agent, sandpile, sandpile.members[i])
            self.assertEqual(str((agent.primary_group()))[5], i)


    def test_get_next_group(self):
        agent = create_agent(TEST_ANUM)
        sandpile.members[0] += agent
        next_group = get_next_group(agent)
        self.assertEqual(str(next_group)[5], 1)


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



