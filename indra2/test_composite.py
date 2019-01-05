"""
This is the test suite for entity.py.
"""

from collections import OrderedDict

from unittest import TestCase, main

from composite import Composite
from test_entity import create_hardy, create_newton, create_leibniz
from test_entity import create_ramanujan, create_littlewood


def create_calcguys():
    n = create_newton()
    l = create_leibniz()
    mems = OrderedDict([(n.name, n), (l.name, l)])
    return Composite("Calculus guys", members=mems)


def create_cambguys():
    h = create_hardy()
    r = create_ramanujan()
    mems = OrderedDict([(h.name, h), (r.name, r)])
    return Composite("Cambridge guys", members=mems)


def create_mathguys():
    calc = create_calcguys()
    camb = create_cambguys()
    mems = OrderedDict([(calc.name, calc), (camb.name, camb)])
    return Composite("Math guys", members=mems)


class CompositeTestCase(TestCase):
    def test_eq(self):
        calc1 = create_calcguys()
        camb = create_cambguys()
        print("calc1 = " + calc1.__repr__())
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

    def test_enttype(self):
        # self.assertTrue(l1.same_type(l2))
        # self.assertFalse(l1.same_type(n))
        pass

    def test_iter(self):
        # self.assertEqual(s, "placetime")
        pass

    def test_reversed(self):
        # self.assertEqual(s, "timeplace")
        pass

    def test_imul(self):
        # self.assertEqual(h[ANM], AGE * 2.0)
        pass

    def test_iadd(self):
        # self.assertEqual(h[ANM], AGE + 2.0)
        pass

    def test_isub(self):
        # self.assertEqual(h[ANM], AGE - 2.0)
        pass

    def test_magnitude(self):
        # self.assertEqual(h.magnitude(), AGE)
        pass


if __name__ == '__main__':
    main()
