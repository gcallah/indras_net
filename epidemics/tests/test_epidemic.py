""" This is a template file for tests.  """
from unittest import TestCase, main, skip

from indra.composite import Composite
from indra.env import Env
import epidemics.epidemic as ep
"""
This is for persoanl reference
HEalthy = "0"
EXposed = "1"
INfected = "2"
Contagious = "3"
DEad = "4"
IMmune = "5"
"""


def create_sal():
    return ep.create_person("Saliou", 0, ep.HE)


def create_bob():
    return ep.create_person("Bob", 1, ep.IN)


def create_azi():
    return ep.create_person("Aziz", 2, ep.CN)

class BasicTestCase(TestCase):
    def setUp(self):
        groups = []
        self.sal = create_sal()
        self.bob = create_bob()
        self.azi = create_azi()


        # create custumized envirements envirements
        

        self.healthy = Composite(ep.HEALTHY, state=ep.HE)
        groups.append(self.healthy)
        groups.append(Composite(ep.EXPOSED, state=ep.EX))
        self.contagious = Composite(ep.CONTAGIOUS, state = ep.CN)
        groups.append(self.contagious)
        groups.append(Composite(ep.INFECTED, state=ep.IN))
        groups.append(Composite(ep.CONTAGIOUS, state=ep.CN))
        groups.append(Composite(ep.DEAD, state=ep.DE))
        groups.append(Composite(ep.IMMUNE, state=ep.IM))
        # you could do this also:
        # exposed = self.env[ep.EXPOSED]

        self.env = Env(ep.MODEL_NAME, height=20, width=20, members=groups)
        ep.set_env_attrs()

    def tearDown(self):
        self.sal = None
        self.bob = None
        self.azi = None
        self.healthy = None
        self.env = None

    def test_healthy(self):
        # create people and test their attrubutes
        self.assertTrue(ep.is_healthy(self.sal))

    def test_not_healthy(self):
        self.assertFalse(ep.is_healthy(self.bob))

    def test_contagious(self):
        self.assertTrue(ep.is_contagious(self.azi))

    def test_samePerson(self):
        self.assertIs(self.azi, self.azi)
     
    def test_not_same_agent(self):
        self.assertIsNot(self.azi,self.bob)
    
    def test_cordinates(self):
        '''
        This should not work yet as Aziz doesn't have
        a pos yet but the problem should be caught.
        '''
        self.assertIsNone(self.azi.get_pos())
 
    def is_located(self):
        self.sal.set_pos(0,0)
        self.asserIsNotNone(self.sal.get_pos())

    @skip("envirement problem, need to clear region to test isolation")
    def test_is_not_quarantined(self):

        # nearby  means 1.8 away
        # create an envirement first
        

        self.healthy += self.sal
        self.contagious += self.azi

        self.bob.set_pos(0,0,0)
        self.azi.set_pos(0,0,1)
        self.assertFalse(ep.is_isolated(self.azi),"Agent is 1 unit away, but is  quanrantined(1.8 normal)")


    @skip("envirement problem, need to clear region to test isolation")
    def test_is_quarantined(self):
        # nearby  means 1.8 away
        # create an envirement first

        self.healthy += self.sal
        self.contagious += self.azi
        self.sal.set_pos(0,0,5)
        self.azi.set_pos(0,0,0)

        self.assertTrue(ep.is_isolated(azi), "agent is 5 units away but is not qurantined(1.8 normal)")

    def test_main(self):
        self.assertEqual(ep.main(), 0)


if __name__ == '__main__':
    main()
