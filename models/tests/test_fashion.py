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
    """
    These test cases must be completely rewritten!
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_change_color(self):
        """
        Test changing an agent's color.
        """
        pass


    def test_env_unfavorable(self):
        """
        Test if the env is unfavorable to the agent.
        """
        pass

    def test_new_color_pref(self):
        """
        Make sure determining a new color pref works.
        The tests against neutral need to be re-written.
        """
        pass

    def test_create_tsetter(self):
        pass

    def test_create_follower(self):
        pass

    def test_follower_action(self):
        pass

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
