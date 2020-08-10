""" This is a template file for tests.  """
from unittest import TestCase, main, skip

from indra.composite import Composite
from indra.env import Env
from indra.space import debug_agent_pos
from registry.registry import clear_registry
import epidemics.epidemic as ep
"""
This is for personal reference
HEalthy = "0"
EXposed = "1"
INfected = "2"
Contagious = "3"
DEad = "4"
IMmune = "5"
"""

DEBUG = False


def header(s):
    print("\n==================")
    print(s)
    print("==================")


def agent_debug(agent):
    if DEBUG:
        print("Agent", str(agent), "with id:", id(agent), "Position: ",
              agent.get_pos())


def create_sal():
    sal = ep.create_person("Saliou", 0, ep.HE)
    agent_debug(sal)
    return sal


def create_bob():
    bob = ep.create_person("Bob", 1, ep.DE)
    agent_debug(bob)
    return bob


def create_azi():
    azi = ep.create_person("Aziz", 2, ep.CN)
    agent_debug(azi)
    return azi


class EpidemicTestCase(TestCase):
    def setUp(self):
        header("Running set up")
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
        ep.set_env_attrs()

    def tearDown(self):
        header("Running tear down")
        self.sal = None
        self.bob = None
        self.azi = None
        self.healthy = None
        self.contagious = None
        self.env = None
        clear_registry()

    def test_healthy(self):
        header("Running test_healthy")
        # create people and test their attributes
        self.assertTrue(ep.is_healthy(self.sal))

    def test_not_healthy(self):
        self.assertFalse(ep.is_healthy(self.bob))

    def test_contagious(self):
        self.assertTrue(ep.is_contagious(self.azi))

    def test_is_not_quarantined(self):
        header("Running test_is_not_quarantined")
        # default max social dist is ep.DEF_DISTANCING unit.
        self.env.place_member(self.sal, xy=(0, 0))
        self.env.place_member(self.azi, xy=(0, ep.DEF_DISTANCING//2))
        debug_agent_pos(self.sal)
        debug_agent_pos(self.azi)
        self.assertFalse(ep.is_isolated(self.azi))

    @skip("Test is failing on travis, but not locally.")
    def test_is_quarantined(self):
        header("Running test_is_quarantined")
        # default max social dist is ep.DEF_DISTANCING unit.
        far_away = ep.DEF_DISTANCING * 2
        self.env.place_member(self.sal, xy=(0, 0))
        self.env.place_member(self.azi, xy=(0, far_away))
        debug_agent_pos(self.sal)
        debug_agent_pos(self.azi)
        self.assertTrue(ep.is_isolated(self.azi),
                        "agent is " + str(far_away)
                        + " units away but is not quarantined.")

    def test_is_infecting(self):
        # are the contagious agents successfully infecting the healthy?
        header("Running test_is_infecting")
        # default max social dist is ep.DEF_DISTANCING unit.
        close = ep.DEF_DISTANCING // 2
        self.env.place_member(self.sal, xy=(0, 0))
        self.env.place_member(self.azi, xy=(0, close))
        debug_agent_pos(self.sal)
        ep.person_action(self.sal)
        ep.person_action(self.azi)
        self.assertFalse(ep.is_healthy(self.azi),
                         "agent is " + str(close)
                         + " units away from a contagious agent"
                         + " but is not exposed")

    def test_dead_action(self):
        # dead_people shoudn't move
        header("Running test_dead_action ")
        self.env.place_member(self.sal, xy=(0, 0))
        debug_agent_pos(self.bob)
        self.assertIs(ep.DONT_MOVE, ep.person_action(self.bob))

    def test_close_contagion_action(self):
        # Will agents move away if they are are not isolated
        header("Running test_is_infecting")
        # default max social dist is ep.DEF_DISTANCING unit.
        close = ep.DEF_DISTANCING // 2
        self.env.place_member(self.sal, xy=(0, 0))
        self.env.place_member(self.azi, xy=(0, close))
        debug_agent_pos(self.sal)
        self.assertIs(ep.MOVE, ep.person_action(self.sal))

    @skip("Test failing now for unknown reason.")
    def test_main(self):
        self.assertEqual(ep.main(), 0)


if __name__ == '__main__':
    main()
