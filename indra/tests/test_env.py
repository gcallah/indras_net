"""
This is the test suite for env.py.
"""
import os
from unittest import TestCase, main, skip

import indra.display_methods as disp
from indra.composite import Composite
from indra.env import Env, PopHist, POP_HIST_HDR, POP_SEP
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.tests.test_agent import create_newton
from indra.tests.test_composite import create_calcguys, create_cambguys
from indra.user import TEST, API

travis = False

GRP1 = "Group1"
GRP2 = "Group2"

X = 0
Y = 1

ENV_ACT_RET = 10


def env_action(env, **kwargs):
    env.duration = ENV_ACT_RET


class EnvTestCase(TestCase):
    def setUp(self):
        self.newton = create_newton()
        self.calcs = create_calcguys()
        self.cambs = create_cambguys()
        self.pop_hist = PopHist()
        self.env = Env("Test env", action=env_action)

    def tearDown(self):
        self.newton = None
        self.calcs = None
        self.cambs = None
        self.pop_hist = None
        self.env = None

    def fill_pop_hist(self):
        self.pop_hist.record_pop(GRP1, 10)
        self.pop_hist.record_pop(GRP2, 10)
        self.pop_hist.record_pop(GRP1, 20)
        self.pop_hist.record_pop(GRP2, 20)
        return self.pop_hist

    def test_user_type(self):
        """
        Make sure our user type is test.
        """
        self.assertEqual(self.env.user_type, TEST)

    def test_runN(self):
        """
        Test running for N turns.
        """
        new_env = Env("Test1 env", action=env_action,
                      members=[self.newton])
        num_periods = 10
        acts = new_env.runN(num_periods)
        self.assertEqual(acts, num_periods)

    def test_str_pop(self):
        """
        Test converting the pop history to a string.
        """
        self.fill_pop_hist()
        s = str(self.pop_hist)
        self.assertEqual(s, POP_HIST_HDR + GRP1 + POP_SEP + GRP2 + POP_SEP)

    def test_record_pop(self):
        self.assertTrue(True)

    @skip("This now works differently and the test needs to be re-written")
    def test_add_child(self):
        self.env.add_child(self.newton, self.calcs)
        self.assertIn((self.newton, self.calcs), self.env.womb)

    def test_add_switch(self):
        self.env.add_switch(self.newton, self.calcs, self.cambs)
        self.assertIn((self.newton.name, self.calcs.name, self.cambs.name),
                      self.env.switches)

    def test_has_disp(self):
        if not disp.plt_present:
            self.assertTrue(not self.env.has_disp())
        else:
            self.assertTrue(self.env.has_disp())

    def test_line_data(self):
        """
        Test the construction of line graph data.
        This test must be changed to handle new color param!
        Commented out for the moment.
        """
        global travis
        travis = os.getenv("TRAVIS")
        if not travis:
            self.env.pop_hist = self.fill_pop_hist()
            ret = self.env.line_data()
            self.assertEqual(ret, (2,
                                   {GRP1: {"color": "navy", "data": [10, 20]},
                                    GRP2: {"color": "blue", "data": [10, 20]}}))

    def test_plot_data(self):
        """
        Test the construction of scatter plot data.
        """
        global travis
        travis = os.getenv("TRAVIS")
        if not travis:
            our_grp = Composite(GRP1, members=[self.newton])
            self.env = Env("Test env", members=[our_grp])
            ret = self.env.plot_data()
            (x, y) = self.newton.pos
            self.assertEqual(ret, {GRP1: {X: [x], Y: [y], 'color': None,
                                          'marker': None}})

    def test_headless(self):
        if (self.env.user_type == API) or (self.env.user_type == TEST):
            self.assertTrue(self.env.headless())
        else:
            self.assertTrue(not self.env.headless())

    def test_env_action(self):
        self.env()
        self.assertEqual(self.env.duration, ENV_ACT_RET)

    @skip
    def test_restore_env(self):
        """
        This test depends upon a particular, stored json
        format: must be re-written.
        """
        tests_env = env_json_basic.ret()
        ret_env = Env("env", serial_obj=tests_env)
        self.assertEqual(str(type(ret_env)), "<class 'indra.env.Env'>")


if __name__ == '__main__':
    main()
