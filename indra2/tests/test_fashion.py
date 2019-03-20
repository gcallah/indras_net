"""
This is the test suite for space.py.
"""

from unittest import TestCase, main
from indra2.agent import switch
from indra2.fashion import set_up, DEBUG, DEBUG2, create_follower, change_color
from indra2.fashion import FOLLOWER_PRENM, RED_FOLLOWERS, BLUE_FOLLOWERS

TEST_FNUM = 999
TEST_FNAME = FOLLOWER_PRENM + str(TEST_FNUM)

red_tsetters = None
blue_tsetters = None
red_followers = None
blue_followers = None
society = None
opp_group = None


class FashionTestCase(TestCase):
    def setUp(self):
        (self.blue_tsetters, self.red_tsetters, self.blue_followers,
         self.red_followers, self.opp_group,
         self.society) = set_up()
        self.test_follower = create_follower(TEST_FNUM)
        self.blue_followers += self.test_follower
        red_tsetters = self.red_tsetters
        blue_tsetters = self.blue_tsetters
        red_followers = self.red_followers
        blue_followers = self.blue_followers
        society = self.society
        opp_group = self.opp_group


class FashionTestCase(TestCase):
    def setUp(self):
        (self.blue_tsetters, self.red_tsetters, self.blue_followers,
         self.red_followers, self.opp_group,
         self.society) = set_up()
        self.test_follower = create_follower(TEST_FNUM)
        self.blue_followers += self.test_follower

    def tearDown(self):
        self.blue_tsetters = None
        self.red_tsetters = None
        self.blue_followers,
        self.red_followers = None
        self.opp_group = None
        self.society = None
        self.test_follower = None

    def test_change_color(self):
        """
        Test changing an agent's color.
        """
        change_color(self.test_follower, self.society, self.opp_group)
        self.assertEqual(len(self.society.switches), 1)
        (agent, from_grp, to_grp) = self.society.switches[0]
        self.assertEqual(str(agent), TEST_FNAME)
        self.assertEqual(str(from_grp), BLUE_FOLLOWERS)
        self.assertEqual(str(to_grp), RED_FOLLOWERS)
        switch(agent, from_grp, to_grp)
        self.assertEqual(agent.primary_group(), to_grp)

if __name__ == '__main__':
    main()
