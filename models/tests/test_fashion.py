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

    def test_main(self):
        self.assertEqual(fshn.main(), 0)

    if __name__ == '__main__':
        main()
