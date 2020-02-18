"""
This is the test suite for space.py.
"""

from unittest import TestCase, skip

import models.wolfsheep as ws
from indra.utils import get_props
from models.wolfsheep import AGT_WOLF_NAME, AGT_SHEEP_NAME
from models.wolfsheep import WOLF_LIFESPAN, SHEEP_LIFESPAN, SHEEP_REPRO_PERIOD
from models.wolfsheep import WOLF_REPRO_PERIOD, eat, reproduce
from models.wolfsheep import create_sheep, create_wolf, set_up, wolf_action, \
    sheep_action
from models.wolfsheep import isactive, wolves_created

TEST_SNUM = 3
TEST_WNUM = 3
TEST_WNAME = AGT_WOLF_NAME + str(TEST_WNUM)
TEST_SNAME = AGT_SHEEP_NAME + str(TEST_SNUM)


class WolfsheepTestCase(TestCase):
    def setUp(self, props=None):
        self.pa = get_props("wolfsheep", props)
        set_up()
        self.wolf = create_wolf(TEST_WNAME, TEST_WNUM, self.pa)
        self.sheep = create_sheep(TEST_SNAME, TEST_SNUM, self.pa)

    def tearDown(self):
        self.test_wolves = None
        self.test_sheep = None

    def test_create_wolf(self):
        """
         Test to see if wolf is created
        """
        new_wolf = create_wolf(TEST_WNAME, 1, props=self.pa)
        self.assertEqual(new_wolf.name, AGT_WOLF_NAME + str(1))

    def test_create_sheep(self):
        """
        Test to see if sheep is created
        """
        new_sheep = create_sheep(TEST_SNAME, 1, props=self.pa)
        self.assertEqual(new_sheep.name, AGT_SHEEP_NAME + str(1))

    def test_wolf_action(self):
        """
        Wolves act by eating a random sheep from the meadow.
        """
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
            self.assertEqual(self.sheep["time_to_repr"],
                             SHEEP_REPRO_PERIOD)
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
        Test to see if is_active returns  correct values for alive and dead
        agents.
        """
        self.assertEqual(True, isactive(self.sheep))
        self.sheep.die()
        self.assertEqual(False, isactive(self.sheep))

    @skip("Must re-write for no global regime.")
    def test_reproduce(self):
        """
        Test to see if wolves reproduce at the right time.
        """
        self.wolf["time_to_repr"] = 0
        self.assertTrue(reproduce(self.wolf, create_wolf,
                                  wolves_created, ws.wolves))
        self.assertEqual(self.wolf["time_to_repr"], WOLF_REPRO_PERIOD)

    @skip("Must re-write for no global regime.")
    def test_reproduce_nonzerotimetorepr(self):
        """
        Negative test to check the reproduction of wolves.
        """
        self.wolf["time_to_repr"] = 1
        self.assertFalse(reproduce(self.wolf, create_wolf,
                                   wolves_created, ws.wolves))
