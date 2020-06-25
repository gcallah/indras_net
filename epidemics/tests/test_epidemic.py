""" This is a template file for tests.  """
from unittest import TestCase, main, skip
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


def create_env():
    return ep.set_up()


class BasicTestCase(TestCase):
    def set_up(self):
        sal = create_sal()
        bob = create_bob()
        azi = create_azi()
        
    def tear_down(self):
        sal = None
        bob = None
        azi = None
        env = None

    def test_healthy(self):
        # create people and test their attrubutes
        sal = create_sal()
        self.assertTrue(ep.is_healthy(sal))

    def test_not_healthy(self):

        bob = create_bob()
        self.assertFalse(ep.is_healthy(bob))

    def test_contagious(self):
        azi = create_azi()
        self.assertTrue(ep.is_contagious(azi))

    def test_samePerson(self):
        azi = create_azi()
        self.assertIs(azi, azi)
     
    def test_not_same_agent(self):
        azi = create_azi()
        bob = create_bob()
        self.assertIsNot(azi,bob)
    
    def test_cordinates(self):
        '''
        This should not work yet as Aziz doesn't have
        a pos yet but the problem should be caught.
        '''
        azi = create_azi()
        self.assertIsNone(azi.get_pos())
 
    def is_located(self):         
        bob = create_bob()
        bob.set_pos(0,0)
        self.asserIsNotNone(bob.get_pos())

    def test_is_not_quarantined(self):

        # nearby  means 1.8 away
        # create an envirement first
        
        env = create_env()
        bob = create_bob()
        bob.set_pos(0,0,0)
        azi = create_azi()
        azi.set_pos(0,0,1)
        self.assertFalse(ep.is_isolated(azi),"Agent is 1 unit away, but is  quanrantined(1.8 normal)")

    @skip("envirement problem, need to clear region to test isolation")
    def test_is_quarantined(self):

        # nearby  means 1.8 away
        # create an envirement first

        env = create_env()
        bob = create_bob()
        bob.set_pos(0,0,5)
        azi = create_azi()
        azi.set_pos(0,0,0)
        self.assertTrue(ep.is_isolated(azi), "agent is 5 units away but is not qurantined(1.8 normal)")

    def test_main(self):
        self.assertEqual(ep.main(), 0)


if __name__ == '__main__':
    main()
