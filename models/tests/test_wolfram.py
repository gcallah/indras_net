from unittest import TestCase, main
from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env
from models.wolfram import create_agent, set_up, B, W
from models.wolfram import turn_black, get_color, get_rule, next_color, wolfram_action
import models.wolfram as wolf

TEST_ANUM = 999999

class WolframTestCase(TestCase):
    def setUp(self):
        (wolf.wolfram_env, wolf.groups, wolf.rule_dict) = set_up()

    def tearDown(self):
        wolf.groups = None
        wolf.wolfram_env = None
        wolf.rule_dict = None

    def test_create_agent(self):
        a = create_agent(0, 0)
        self.assertEqual(a.name, '(0,0)')

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

    def test_get_rule(self):
        rule30 =  {"(1, 1, 1)": 0,
        "(1, 1, 0)": 0,
        "(1, 0, 1)": 0,
        "(1, 0, 0)": 1,
        "(0, 1, 1)": 1,
        "(0, 1, 0)": 1,
        "(0, 0, 1)": 1,
        "(0, 0, 0)": 0}
        self.assertEqual(get_rule(30), rule30)

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

    def test_wolfram_action(self):

        rule30 = {
        (B, B, B): W,
        (B, B, W): W,
        (B, W, B): W,
        (B, W, W): B,
        (W, B, B): B,
        (W, B, W): B,
        (W, W, B): B,
        (W, W, W): W}

        periods = wolf.wolfram_env.get_periods()
        
        wolfram_action(wolf.wolfram_env)
        self.assertEqual(wolf.wolfram_env.height - 2, wolf.wolfram_env.height - periods - 2)

        active_row = wolf.wolfram_env.get_row_hood(wolf.wolfram_env.height - periods - 1)
        correct_row = wolf.wolfram_env.get_row_hood(wolf.wolfram_env.height - 2)
        equal = True
        for i in range(len(active_row)):
            if active_row[i] != correct_row[i]:
                equal = False
        self.assertEqual(equal, True)

        next_row = wolf.wolfram_env.get_row_hood(wolf.wolfram_env.height - periods - 2)
        next_correct_row = wolf.wolfram_env.get_row_hood(wolf.wolfram_env.height - 3)
        equal = True
        for i in range(len(next_row)):
            if next_row[i] != next_correct_row[i]:
                equal = False
        self.assertEqual(equal, True)

        previous_row = wolf.wolfram_env.get_row_hood(wolf.wolfram_env.height - periods - 1)
        previous_correct_row = wolf.wolfram_env.get_row_hood(wolf.wolfram_env.height - 1)
        equal = True
        for i in range(len(previous_row)):
            if previous_row[i] != previous_correct_row[i]:
                equal = False
        self.assertEqual(equal, True)
