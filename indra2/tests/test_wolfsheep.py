"""
This is the test suite for space.py.
"""

from unittest import TestCase, main
from indra2.agent import Agent
from indra2.wolfsheep import create_sheep, create_wolf, set_up
import indra2.wolfsheep as wolfsheep

TEST_SNUM = 999
TEST_WNUM = 998

#
# def create_wolf(i):
#     return Agent("wolf" +str(i), duration=10,
#                  attrs={"time_to_repr": 3})
#
#
# def create_sheep(i):
#     return Agent("sheep" + str(i), duration=10,
#                  attrs={"time_to_repr": 3})


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
        self.assertEqual(new_wolf.name, "wolf" + str(1))

    def test_create_sheep(self):
        new_sheep = create_sheep(1)
        self.assertEqual(new_sheep.name,"sheep" + str(1))





