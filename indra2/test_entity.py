"""
This is the test suite for entity.py.
"""

import json

from unittest import TestCase, main

from entity import Entity, NAME_ID, SEP

leibbyear = 1646
leibdyear = 1716

def create_leibniz():
    name = "Leibniz"
    attrs = {"place": 0.0, "time": leibbyear}
    return Entity(name, attrs)

class EntityTestCase(TestCase):
    def test_str(self):
        name = "Ramanujan"
        ent = Entity(name)
        self.assertEqual(name, str(ent))

    def test_repr(self):
        name = "Hardy"
        age_nm = "age"
        age = 141.0
        attrs = {age_nm: age}
        ent = Entity(name, attrs)
        rep = '{"name": "Hardy", "attrs": {"age": 141.0}}'
        self.assertEqual(rep, repr(ent))

    def test_len(self):
        name = "Newton"
        attrs = {"place": 0.0, "time": 1658.0}
        ent = Entity(name, attrs)
        self.assertEqual(len(ent), 2)

    def test_get(self):
        ent = create_leibniz()
        self.assertEqual(ent["time"], leibbyear)

    def test_set(self):
        ent = create_leibniz()
        ent["time"] = leibdyear
        self.assertEqual(ent["time"], leibdyear)

    def test_contains(self):
        ent = create_leibniz()
        s = "place"
        return ent[s]

if __name__ == '__main__':
    main()
