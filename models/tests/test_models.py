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

    def test_sandpile_census(self):
        sandpile.sandpile_action(sandpile.sandpile_env)
        census = sandpile.sandpile_env.get_census(return_census_dict=True)
        self.assertEqual(census["agents acted"], 1)
        sandpile.sandpile_action(sandpile.sandpile_env)
        sandpile.sandpile_action(sandpile.sandpile_env)
        sandpile.sandpile_action(sandpile.sandpile_env)
        sandpile.sandpile_action(sandpile.sandpile_env)
        census = sandpile.sandpile_env.get_census(return_census_dict=True)
        self.assertEqual(census["agents acted"], 5)
        self.assertEqual("Group3" in census["group census"], True)

    def test_wolfram_census(self):
        census = wolfram.wolfram_env.get_census(return_census_dict=True)
        self.assertEqual(census["agents acted"], 0)
        wolfram.wolfram_action(wolfram.wolfram_env)
        census = wolfram.wolfram_env.get_census(return_census_dict=True)
        self.assertEqual(census["agents acted"], 3)
        # wolfram.wolfram_action(wolfram.wolfram_env)
        # census = wolfram.wolfram_env.get_census(return_census_dict=True)
        # self.assertEqual(census["agents acted"], 3)
        # wolfram.wolfram_action(wolfram.wolfram_env)
        # census = wolfram.wolfram_env.get_census(return_census_dict=True)
        # wolfram.wolfram_env.user.tell(census["agents acted"])
        # self.assertEqual(census["agents acted"], 6)

    def test_gameoflife_census(self):
        wolfram.wolfram_action(wolfram.wolfram_env)