"""
This is the test suite for space.py.
"""

from unittest import TestCase, main
from indra.agent import Agent
from models.wolfsheep import create_sheep, create_wolf, set_up, wolf_action, sheep_action
from models.wolfsheep import AGT_WOLF_NAME, AGT_SHEEP_NAME, ERR_MSG
from models.wolfsheep import WOLF_LIFESPAN, SHEEP_LIFESPAN, SHEEP_REPRO_PERIOD
from models.wolfsheep import WOLF_REPRO_PERIOD, get_prey, eat, reproduce
from models.wolfsheep import isactive, wolves_created
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
        time_to_repro = self.wolf["time_to_repr"]
        wolf_action(self.wolf)
        if time_to_repro == 1:
            self.assertEqual(self.wolf["time_to_repr"], WOLF_REPRO_PERIOD)
        else:
            self.assertEqual(self.wolf["time_to_repr"], time_to_repro - 1)


    def test_sheep_action(self):
        time_to_repro = self.sheep["time_to_repr"]
        sheep_action(self.sheep)
        if time_to_repro == 1:
                self.assertEqual(self.sheep["time_to_repr"], SHEEP_REPRO_PERIOD)
        else:
            self.assertEqual(self.sheep["time_to_repr"], time_to_repro - 1)

    def test_eat(self):
        """
        When wolf eats sheep, wolf gains life, sheep dies.
        """
        eat(self.wolf, self.sheep)
        self.assertEqual(self.wolf.duration, WOLF_LIFESPAN
                         + SHEEP_LIFESPAN)
        # the sheep should be dead!
        self.assertFalse(isactive(self.sheep))

    def test_isactive(self):
        """
        Test to see if isactive returns  correct values for alive and dead
        agents.
        """
        self.assertEqual(True, isactive(self.sheep))
        self.sheep.die()
        self.assertEqual(False, isactive(self.sheep))

    def test_reproduce(self):
        self.wolf
        self.wolf["time_to_repr"] = 0
        self.assertTrue(reproduce(self.wolf, create_wolf,
                                  wolves_created, wolfsheep.wolves))
        self.assertEqual(self.wolf["time_to_repr"], WOLF_REPRO_PERIOD)


#    def test_wolf_action_repr_period(self):
#        new_wolf = create_wolf(1)
#        wolf_action(new_wolf)
#        self.assertEqual(new_wolf['time_to_repr'], WOLF_REPRO_PERIOD - 1)
#
#    def test_sheep_action_repr_period(self):
#        new_sheep = create_sheep(1)
#        sheep_action(new_sheep)
#        self.assertEqual(new_sheep['time_to_repr'], SHEEP_REPRO_PERIOD - 1)




