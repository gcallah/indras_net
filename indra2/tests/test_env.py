"""
This is the test suite for env.py.
"""

from unittest import TestCase, main

from indra2.env import Env
from indra2.agent import Agent
from indra2.tests.test_agent import create_newton


class EnvTestCase(TestCase):
    def test_runN(self):
        NUM_PER = 10
        newton = create_newton();
        env = Env("Test Env", members=[newton])
        acts = env.runN(NUM_PER)
        self.assertEqual(acts, NUM_PER)

if __name__ == '__main__':
    main()
