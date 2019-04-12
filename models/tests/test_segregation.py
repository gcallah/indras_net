"""
This is the test suite for space.py.
"""

from unittest import TestCase, main
from indra.agent import Agent
from models.segregation import set_up, create_agent, RED, BLUE
from models.segregation import env_unfavorable, agent_action
from models.segregation import group_names

TEST_ANUM = 999999


class WolfsheepTestCase(TestCase):
    def setUp(self):
        (self.blue_agents, self.red_agents, self.city) = set_up()

    def tearDown(self):
        self.blue_agents = None
        self.red_agents = None
        self.city = None

    def test_create_agent(self):
       fred = create_agent(TEST_ANUM, color=RED) 
       freds_nm = group_names[RED] + str(TEST_ANUM)
       self.assertEqual(freds_nm, str(fred))
