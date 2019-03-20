"""
This is the test suite for space.py.
"""

from unittest import TestCase, main
from indra2.agent import switch
from indra2.fashion import set_up, DEBUG, DEBUG2, create_follower
from indra2.fashion import change_color, create_tsetter, follower_action, tsetter_action
from indra2.fashion import FOLLOWER_PRENM, RED_FOLLOWERS, BLUE_FOLLOWERS, RED
from indra2.fashion import BLUE, TSETTER_PRENM, BLUE_TSETTERS, RED_TSETTERS
import indra2.fashion as fshn

TEST_FNUM = 999
TEST_FNAME = FOLLOWER_PRENM + str(TEST_FNUM)


class FashionTestCase(TestCase):
    def setUp(self):
        (fshn.blue_tsetters, fshn.red_tsetters, fshn.blue_followers,
         fshn.red_followers, fshn.opp_group, fshn.society) = set_up()
        self.test_follower = create_follower(TEST_FNUM)
        fshn.blue_followers += self.test_follower

    def tearDown(self):
        fshn.blue_tsetters = None
        fshn.red_tsetters = None
        fshn.blue_followers = None
        fshn.red_followers = None
        fshn.opp_group = None
        fshn.society = None
        self.test_follower = None

    def test_change_color(self):
        """
        Test changing an agent's color.
        """
        change_color(self.test_follower, fshn.society, fshn.opp_group)
        self.assertEqual(len(fshn.society.switches), 1)
        (agent, from_grp, to_grp) = fshn.society.switches[0]
        self.assertEqual(str(agent), TEST_FNAME)
        self.assertEqual(str(from_grp), BLUE_FOLLOWERS)
        self.assertEqual(str(to_grp), RED_FOLLOWERS)
        switch(agent, from_grp, to_grp)
        self.assertEqual(agent.primary_group(), to_grp)

    
    def test_create_tsetter(self):
        new_agent = create_tsetter(2, RED)

        self.assertEqual(new_agent.name, TSETTER_PRENM +str(2))
        # if(Agent['color']=='RED'):
        #     print(True)
        # else:
        #     print(False)

    def test_create_follower(self):
        new_follower = create_follower(2 , BLUE)
        self.assertEqual(new_follower.name, FOLLOWER_PRENM + str(2))

    def test_follower_action(self):
        follower = self.test_follower
        old_grp = follower.primary_group()
        ratio = follower_action(follower)
        if ratio <= 1:
            self.assertEqual(follower.primary_group(), old_grp)
                # self.assertEqual(.primary_group(),RED_FOLLOWERS)
                # self.assertEqual(ratio)


    # def test_tsetter_action(self):
    #             tsetter_action(BLUE_TSETTERS)
    #             self.assertEqual(.primary_group(), BLUE_TSETTERS)
    #             self.assertle


    if __name__ == '__main__':
        main()
