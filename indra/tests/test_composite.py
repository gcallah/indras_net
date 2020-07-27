"""
This is the test suite for composite.py.
"""

from IPython import embed
from unittest import TestCase, main, skip

from indra.agent import join, split, switch
from indra.composite import Composite
from indra.tests.test_agent import create_hardy, create_newton
from indra.tests.test_agent import create_ramanujan, create_littlewood
from indra.tests.test_agent import create_ramsey, create_leibniz

N = "Newton"
R = "Ramanujan"
L = "Leibniz"
H = "Hardy"
NL = N + L
LN = L + N
HR = H + R
LR = "LittlewoodRamsey"

CALC_GUYS = "Calculus guys"


def match_name(agent, name):
    return agent.name == name


def max_duration(agent, duration):
    return agent.duration <= duration


def create_calcguys(members=[create_newton(), create_leibniz()]):
    return Composite(CALC_GUYS, members=members)


def create_cambguys():
    return Composite("Cambridge guys", members=[create_hardy(),
                                                create_ramanujan()])


def create_cambguys2():
    return Composite("Other Cambridge guys",
                     members=[create_littlewood(), create_ramsey()])


def create_mathgrp():
    return Composite("Math groups",
                     members=[create_calcguys(), create_cambguys()])


def create_mathguys():
    mathguys = create_calcguys() + create_cambguys()
    return mathguys


def create_mem_str(comp):
    s = ""
    for agent in comp:
        s += agent  # this will collect the names of the members
    return s


def print_mem_str(comp):
    print(create_mem_str(comp))


class CompositeTestCase(TestCase):
    def setUp(self):
        self.hardy = create_hardy()
        self.newton = create_newton()
        self.calc = create_calcguys(members=[self.newton, create_leibniz()])
        self.camb = create_cambguys()
        self.mathgrp = create_mathgrp()
        self.mathguys = create_mathguys()

    def tearDown(self):
        self.hardy = None
        self.newton = None
        self.calc = None
        self.camb = None
        self.mathgrp = None
        self.mathguys = None

    def test_ismember(self):
        self.assertTrue(self.calc.ismember(self.newton))

    def test_eq(self):
        self.assertEqual(self.calc, self.calc)
        self.assertNotEqual(self.camb, self.calc)

    def test_str(self):
        name = "Ramanujan"
        c = Composite(name)
        self.assertEqual(name, str(c))

    def test_repr(self):
        # this test has to be written!
        # self.assertEqual(rep, repr(agent))
        pass

    def test_len(self):
        self.assertEqual(len(self.camb), 2)

    def test_get(self):
        self.assertEqual(self.camb[H], self.hardy)

    def test_set(self):
        self.camb[str(self.newton)] = self.newton
        self.assertEqual(self.camb[str(self.newton)], self.newton)

    def test_contains(self):
        self.assertTrue(H in self.camb)

    def test_iter(self):
        self.assertEqual(create_mem_str(self.calc), NL)

    def test_reversed(self):
        s = ""
        for guy in reversed(self.calc):
            s += guy
        self.assertEqual(s, LN)

    def test_mul(self):
        self.camb += self.newton
        math_inter = self.calc * self.camb
        print_mem_str(math_inter)
        self.assertEqual(create_mem_str(math_inter), N)

    def test_imul(self):
        self.assertEqual(create_mem_str(self.mathguys), NL + HR)
        self.mathguys *= self.camb  # should drop out calc!
        self.assertEqual(create_mem_str(self.mathguys), HR)

    def test_add(self):
        self.assertEqual(create_mem_str(self.mathguys), NL + HR)
        self.mathguys = self.calc + self.camb + create_cambguys2()
        self.assertEqual(create_mem_str(self.mathguys), NL + HR + LR)
        # ensure we did not change original group:
        self.assertEqual(create_mem_str(self.calc), NL)
        # let's make sure set union does not dupe members:
        camb_self_union = self.camb + self.camb
        self.assertEqual(create_mem_str(camb_self_union), HR)
        # now let's add an atom rather than a composite:
        self.calch = self.calc + self.hardy
        self.assertEqual(create_mem_str(self.calch), NL + H)

    def test_iadd(self):
        # let's make sure set union does not dupe members:
        self.camb += self.camb
        self.assertEqual(create_mem_str(self.camb), HR)
        # now test adding new members:
        self.camb += create_cambguys2()
        self.assertEqual(create_mem_str(self.camb), HR + LR)
        # now test adding an atomic entity:
        self.camb += create_newton()
        self.assertEqual(create_mem_str(self.camb), HR + LR + N)

    def test_sub(self):
        mathguys = self.calc + self.camb + create_cambguys2()
        cambguys = mathguys - self.calc
        self.assertEqual(create_mem_str(cambguys), HR + LR)
        # now test deleting an atom:
        hardygone = cambguys - self.hardy
        self.assertEqual(create_mem_str(hardygone), R + LR)
        # make sure we didn't change original group:
        self.assertEqual(create_mem_str(cambguys), HR + LR)
        # delete something that ain't there:
        cambguys = cambguys - self.calc
        self.assertEqual(create_mem_str(cambguys), HR + LR)

    def test_isub(self):
        maths = self.calc + self.camb + create_cambguys2()
        maths -= self.calc
        self.assertEqual(create_mem_str(maths), HR + LR)
        # now test deleting an atom:
        maths -= self.hardy
        self.assertEqual(create_mem_str(maths), R + LR)

    def test_call(self):
        (acts, moves) = self.mathgrp()
        self.assertEqual(acts, 3)  # hardy is passive!

    def test_subset(self):
        just_n = self.calc.subset(match_name, str(self.newton), name="Just Newton!")
        self.assertEqual(create_mem_str(just_n), N)
        just_l = self.calc.subset(max_duration, 25, name="Just Leibniz!")
        self.assertEqual(create_mem_str(just_n), N)

    def test_rand_member(self):
        rand_guy = self.calc.rand_member()
        self.assertIsNotNone(rand_guy)
        empty_set = Composite("Empty")
        rand_guy = empty_set.rand_member()
        self.assertIsNone(rand_guy)

    def test_magnitude(self):
        pass

    def test_is_mbr_comp(self):
        self.assertTrue(self.mathgrp.is_mbr_comp(CALC_GUYS))
        self.assertFalse(self.calc.is_mbr_comp(str(self.newton)))

    def test_pop_count(self):
        self.assertEqual(self.mathgrp.pop_count(CALC_GUYS), 2)
        self.assertEqual(self.calc.pop_count(str(self.newton)), 1)

    def test_leave_group(self):
        """
        Test leaving a group.
        This test is here rather than in agent because it requires Composite!
        """
        split(self.calc, self.newton)
        self.assertEqual(create_mem_str(self.calc), L)

    def test_join_group(self):
        """
        Test joining a group.
        This test is here rather than in agent because it requires Composite!
        """
        join(self.calc, self.hardy)
        self.assertEqual(create_mem_str(self.calc), NL + H)

    @skip("switch() seems to work in models but not in test!")
    def test_switch_groups(self):
        """
        Test switching groups.
        This test is here rather than in agent because it requires Composite!
        """
        switch(self.hardy.name, self.camb.name, self.calc.name)
        self.assertIn(str(self.hardy), self.calc)


if __name__ == '__main__':
    main()
