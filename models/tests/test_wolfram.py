from unittest import TestCase, main
from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env
from models.wolfram import create_agent, set_up, B, W
from models.wolfram import next_color, get_color, turn_black
import models.wolfram as wolf

TEST_ANUM = 999999

class WolframTestCase(TestCase):
    def setUp(self):
        (wolf.groups, wolf.wolfram_env, wolf.rule_dict) = set_up()

    def tearDown(self):
        wolf.groups = None
        wolf.wolfram_env = None
        wolf.rule_dict = None

    def test_turn_black(self):
        agent = create_agent(0, 0)
        wolf.groups[W] += agent
        turn_black(wolf.wolfram_env, wolf.groups, agent)
        self.assertEqual(agent.primary_group(), wolf.groups[B])

    def test_get_color(self):
        """
        Based on a passed in group return the appropriate color.
        """
        self.assertEqual(get_color(wolf.groups[B]), B)

    def test_next_color(self):
        """
        Ensure we get proper color based on trio from previous row.
        """
        self.assertEqual(next_color(wolf.rule_dict, B, B, B), W)
        self.assertEqual(next_color(wolf.rule_dict, B, B, W), W)
        self.assertEqual(next_color(wolf.rule_dict, B, W, B), W)
        self.assertEqual(next_color(wolf.rule_dict, B, W, W), B)   
        self.assertEqual(next_color(wolf.rule_dict, W, B, B), B)
        self.assertEqual(next_color(wolf.rule_dict, W, B, W), B)
        self.assertEqual(next_color(wolf.rule_dict, W, W, B), B)
        self.assertEqual(next_color(wolf.rule_dict, W, W, W), W)                

    def test_create_agent(self):
        a = create_agent(0, 0)
        self.assertEqual(a.name, '(0,0)')
