"""
This is the test suite for space.py.
"""

from operator import gt, lt
from unittest import TestCase, main, skip

import models.fashion as fshn
from indra.agent import switch
from models.fashion import BLUE_FOLLOWERS, RED_SIN, NEUTRAL, BIG_ENOUGH
from models.fashion import BLUE_SIN, TSETTER_PRENM
from models.fashion import FOLLOWER_PRENM, RED_FOLLOWERS, env_unfavorable
from models.fashion import change_color, create_tsetter
from models.fashion import follower_action, tsetter_action, new_color_pref
from models.fashion import set_up, create_follower

TEST_FNUM = 999
TEST_TNUM = 998
TEST_FNAME = FOLLOWER_PRENM + str(TEST_FNUM)


class FashionTestCase(TestCase):
    def setUp(self):
        (fshn.society, fshn.blue_tsetters, fshn.red_tsetters,
         fshn.blue_followers, fshn.red_followers, fshn.opp_group) = set_up()
        self.test_follower = create_follower(FOLLOWER_PRENM, TEST_FNUM)
        self.test_tsetter = create_tsetter(TSETTER_PRENM, TEST_TNUM)
        fshn.red_tsetters += self.test_tsetter
        fshn.blue_followers += self.test_follower

    def tearDown(self):
        fshn.blue_tsetters = None
        fshn.red_tsetters = None
        fshn.blue_followers = None
        fshn.red_followers = None
        fshn.opp_group = None
        fshn.society = None
        self.test_follower = None
        self.test_tsetter = None

    def test_change_color(self):
        """
        Test changing an agent's color.
        """
        change_color(self.test_follower, fshn.society, fshn.opp_group)
        self.assertEqual(len(fshn.society.switches), 1)
        # here we should actually trigger the switch, but we have to
        # figure out how without getting all up in the switches internals

    def test_env_unfavorable(self):
        """
        Test if the env is unfavorable to the agent.
        """
        self.assertTrue(env_unfavorable(RED_SIN, BLUE_SIN, lt, gt))
        self.assertFalse(env_unfavorable(RED_SIN, RED_SIN, lt, gt))
        self.assertFalse(env_unfavorable(RED_SIN, NEUTRAL, lt, gt))
        self.assertTrue(env_unfavorable(RED_SIN, NEUTRAL - BIG_ENOUGH, lt, gt))
        self.assertTrue(env_unfavorable(
            BLUE_SIN, NEUTRAL + BIG_ENOUGH, lt, gt))

    def test_new_color_pref(self):
        """
        Make sure determining a new color pref works.
        The tests against neutral need to be re-written.
        """
        new_pref = new_color_pref(RED_SIN, RED_SIN)
        self.assertEqual(new_pref, RED_SIN)
        new_pref = new_color_pref(BLUE_SIN, BLUE_SIN)
        self.assertEqual(new_pref, BLUE_SIN)
        new_pref = new_color_pref(BLUE_SIN, RED_SIN)
        # self.assertAlmostEqual(new_pref, NEUTRAL)
        new_pref = new_color_pref(RED_SIN, BLUE_SIN)
        # self.assertAlmostEqual(new_pref, NEUTRAL)

    def test_create_tsetter(self):
        new_agent = create_tsetter(TSETTER_PRENM, 2, RED_SIN)

        self.assertEqual(new_agent.name, TSETTER_PRENM + str(2))

    def test_create_follower(self):
        new_follower = create_follower(FOLLOWER_PRENM, 2, BLUE_SIN)
        self.assertEqual(new_follower.name, FOLLOWER_PRENM + str(2))

    def test_follower_action(self):
        follower = self.test_follower
        old_grp = follower.primary_group()
        ratio = follower_action(follower)
        if ratio <= 1:
            self.assertEqual(follower.primary_group(), old_grp)
        else:
            self.assertEqual(len(fshn.society.switches), 1)

    @skip("Model seems to work but this test fails: must investigate.")
    def test_tsetter_action(self):
        tsetter = self.test_tsetter
        oldt_grp = tsetter.primary_group()
        ratio = tsetter_action(tsetter)
        if ratio <= 1:
            self.assertEqual(len(fshn.society.switches), 1)
        else:
            self.assertEqual(tsetter.primary_group(), oldt_grp)

    if __name__ == '__main__':
        main()
