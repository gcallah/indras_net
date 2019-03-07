"""
This is the test suite for composite.py.
"""

from unittest import TestCase, main

from indra2.composite import Composite
from indra2.tests.test_agent import create_hardy, create_newton
from indra2.tests.test_agent import create_ramanujan, create_littlewood
from indra2.tests.test_agent import create_ramsey, create_leibniz

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


def create_calcguys():
    return Composite(CALC_GUYS, members=[create_newton(),
                                               create_leibniz()])


def create_cambguys():
    return Composite("Cambridge guys", members=[create_hardy(),
                                                create_ramanujan()])


def create_cambguys2():
    return Composite("Other Cambridge guys",
                     members=[create_littlewood(), create_ramsey()])


def create_mathguys():
    return Composite("Math guys",
                     members=[create_calcguys(), create_cambguys()])

def create_mem_str(comp):
    s = ""
    for agent in comp:
        s += agent  # this will collect the names of the members
    return s


class CompositeTestCase(TestCase):
    def setUp(self):
        self.calc = create_calcguys()
        self.camb = create_cambguys()
        self.hardy = create_hardy()

    def tearDown(self):
        self.calc = None
        self.camb = None
        self.hardy = None

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
        self.assertEqual(self.camb["Hardy"], self.hardy)

    def test_set(self):
        self.camb["jel"] = create_littlewood()
        self.assertEqual(self.camb["jel"], create_littlewood())

    def test_contains(self):
        self.assertTrue("Hardy" in self.camb)

    def test_iter(self):
        self.assertEqual(create_mem_str(self.calc), NL)

    def test_reversed(self):
        s = ""
        for guy in reversed(self.calc):
            s += guy
        self.assertEqual(s, LN)

    def test_mul(self):
        newt = create_newton()
        self.camb[newt.name] = newt
        mathguys = self.calc * self.camb
        self.assertEqual(create_mem_str(mathguys), N)

    def test_imul(self):
        mathguys = self.calc + self.camb
        self.assertEqual(create_mem_str(mathguys), NL + HR)
        mathguys *= self.camb  # should drop out calc!
        self.assertEqual(create_mem_str(mathguys), HR)

    def test_add(self):
        mathguys = self.calc + self.camb
        self.assertEqual(create_mem_str(mathguys), NL + HR)
        mathguys = self.calc + self.camb + create_cambguys2()
        self.assertEqual(create_mem_str(mathguys), NL + HR + LR)
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
        mathguys = self.calc + self.camb + create_cambguys2()
        mathguys -= self.calc
        self.assertEqual(create_mem_str(mathguys), HR + LR)
        # now test deleting an atom:
        mathguys -= self.hardy
        self.assertEqual(create_mem_str(mathguys), R + LR)

    def test_call(self):
        mathguys = self.camb + create_calcguys()
        acts = mathguys()
        self.assertEqual(acts, 3)  # hardy is passive!

    def test_subset(self):
        just_n = self.calc.subset(match_name, "Newton", name="Just Newton!")
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
        math_guys = create_mathguys()
        self.assertTrue(math_guys.is_mbr_comp(CALC_GUYS))
        self.assertFalse(self.calc.is_mbr_comp("Newton"))

    def test_pop_count(self):
        math_guys = create_mathguys()
        self.assertEqual(math_guys.pop_count(CALC_GUYS), 2)
        self.assertEqual(self.calc.pop_count("Newton"), 1)

if __name__ == '__main__':
    main()
