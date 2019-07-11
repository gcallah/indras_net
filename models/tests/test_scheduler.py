"""
This is the test suite for space.py.
"""

from unittest import TestCase, main
from operator import gt, lt
from indra.agent import switch
from indra.env import Env
from models.scheduler import set_up
import models.scheduler as fshn


class SchedulerTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_set_up(self):
        """
        Test setting up env.
        """
        (env, grp1, grp2) = set_up()
        self.assertTrue(isinstance(env, Env))

    if __name__ == '__main__':
        main()
