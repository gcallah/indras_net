"""
This is the test suite for the wolf-sheep model.
"""

from unittest import TestCase, skip

from registry.registry import get_group, get_env
import models.wolfsheep as ws
from models.wolfsheep import AGT_WOLF_NAME, AGT_SHEEP_NAME
from models.wolfsheep import WOLF_GROUP, SHEEP_GROUP
from models.wolfsheep import WOLF_LIFESPAN, SHEEP_LIFESPAN, SHEEP_REPRO_PERIOD, MAX_ENERGY
from models.wolfsheep import WOLF_REPRO_PERIOD, eat, reproduce
from models.wolfsheep import create_sheep, create_wolf, set_up
from models.wolfsheep import wolf_action, sheep_action
from models.wolfsheep import isactive, TIME_TO_REPR

TEST_SNUM = 3
TEST_WNUM = 3
TEST_WNAME = AGT_WOLF_NAME + str(TEST_WNUM)
TEST_SNAME = AGT_SHEEP_NAME + str(TEST_SNUM)


class WolfsheepTestCase(TestCase):
    def setUp(self, props=None):
        set_up()
        self.wolf = create_wolf(TEST_WNAME, TEST_WNUM)
        self.sheep = create_sheep(TEST_SNAME, TEST_SNUM)
        self.wolves = get_group(WOLF_GROUP)
        self.wolves += self.wolf
        # make a new plural for sheep!
        self.sheeps = get_group(SHEEP_GROUP)
        self.sheeps += self.sheep
        get_env().place_member(self.sheep, None)
        get_env().place_member(self.wolf, None)

    def tearDown(self):
        self.wolf = None
        self.sheep = None
        self.wolves = None
        self.sheeps = None

    # an integration test:
    def test_main(self):
        self.assertEqual(ws.main(), 0)

    def test_create_wolf(self):
        """
         Test to see if wolf is created
        """
        new_wolf = create_wolf(TEST_WNAME, 1)
        self.assertEqual(new_wolf.name, AGT_WOLF_NAME + str(1))

    def test_create_sheep(self):
        """
        Test to see if sheep is created
        """
        new_sheep = create_sheep(TEST_SNAME, 1)
        self.assertEqual(new_sheep.name, AGT_SHEEP_NAME + str(1))

    def test_wolf_action(self):
        """
        Wolves act by eating a random sheep from the meadow.
        """
        time_to_repro = self.wolf[TIME_TO_REPR]
        wolf_action(self.wolf)
        if time_to_repro == 1:
            self.assertEqual(self.wolf[TIME_TO_REPR], WOLF_REPRO_PERIOD)
        else:
            self.assertEqual(self.wolf[TIME_TO_REPR], time_to_repro - 1)

    def test_sheep_action(self):
        time_to_repro = self.sheep[TIME_TO_REPR]
        sheep_action(self.sheep)
        if time_to_repro == 1:
            self.assertEqual(self.sheep[TIME_TO_REPR],
                             SHEEP_REPRO_PERIOD)
        else:
            self.assertEqual(self.sheep[TIME_TO_REPR], time_to_repro - 1)

    def test_eat(self):
        """
        When wolf eats sheep, wolf gains life, sheep dies.
        """
        eat(self.wolf, self.sheep)
        self.assertEqual(self.wolf.duration, WOLF_LIFESPAN
                         + min(SHEEP_LIFESPAN, MAX_ENERGY))
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


    def test_reproduce(self):
        """
        Test to see if wolves reproduce at the right time.
        """
        self.wolf[TIME_TO_REPR] = 0
        reproduce(self.wolf, create_wolf, WOLF_GROUP)
        # self.assertTrue(reproduce(self.wolf, create_wolf, WOLF_GROUP))
        self.assertEqual(self.wolf[TIME_TO_REPR], WOLF_REPRO_PERIOD)


    def test_reproduce_nonzerotimetorepr(self):
        """
        Negative test to check the reproduction of wolves.
        """
        self.wolf[TIME_TO_REPR] = 1
        self.assertFalse(reproduce(self.wolf, create_wolf, WOLF_GROUP))
