"""
This is the test suite for space.py.
"""

from unittest import TestCase, main
from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env
from models.segregation import set_up, create_agent, RED, BLUE
from models.segregation import env_unfavorable, agent_action
from models.segregation import group_names, agent_action, my_group_index
from models.segregation import env_unfavorable, agent_action, other_group_index
import models.segregation as seg

TEST_ANUM = 999999

SMALL_GRID = 4

def print_sep():
    print("________________________", flush=True)

class SegregationTestCase(TestCase):
    def setUp(self):
        (seg.blue_agents, seg.red_agents, seg.city) = set_up()

    def tearDown(self):
        seg.blue_agents = None
        seg.red_agents = None
        seg.city = None

    def test_my_group_index(self):
        red_agent = create_agent(TEST_ANUM, color=RED)
        self.assertEqual(RED, my_group_index(red_agent))
        blue_agent = create_agent(TEST_ANUM, color=BLUE)
        self.assertEqual(BLUE, my_group_index(blue_agent))

    def test_other_group_index(self):
        red_agent = create_agent(TEST_ANUM, color=RED)
        self.assertEqual(BLUE, other_group_index(red_agent))
        blue_agent = create_agent(TEST_ANUM, color=BLUE)
        self.assertEqual(RED, other_group_index(blue_agent))

    def test_create_agent(self):
        fred = create_agent(TEST_ANUM, color=RED) 
        freds_nm = group_names[RED] + str(TEST_ANUM)
        self.assertEqual(freds_nm, str(fred))

    def create_little_city(self, with_blue=False):
        red_agents = Composite("My reds")
        test_agent = create_agent(TEST_ANUM, color=RED) 
        red_agents += test_agent
        blue_agents = Composite("My blues")
        if with_blue:
            print_sep()
            print("Creating blue agents")
            print_sep()
            for i in range(0, SMALL_GRID):
                print_sep()
                blue_agents += create_agent(TEST_ANUM + 1, color=BLUE)

        my_city = Env("Small city for test", width=SMALL_GRID,
                           height=SMALL_GRID,
                           members=[red_agents, blue_agents])
        return test_agent

    def test_agent_action(self):
        """
        We are going to test two cases: one where agent should
        be satisfied with neighborhood, and one not.
        """
        print_sep()
        print("In test_agent_action")
        print_sep()
        fred = self.create_little_city()
        # self.assertEqual(agent_action(fred), False)
        # fred = self.create_little_city(with_blue=True)
        # self.assertEqual(ret, True)

    def test_env_unfavorable(self):
        env_fav = env_unfavorable(0.4, 0.5)
        self.assertEqual(env_fav, True)

        env_fav = env_unfavorable(0.6, 0.5)
        self.assertEqual(env_fav, False)
