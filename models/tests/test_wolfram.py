from unittest import TestCase, main
from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env
from models.wolfram import create_agent, set_up

TEST_ANUM = 999999

class WolframTestCase(TestCase):
    def setUp(self):
        set_up()
        self.test_agent = create_agent(TEST_ANUM, TEST_ANUM)
        pass
    def test_create_agent(self):
        agent = create_agent(TEST_ANUM, TEST_ANUM)
        test_name = "(" + str(TEST_ANUM) + "," + str(TEST_ANUM) + ")"
        self.assertEqual(agent.name, test_name)    
    
