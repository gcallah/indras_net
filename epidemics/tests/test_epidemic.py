""" This is a template file for tests.  """
from unittest import TestCase, main, skip

from indra.composite import Composite
from indra.env import Env
from indra.space import debug_agent_pos
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
    print("Creating Saliou0")
    return ep.create_person("Saliou", 0, ep.HE)


def create_bob():
    return ep.create_person("Bob", 1, ep.IN)


def create_azi():
    print("Creating Aziz2")
    return ep.create_person("Aziz", 2, ep.CN)


class EpidemicTestCase(TestCase):
    def setUp(self):
        groups = []
        self.sal = create_sal()
        self.bob = create_bob()
        self.azi = create_azi()

        # create customized enviroment
        self.healthy = Composite(ep.HEALTHY, members=[self.sal])
        groups.append(self.healthy)
        groups.append(Composite(ep.EXPOSED, state=ep.EX))
        self.contagious = Composite(ep.CONTAGIOUS)
        groups.append(self.contagious)
        groups.append(Composite(ep.INFECTED, members=[self.bob]))
        groups.append(Composite(ep.CONTAGIOUS, members=[self.azi]))
        groups.append(Composite(ep.DEAD))
        groups.append(Composite(ep.IMMUNE))

        self.env = Env("Test env", height=20, width=20, members=groups)
        # you could do this also:
        # self.exposed = self.env[ep.EXPOSED]
        ep.set_env_attrs()

    def tearDown(self):
        self.sal = None
        self.bob = None
        self.azi = None
        self.healthy = None
        self.contagious = None
        self.env = None

    @skip("Trying to fix is quarantined.")
    def test_healthy(self):
        # create people and test their attrubutes
        self.assertTrue(ep.is_healthy(self.sal))

    @skip("Trying to fix is quarantined.")
    def test_not_healthy(self):
        self.assertFalse(ep.is_healthy(self.bob))

    @skip("Trying to fix is quarantined.")
    def test_contagious(self):
        self.assertTrue(ep.is_contagious(self.azi))

    @skip("Trying to fix is quarantined.")
    def test_same_person(self):
        self.assertIs(self.azi, self.azi)

    @skip("Trying to fix is quarantined.")
    def test_not_same_agent(self):
        self.assertIsNot(self.azi, self.bob)

    @skip("environment problem, need to clear region to test isolation")
    def test_is_not_quarantined(self):
        # default max social dist is ep.DEF_DISTANCING unit.
        self.env.place_member(self.sal, xy=(0, 0))
        self.env.place_member(self.azi, xy=(0, 1))
        debug_agent_pos(self.sal)
        debug_agent_pos(self.azi)
        self.assertFalse(ep.is_isolated(self.azi))

    @skip("environment problem,  The distance is returning zero despite suifficient unit distance between agents")
    def test_is_quarantined(self):
        # default max social dist is ep.DEF_DISTANCING unit.
        far_away = ep.DEF_DISTANCING * 2
        self.env.place_member(self.sal, xy=(0, 0))
        self.env.place_member(self.azi, xy=(0, far_away))
        self.assertTrue(ep.is_isolated(self.azi),
                        "agent is " + str(far_away)
                        + " units away but is not quarantined")

    @skip("Trying to fix is quarantined.")
    def test_main(self):
        self.assertEqual(ep.main(), 0)


if __name__ == '__main__':
    main()
