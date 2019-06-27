from unittest import TestCase, main
from indra.agent import Agent
from indra.composite import Composite
from indra.space import Space
from indra.env import Env
from models.sandpile import set_up, create_agent, get_next_group_idx
from models.sandpile import get_curr_group_idx, change_group, add_grain, topple, sandpile_action, place_action
from models.sandpile import NUM_GROUPS
import models.sandpile as sp

TEST_ANUM = 999999

REP_RAND_TESTS = 20

SMALL_GRID = 4

sandpile = None

class SandpileTestCase(TestCase):
    def setUp(self):
        # (sp.groups, sp.group_indices, sp.sandpile) = set_up()
        #self.test_agent = create_agent(TEST_ANUM, TEST_ANUM)
        (sp.groups, sp.group_indices, sp.sandpile) = set_up()
        pass

    def tearDown(self):
        self.test_agent = None
        sp.groups = None
        sp.group_indices = None
        sp.sandpile = None
        pass

    def test_create_agent(self):
        agent = create_agent(TEST_ANUM, TEST_ANUM)
        test_name = "(" + str(TEST_ANUM) + "," + str(TEST_ANUM) + ")"
        self.assertEqual(agent.name, test_name)

    def test_get_curr_group_idx(self):
        a = create_agent(TEST_ANUM, TEST_ANUM)
        sp.groups = []
        sp.groups.append(Composite("Group" + str(0)))
        sp.groups[0]+= a
        self.assertEqual(get_curr_group_idx(a), 0)

    def test_get_next_group_idx(self):
        a = create_agent(TEST_ANUM, TEST_ANUM)
        self.assertEqual(get_next_group_idx(0), 1)

    def test_change_group(self):
       a = create_agent(TEST_ANUM, TEST_ANUM)
       sp.groups = []
       sp.groups.append(Composite("Group" + str(0)))
       sp.groups.append(Composite("Group" + str(1)))
       sp.groups[0] += a
       change_group(a, sp.sandpile, 0, 1)
       self.assertEqual(get_curr_group_idx(a), 1)

    def test_add_grain(self):
        a = create_agent(TEST_ANUM, TEST_ANUM)
        sp.groups = []
        sp.groups.append(Composite("Group" + str(0)))
        sp.groups.append(Composite("Group" + str(1)))
        sp.groups[0] += a
        add_grain(sp.sandpile, a)
        self.assertEqual(a.primary_group(), sp.groups[1])

    # def test_topple(self):
    #     a = create_agent(TEST_ANUM, TEST_ANUM)
    #     b = create_agent(TEST_ANUM - 1, TEST_ANUM)
    #     c = create_agent(TEST_ANUM + 1, TEST_ANUM)
    #     sp.groups = []
    #     sp.groups.append(Composite("Group" + str(0)))
    #     sp.groups.append(Composite("Group" + str(1)))
    #     sp.groups[0] += b
    #     sp.groups[0] += c
    #     sp.groups[1] += a
    #     neighbors = []
    #     neighbors.append(b)
    #     neighbors.append(c)
    #     a.neighbors = neighbors
    #     topple(sp.sandpile, a)
    #     self.assertEqual(a.primary_group(), sp.groups[1])
    #     self.assertEqual(b.primary_group(), sp.groups[1])
    #     self.assertEqual(c.primary_group(), sp.groups[1])

    def test_sandpile_action(self):
        sandpile_action(sp.sandpile)
        self.assertEqual(sp.sandpile.attrs["center_agent"].primary_group(), sp.groups[1])

    # def test_place_action(self):
    #     a = create_agent(TEST_ANUM, TEST_ANUM)
    #     b = create_agent(TEST_ANUM - 1, TEST_ANUM)
    #     c = create_agent(TEST_ANUM + 1, TEST_ANUM)
    #     d = create_agent(TEST_ANUM, TEST_ANUM - 1)
    #     e = create_agent(TEST_ANUM, TEST_ANUM + 1)
    #     sp.groups = []
    #     sp.groups.append(Composite("Group" + str(0)))
    #     sp.groups[0] += a
    #     sp.groups[0] += b
    #     sp.groups[0] += c
    #     sp.groups[0] += d
    #     sp.groups[0] += e
    #     sp.sandpile = Env("Sandpile", members=sp.groups)
    #     lst = []
    #     neighbors_dict = {"neighbors": lst}
    #     neighbors_dict["neighbors"].append(b)
    #     neighbors_dict["neighbors"].append(c)
    #     neighbors_dict["neighbors"].append(d)
    #     neighbors_dict["neighbors"].append(e)
    #     neighbors_composite = grp_from_nm_dict("Vonneuman neighbors", neighbors_dict["neighbors"])
    #     place_action(sp.sandpile, a)
    #     self.assertEqual(a.neighbors, neighbors_composite)
