from unittest import TestCase, main
from indra.agent import Agent
from indra.composite import Composite
from indra.space import Space
from indra.env import Env

import models.sandpile as sandpile
import models.wolfram as wolfram
import models.gameoflife as gameoflife

class TestAllModels(TestCase):

    def setUp(self):
        (sandpile.sandpile_env, sandpile.groups, sandpile.group_indices) = sandpile.set_up()
        (wolfram.wolfram_env, wolfram.groups, wolfram.rule_dict) = wolfram.set_up()
        (gameoflife.gameoflife_env, gameoflife.groups) = gameoflife.set_up()

    def tearDown(self):
        sandpile.sandpile_env = None
        sandpile.groups = None
        sandpile.group_indices = None
        wolfram.wolfram_env = None
        wolfram.groups = None
        wolfram.rule_dict = None
        gameoflife.gameoflife_env = None
        gameoflife.groups = None

    def test_runN(self):
        self.assertEqual(sandpile.sandpile_env.runN() > 0, True)
        # self.assertEqual(wolfram.wolfram_env.runN() > 0, True)
        self.assertEqual(gameoflife.gameoflife_env.runN() > 0, True)