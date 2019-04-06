"""
This is the test suite for agent.py.
"""

from unittest import TestCase, main

from indra.agent import Agent, ratio_to_sin, NEUTRAL

LEIBBYEAR = 1646
LEIBDYEAR = 1716
ANM = "age"
AGE = 141.0


def newt_action(agent):
    print("I'm " + agent.name + " and I'm inventing modern mechanics!")


def leib_action(agent):
    print("I'm " + agent.name + " and I'm inventing calculus!")


def ram_action(agent):
    print("I'm " + agent.name + " and my duration is only: " +
          str(agent.duration))


def create_leibniz():
    return Agent("Leibniz",
                  attrs={"place": 0.0, "time": LEIBBYEAR},
                  action=leib_action,
                  duration=20)


def create_other_leibniz():
    return Agent("Leibniz",
                  attrs={"place": 1.0, "time": LEIBBYEAR},
                  action=leib_action,
                  duration=20)


def create_newton():
    return Agent("Newton",
                  attrs={"place": 0.0, "time": 1658.0, "achieve": 43.9},
                  action=newt_action,
                  duration=30)


def create_hardy():
    return Agent("Hardy",
                  attrs={ANM: AGE},
                  duration=10)


def create_ramanujan():
    return Agent("Ramanujan", duration=5, action=ram_action)


def create_littlewood():
    return Agent("Littlewood",
                 attrs={"friend": 141.0, "number": 1729.0})


def create_ramsey():
    return Agent("Ramsey",
                 attrs={"friend": 282.9, "number": 3.14})


class AgentTestCase(TestCase):
    def setUp(self):
        self.leib = create_leibniz()
        self.newt = create_newton()
        self.hardy = create_hardy()

    def tearDown(self):
        self.leib = None
        self.newt = None
        self.hardy = None

    def test_eq(self):
        """
        Test if two agents are equal.
        """
        l2 = create_leibniz()
        l3 = create_other_leibniz()
        self.assertTrue(self.leib == l2)
        self.assertNotEqual(self.leib, self.newt)
        self.assertNotEqual(self.leib, l3)
        # change a field and see that they aren't equal:
        l2["place"] = 1.0
        self.assertNotEqual(self.leib, l2)

    def test_str(self):
        """
        Test string rep of an agent.
        """
        ent = create_ramanujan()
        self.assertEqual("Ramanujan", str(ent))

    def test_repr(self):
        rep = ('{\n    "name": "Hardy",'
               + '\n    "duration": 10,'
               + '\n    "pos": null,'
               + '\n    "attrs": '
               + '{\n        "' + ANM + '": ' + str(AGE)
               + '\n    },'
               + '\n    "groups": ""\n}')
        self.assertEqual(rep, repr(self.hardy))

    def test_len(self):
        self.assertEqual(len(create_newton()), 3)

    def test_get(self):
        self.assertEqual(self.leib["time"], LEIBBYEAR)
        # self.assertEqual(self.leib["time"], 0)  # just testing travis ci
        # testing

    def test_set(self):
        """
        We're testing agent set.
        """
        self.leib["time"] = LEIBDYEAR
        self.assertEqual(self.leib["time"], LEIBDYEAR)
        self.newt["place"] = 57.345
        self.assertEqual(self.newt["place"], 57.345)

    def test_contains(self):
        ent = create_leibniz()
        s = "place"
        self.assertTrue(s in ent)

    def test_type(self):
        l1 = create_leibniz()
        l2 = create_other_leibniz()
        n = create_newton()
        self.assertTrue(l1.same_type(l2))
        self.assertFalse(l1.same_type(n))

    def test_iter(self):
        l1 = create_leibniz()
        s = ''
        for attr in l1:
            s += attr
        self.assertEqual(s, "placetime")

    def test_reversed(self):
        l1 = create_leibniz()
        s = ''
        for attr in reversed(l1):
            s += attr
        self.assertEqual(s, "timeplace")

    def test_imul(self):
        h = create_hardy()
        h *= 2.0
        self.assertEqual(h[ANM], AGE * 2.0)

    def test_iadd(self):
        h = create_hardy()
        h += 2.0
        self.assertEqual(h[ANM], AGE + 2.0)

    def test_isub(self):
        h = create_hardy()
        h -= 2.0
        self.assertEqual(h[ANM], AGE - 2.0)

    def test_magnitude(self):
        h = create_hardy()
        self.assertEqual(h.magnitude(), AGE)

    def test_sum(self):
        n = create_newton()
        tsum = sum(n[k] for k in n)
        self.assertAlmostEqual(n.sum(), tsum)

    def test_ratio_to_sin(self):
        self.assertEqual(ratio_to_sin(0), 0)
        self.assertEqual(ratio_to_sin(1), 1)
        self.assertAlmostEqual(ratio_to_sin(.5), NEUTRAL)

if __name__ == '__main__':
    main()
