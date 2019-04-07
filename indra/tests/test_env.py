"""
This is the test suite for env.py.
"""

from unittest import TestCase, main

import indra.display_methods as disp

from indra.env import Env, PopHist, POP_HIST_HDR, POP_SEP
from indra.user import TEST, WEB
from indra.agent import Agent
from indra.tests.test_agent import create_newton
from indra.tests.test_composite import create_calcguys, create_cambguys

GRP1 = "Group1"
GRP2 = "Group2"

X = 0
Y = 1


class EnvTestCase(TestCase):
    def setUp(self):
        self.newton = create_newton()
        self.calcs = create_calcguys()
        self.cambs = create_cambguys()
        self.pop_hist = PopHist()
        self.env = Env("Test env")

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

    def test_user_type(self):
        self.assertEqual(self.env.user_type, TEST)

    def test_runN(self):
        NUM_PERIODS = 10
        self.env += self.newton
        acts = self.env.runN(NUM_PERIODS)
        self.assertEqual(acts, NUM_PERIODS)

    def test_str_pop(self):
        self.fill_pop_hist()
        s = str(self.pop_hist)
        self.assertEqual(s, POP_HIST_HDR + GRP1 + POP_SEP + GRP2 + POP_SEP)

    def test_record_pop(self):
        self.assertTrue(True)

    def test_add_child(self):
        self.env.add_child(self.newton, self.calcs)
        self.assertIn((self.newton, self.calcs), self.env.womb)

    def test_add_switch(self):
        self.env.add_switch(self.newton, self.calcs, self.cambs)
        self.assertIn((self.newton, self.calcs, self.cambs),self.env.switches)

    def test_has_disp(self):
        if not disp.plt_present:
            self.assertTrue(not self.env.has_disp())
        else:
            self.assertTrue(self.env.has_disp())

    # def test_line_data(self):
    #     self.fill_pop_hist()
    #     ret = self.env.line_data()
    #     self.assertEqual(ret, (1, {GRP1: {"data": [10, 20]}, GRP2: {"data": [10, 20]}}))
    #
    # def test_plot_data(self):
    #     self.pop_hist.record_pop(GRP1, 10)
    #     ret = self.env.plot_data()
    #     current_var = self.env.members[GRP1]
    #     current_agent_pos = current_var[GRP1].pos
    #     (x, y) = current_agent_pos
    #     self.assertEqual(ret, {GRP1: {X: [x], Y: [y]}})

    def test_headless(self):
        bool = (self.env.user_type == WEB) or (self.env.user_type == TEST)
        if bool:
            self.assertTrue(self.env.headless())
        else:
            self.assertTrue(not self.env.headless())


if __name__ == '__main__':
    main()
