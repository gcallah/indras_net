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


def create_envirement():
    return ep.set_up()


class BasicTestCase(TestCase):
    def setUp(self):
        sal = create_sal()
        bob = create_bob()
        azi = create_azi()

    def tearDown(self):
        sal = None
        bob = None
        azi = None
        env = None

    def testHealthy(self):
        # create people and test their attrubutes
        sal = create_sal()

        self.assertTrue(ep.is_healthy(sal))
    def testNotHealthy(self):
        bob = create_bob()
        self.assertFalse(ep.is_healthy(bob))

    def testContagious(self):
        azi = create_azi()
        self.assertTrue(ep.is_contagious(azi))

    def testSamePerson(self):
        azi = create_azi()
        self.assertIs(azi,azi)

    def test_cordinates(self):
        # this should not work yet as Aziz doesn't have a pos yet but the problem should be caught. 
        azi = create_azi()
        self.assertIsNotNone(azi.get_x())
        self.assertIsNotNone(azi.get_y())
 
    def test_main(self):
        self.assertEqual(ep.main(), 0)


if __name__ == '__main__':
    main()

