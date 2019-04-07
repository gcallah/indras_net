"""
This is the test suite for space.py.
"""

from unittest import TestCase, main
from indra.agent import Agent
from models.wolfsheep import create_sheep, create_wolf, set_up, wolf_action, sheep_action
from models.wolfsheep import AGT_WOLF_NAME, AGT_SHEEP_NAME, ERR_MSG
from models.wolfsheep import WOLF_LIFESPAN, SHEEP_LIFESPAN, SHEEP_REPRO_PERIOD
from models.wolfsheep import WOLF_REPRO_PERIOD
import models.wolfsheep as wolfsheep

TEST_SNUM = 3
TEST_WNUM = 3
TEST_WNAME = AGT_WOLF_NAME + str(TEST_WNUM)
TEST_SNAME = AGT_SHEEP_NAME + str(TEST_SNUM)


class WolfsheepTestCase(TestCase):
    def setUp(self):
        (wolfsheep.wolves, wolfsheep.sheep, wolfsheep.meadow) = set_up()
        self.wolf = create_wolf(TEST_WNUM)
        self.sheep = create_sheep(TEST_SNUM)

    def tearDown(self):
        self.test_wolves = None
        self.test_sheep = None

    def test_create_wolf(self):
        new_wolf = create_wolf(1)
        self.assertEqual(new_wolf.name, AGT_WOLF_NAME + str(1))

    def test_create_sheep(self):
        new_sheep = create_sheep(1)
        self.assertEqual(new_sheep.name, AGT_SHEEP_NAME + str(1))

    def test_wolf_action(self):
        # yet to be enhanced
        wolf_action(self.wolf)
        self.assertEqual(self.wolf.name, TEST_WNAME)
        # this test can't be right:
        # self.assertEqual(self.wolf.duration, WOLF_LIFESPAN+SHEEP_LIFESPAN)
        # because wolf eats sheep

    def test_sheep_action(self):
        # yet to be enhanced
        sheep_action(self.sheep)
        # action doesn't change name!
        # self.assertEqual(self.sheep.name, TEST_SNAME) 
        self.assertEqual(self.sheep.duration, SHEEP_LIFESPAN)

    def test_wolf_action_repr_period(self):
        new_wolf = create_wolf(1)
        wolf_action(new_wolf)
        self.assertEqual(new_wolf['time_to_repr'], WOLF_REPRO_PERIOD-1)

    def test_sheep_action_repr_period(self):
        new_sheep = create_sheep(1)
        sheep_action(new_sheep)
        self.assertEqual(new_sheep['time_to_repr'], SHEEP_REPRO_PERIOD-1)




