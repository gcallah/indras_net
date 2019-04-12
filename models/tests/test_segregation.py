"""
This is the test suite for space.py.
"""

from unittest import TestCase, main
from indra.agent import Agent
from models.segregation import set_up, create_agent, RED, BLUE
from models.segregation import env_unfavorable, agent_action
from models.segregation import group_names, agent_action
import models.segregation as seg

TEST_ANUM = 999999


class SegregationTestCase(TestCase):
    def setUp(self):
        (seg.blue_agents, seg.red_agents, seg.city) = set_up()

    def tearDown(self):
        seg.blue_agents = None
        seg.red_agents = None
        seg.city = None

    def test_create_agent(self):
       fred = create_agent(TEST_ANUM, color=RED) 
       freds_nm = group_names[RED] + str(TEST_ANUM)
       self.assertEqual(freds_nm, str(fred))

    def test_agent_action(self):
        fred = create_agent(TEST_ANUM, color=RED) 
        ret = agent_action(fred)
        self.assertEqual(ret, False)

    def test_env_unfavorable(self):
        env_fav = env_unfavorable(0.4, 0.5)
        self.assertEqual(env_fav, True)

        env_fav = env_unfavorable(0.6, 0.5)
        self.assertEqual(env_fav, False)


