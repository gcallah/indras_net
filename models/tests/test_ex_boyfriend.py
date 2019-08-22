"""
This is the test suite for ex-boyfriend.py.
"""

from unittest import TestCase, main
from propargs.propargs import PropArgs
from operator import gt, lt
from indra.agent import switch
from indra.env import Env
from models.ex_boyfriend import set_up
import models.ex_boyfriend as ex_boyfriend


class ExBoyfriendTestCase(TestCase):
    def setUp(self):
        self.pa = PropArgs.create_props('ex_boyfriend_props',
                                        ds_file='props/ex_boyfriend.props.json')
        (self.bar, self.ex_boyfriend, self.girlfriend) = set_up()

    def tearDown(self):
        (self.bar, self.ex_boyfriend, self.girlfriend) = (None, None, None)

    def test_create_girlfriend(self):
        """
        Test creating a girlfriend.
        """
        agent = ex_boyfriend.create_girlfriend("Girlfriend", 0)
        self.assertEqual(agent.name, "Girlfriend0")

    def test_create_boyfriend(self):
        """
        Test creating a boyfriend.
        """
        agent = ex_boyfriend.create_boyfriend("Ex-Boyfriend", 0, self.pa)
        self.assertEqual(agent.name, "Ex-Boyfriend0")

    if __name__ == '__main__':
        main()
