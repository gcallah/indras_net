"""
This is the test suite for env.py.
"""

from unittest import TestCase, main

from indra2.env import Env
from indra2.user import not_impl, NOT_IMPL, TermUser
from indra2.user import line_graph, scatter_plot
from indra2.tests.test_env import GRP1, GRP2


class UserTestCase(TestCase):
    def setUp(self):
        # we will need to change env above from None ASAP!
        self.env = Env("Test env")
        self.user = TermUser("TestUser", self.env)

    def tearDown(self):
        self.user = None
        self.env = None

    def test_not_impl(self):
        self.assertEqual(not_impl(self.user), NOT_IMPL)

    def fill_pop_hist(self):
        self.env.pop_hist.record_pop(GRP1, 10)
        self.env.pop_hist.record_pop(GRP2, 10)
        self.env.pop_hist.record_pop(GRP1, 20)
        self.env.pop_hist.record_pop(GRP2, 20)

    def test_line_graph(self):
        self.fill_pop_hist()
        ret = line_graph(self.user)
        if self.user.env.has_disp():
            self.assertIsNotNone(ret)
        else:
            self.assertIsNone(ret)

    def test_scatter_plot(self):
        self.fill_pop_hist()
        ret = scatter_plot(self.user)
        if self.user.env.has_disp():
            self.assertIsNotNone(ret)
        else:
            self.assertIsNone(ret)

if __name__ == '__main__':
    main()
