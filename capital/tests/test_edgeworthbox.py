"""
This is the test suite for drunks.py.
"""

from unittest import TestCase, main

import capital.edgeworthbox as edge


class EdgeworthboxTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_gen_util_func(self):
        util = edge.gen_util_func(0)
        self.assertEqual(util, edge.DEF_MAX_UTIL)

    def test_trade(self):
        pass


    def test_rec_offer(self):
        pass


    def test_utility_delta(self):
        agent = edge.create_cagent('Cheese holders', 0)
        agent["goods"]["cheese"]["endow"] = 4
        change = edge.utility_delta(agent, "cheese", 1)
        self.assertEqual(change, -0.5)


    def test_adj_add_good(self):
        pass


    def test_create_wagent(self):
        agent = edge.create_cagent('Wine holders', 0)
        name = agent.name
        camt = agent["goods"]["cheese"]["endow"]
        wamt = agent["goods"]["wine"]["endow"]
        self.assertEqual(name, "Wine holders0")
        self.assertEqual(camt, edge.DEF_NUM_CHEESE)
        self.assertEqual(wamt, 0)


    def test_create_cagent(self):
        agent = edge.create_cagent('Cheese holders',0)
        name = agent.name
        camt = agent["goods"]["cheese"]["endow"]
        wamt = agent["goods"]["wine"]["endow"]
        self.assertEqual(name, "Cheese holders0")
        self.assertEqual(camt, edge.DEF_NUM_CHEESE)
        self.assertEqual(wamt, 0)

    if __name__ == '__main__':
        main()
