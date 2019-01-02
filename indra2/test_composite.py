"""
This is the test suite for entity.py.
"""

import numpy
import json

from unittest import TestCase, main

from composite import Composite


class CompositeTestCase(TestCase):
    def test_eq(self):
        pass

    def test_str(self):
        name = "Ramanujan"
        c = Composite(name)
        self.assertEqual(name, str(c))

    def test_repr(self):
        # self.assertEqual(rep, repr(ent))
        pass

    def test_len(self):
        # self.assertEqual(len(ent), 3)
        pass

    def test_get(self):
        # self.assertEqual(ent["time"], leibbyear)
        pass

    def test_set(self):
        # self.assertEqual(ent["time"], leibdyear)
        pass

    def test_contains(self):
        # self.assertTrue(s in ent)
        pass

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
