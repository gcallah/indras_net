from unittest import TestCase, main
from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env
from models.wolfram import set_up, W, B
from models.wolfram import create_agent, turn_black, get_color, get_rule, next_color, wolfram_action
import models.wolfram as wolf

TEST_ANUM = 999999

class WolframTestCase(TestCase):
    def setUp(self):
        (wolf.wolfram_env, wolf.groups, wolf.rule_dict) = set_up()

    def tearDown(self):
        wolf.wolfram_env = None
        wolf.groups = None
        wolf.rule_dict = None

    def test_create_agent(self):
        """
        Creates an agent and checks that it has the correct name,
        which is its (x, y) corrdinates.
        """
        a = create_agent(0, 0)
        self.assertEqual(a.name, '(0,0)')

    def test_turn_black(self):
        """
        Creates an agent and assign it to group white
        then change the color of this agent to black using turn_black
        then checks that the color was correctly switched.
        """
        agent = create_agent(0, 0)
        white = Composite("white")
        black = Composite("black")
        wolf.groups = []
        wolf.groups.append(white)
        wolf.groups.append(black)
        wolf.groups[W] += agent
        turn_black(wolf.groups, agent)
        self.assertEqual(agent.primary_group(), wolf.groups[B])

    def test_get_color(self):
        """
        Based on a passed in group return the appropriate color.
        """
        white = Composite("white")
        black = Composite("black")
        wolf.groups = []
        wolf.groups.append(white)
        wolf.groups.append(black)
        self.assertEqual(get_color(wolf.groups[W]), W)

    def test_get_rule(self):
        """
        Creates a dictionary of a rule (rule 30 in this case)
        then compares it to what get_rule returns 
        given that get_rule was passed in the parameter to return rule 30.
        """
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
