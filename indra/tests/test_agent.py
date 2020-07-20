"""
This is the test suite for agent.py.
"""

from unittest import TestCase, main, skip

from indra.agent import Agent, ratio_to_sin, NEUTRAL
from indra.agent import prob_state_trans, set_trans

REP_RAND_TESTS = 20

LEIBBYEAR = 1646
LEIBDYEAR = 1716
ANM = "age"
AGE = 141.0

STATE_TRANS = [
    [.98, .02, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, .96, .04],
    [1.0, 0.0, 0.0, 0.0],
]


def newt_action(agent, **kwargs):
    print("I'm " + agent.name + " and I'm inventing modern mechanics!")


def leib_action(agent, **kwargs):
    print("I'm " + agent.name + " and I'm inventing calculus!")


def ram_action(agent, **kwargs):
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

    def test_len(self):
        """
        See if we get the agent's len correct.
        """
        self.assertEqual(len(create_newton()), 3)

    def test_get(self):
        """
        Get a named attribute from an agent.
        """
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

    def test_iter(self):
        l1 = create_leibniz()
        s = ''
        for attr in l1:
            s += attr
        self.assertEqual(s, "placetime")

    def test_ratio_to_sin(self):
        self.assertEqual(ratio_to_sin(0), 0)
        self.assertEqual(ratio_to_sin(1), 1)
        self.assertAlmostEqual(ratio_to_sin(.5), NEUTRAL)

    def test_prob_state_trans(self):
        global STATE_TRANS

        for i in range(REP_RAND_TESTS):
            new_state = prob_state_trans(0, STATE_TRANS)
            self.assertNotEqual(new_state, 2)
            self.assertNotEqual(new_state, 3)
            new_state = prob_state_trans(1, STATE_TRANS)
            self.assertEqual(new_state, 2)
            new_state = prob_state_trans(2, STATE_TRANS)
            self.assertNotEqual(new_state, 0)
            self.assertNotEqual(new_state, 1)
            new_state = prob_state_trans(3, STATE_TRANS)
            self.assertEqual(new_state, 0)

    def test_set_trans(self):
        """
        Tests re-setting a probability.
        We're going to switch 2 probs, then put 'em
        back, so we don't break above test.
        """
        global STATE_TRANS

        prob1 = STATE_TRANS[0][0]
        prob2 = STATE_TRANS[0][1]
        set_trans(STATE_TRANS, 0, 0, prob2, 1)
        self.assertAlmostEqual(STATE_TRANS[0][0], prob2)
        self.assertAlmostEqual(STATE_TRANS[0][1], prob1)
        # now set 'em back:
        set_trans(STATE_TRANS, 0, 0, prob1, 1)
        self.assertAlmostEqual(STATE_TRANS[0][0], prob1)
        self.assertAlmostEqual(STATE_TRANS[0][1], prob2)


if __name__ == '__main__':
    main()
