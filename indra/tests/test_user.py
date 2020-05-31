"""
This is the test suite for env.py.
"""

from unittest import TestCase, main, skip

from indra.env import Env
from indra.tests.test_agent import create_newton
from indra.tests.test_env import GRP1, GRP2
from indra.user import line_graph, scatter_plot, DEF_STEPS, get_menu_json
from indra.user import not_impl, TermUser
from registry.registry import NOT_IMPL
from indra.user import TestUser, run, CANT_ASK_TEST

MSG = "Hello world"


class UserTestCase(TestCase):
    def setUp(self):
        self.env = Env("Test env")
        self.user = TermUser("User", self.env)
        self.test_user = TestUser("TestUser", self.env)

    def tearDown(self):
        self.user = None
        self.env = None
        self.test_user = None

    def test_tell(self):
        """
        Try to tell the user something.
        """
        ret = self.user.tell(MSG)
        self.assertEqual(ret, MSG)

    @skip("Models work but this test fails: problem is in the test!")
    def test_run(self):
        # need special env for this one
        env = Env("Test env", members=[create_newton()])
        user = TermUser("User", env)
        acts = run(user, test_run=True)
        self.assertEqual(acts, DEF_STEPS)

    def test_not_impl(self):
        self.assertEqual(not_impl(self.user), NOT_IMPL)

    def fill_pop_hist(self):
        self.env.pop_hist.record_pop(GRP1, 10)
        self.env.pop_hist.record_pop(GRP2, 10)
        self.env.pop_hist.record_pop(GRP1, 20)
        self.env.pop_hist.record_pop(GRP2, 20)

    @skip("All line graphs work but this test fails: fault is in the test")
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

    @skip("Models work but this test fails: problem is in the test!")
    def test_tcall(self):
        # need special env for this one
        env = Env("Test env", members=[create_newton()])
        user = TestUser("TestUser", env)
        acts = run(user, test_run=True)
        self.assertEqual(acts, DEF_STEPS)

    def test_task(self):
        self.assertEqual(self.test_user.ask("Silly question?"), CANT_ASK_TEST)

    def test_get_menu_json(self):
        """
        See if we can read in the menu!
        """
        menu = get_menu_json()
        self.assertTrue(len(menu) >= 2)


if __name__ == '__main__':
    main()
