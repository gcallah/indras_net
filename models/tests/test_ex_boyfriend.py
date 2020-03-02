"""
This is the test suite for ex-boyfriend.py.
"""

from unittest import TestCase, main

from propargs.propargs import PropArgs

import models.ex_boyfriend as ex_boyfriend
from models.ex_boyfriend import set_up


class ExBoyfriendTestCase(TestCase):
    def setUp(self):
        set_up()

    def tearDown(self):
        pass

    def test_create_newly_freed(self):
        """
        Test creating a newly_freed.
        """
        agent = ex_boyfriend.create_newly_freed("Girlfriend", 0)
        self.assertEqual(agent.name, "Girlfriend0")

    def test_create_boyfriend(self):
        """
        Test creating a boyfriend.
        """
        agent = ex_boyfriend.create_boyfriend("Ex-Boyfriend", 0)
        self.assertEqual(agent.name, "Ex-Boyfriend0")

    if __name__ == '__main__':
        main()
