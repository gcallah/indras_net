"""
This is the test suite for space.py.
"""

from unittest import TestCase, main
from indra2.agent import Agent
from indra2.wolfsheep import create_sheep, create_wolf, set_up, wolf_action, sheep_action
from indra2.wolfsheep import AGT_WOLF_NAME, AGT_SHEEP_NAME, ERR_MSG, WOLF_LIFESPAN, SHEEP_LIFESPAN
import indra2.wolfsheep as wolfsheep

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
        self.assertEqual(self.wolf.duration, WOLF_LIFESPAN+SHEEP_LIFESPAN)  # because wolf eats sheep

    def test_wolf_action_neg_case(self):
        test_neg_case = wolf_action(self.sheep)
        self.assertEqual(test_neg_case, ERR_MSG)

    def test_sheep_action(self):
        # yet to be enhanced
        sheep_action(self.sheep)
        self.assertEqual(self.sheep.name, TEST_SNAME)
        self.assertEqual(self.sheep.duration, SHEEP_LIFESPAN)

    def test_sheep_action_neg_case(self):
        test_negCase = sheep_action(self.wolf)
        self.assertEqual(test_negCase, ERR_MSG)






