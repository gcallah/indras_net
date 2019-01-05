"""
This is the test suite for entity.py.
"""

from collections import OrderedDict

from unittest import TestCase, main

from composite import Composite
from test_entity import create_hardy, create_newton, create_leibniz
from test_entity import create_ramanujan, create_littlewood, create_ramsey

NL = "NewtonLeibniz"
LN = "LeibnizNewton"
HR = "HardyRamanujan"
LR = "LittlewoodRamsey"

def create_calcguys():
    n = create_newton()
    l = create_leibniz()
    return Composite("Calculus guys",
                     members=OrderedDict([(n.name, n), (l.name, l)]))


def create_cambguys():
    h = create_hardy()
    r = create_ramanujan()
    return Composite("Cambridge guys",
                     members=OrderedDict([(h.name, h), (r.name, r)]))


def create_cambguys2():
    l = create_littlewood()
    r = create_ramsey()
    return Composite("Other Cambridge guys",
                     members=OrderedDict([(l.name, l), (r.name, r)]))


def create_mathguys():
    calc = create_calcguys()
    camb = create_cambguys()
    return Composite("Math guys",
                     members=OrderedDict([(calc.name, calc),
                                          (camb.name, camb)]))


class CompositeTestCase(TestCase):
    def test_eq(self):
        calc1 = create_calcguys()
        camb = create_cambguys()
        self.assertEqual(calc1, calc1)
        self.assertNotEqual(camb, calc1)

    def test_str(self):
        name = "Ramanujan"
        c = Composite(name)
        self.assertEqual(name, str(c))

    def test_repr(self):
        # self.assertEqual(rep, repr(ent))
        pass

    def test_len(self):
        camb = create_cambguys()
        self.assertEqual(len(camb), 2)

    def test_get(self):
        camb = create_cambguys()
        self.assertEqual(camb["Hardy"], create_hardy())

    def test_set(self):
        camb = create_cambguys()
        camb["jel"] = create_littlewood()
        self.assertEqual(camb["jel"], create_littlewood())

    def test_contains(self):
        camb = create_cambguys()
        self.assertTrue("Hardy" in camb)

    def test_iter(self):
        calc = create_calcguys()
        s = ""
        for guy in calc:
            s += guy
        self.assertEqual(s, NL)

    def test_reversed(self):
        calc = create_calcguys()
        s = ""
        for guy in reversed(calc):
            s += guy
        self.assertEqual(s, LN)

    def test_imul(self):
        # self.assertEqual(h[ANM], AGE * 2.0)
        pass

    def test_add(self):
        calc = create_calcguys()
        camb = create_cambguys()
        mathguys = calc + camb
        s = ""
        for mathwiz in mathguys:
            s += mathwiz
        self.assertEqual(s, NL + HR)
        camb2 = create_cambguys2()
        mathguys = calc + camb + camb2
        s = ""
        for mathwiz in mathguys:
            s += mathwiz
        self.assertEqual(s, NL + HR + LR)

    def test_iadd(self):
        camb = create_cambguys()
        camb2 = create_cambguys2()
        camb += camb2
        s = ""
        for cambwiz in camb:
            s += cambwiz
        self.assertEqual(s, HR + LR)

    def test_sub(self):
        calc = create_calcguys()
        camb = create_cambguys()
        camb2 = create_cambguys2()
        mathguys = calc + camb + camb2
        s = ""
        cambguys = mathguys - calc
        for cambwiz in cambguys:
            s += cambwiz
        self.assertEqual(s, HR + LR)


    def test_isub(self):
        pass

    def test_magnitude(self):
        pass


if __name__ == '__main__':
    main()
