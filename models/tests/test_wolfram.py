from unittest import TestCase, main
from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env
from models.wolfram import create_agent, set_up, B, W
from models.wolfram import next_color
import models.wolfram as wolf

TEST_ANUM = 999999

class WolframTestCase(TestCase):
    def setUp(self):
        (wolf.groups, wolf.wolfram_env, wolf.rule_dict) = set_up()

    def tearDown(self):
        wolf.group = None
        wolf.wolfram_en = None
        wolf.rule_dict = None

    def test_next_color(self):
        self.assertEqual(next_color(wolf.rule_dict, B, B, B), W)
        self.assertEqual(next_color(wolf.rule_dict, W, B, B), B)

#    def test_create_agent(self):
#        a = create_agent(0, 0)
#        self.assertEqual(a.name, '(0,0)')
