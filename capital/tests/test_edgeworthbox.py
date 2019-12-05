"""
This is the test suite for edgeworthbox.py.
"""

from unittest import TestCase, main

import capital.edgeworthbox as edge
from capital.trade_utils import seek_a_trade, gen_util_func
import capital.trade_utils as tu


class EdgeworthboxTestCase(TestCase):
    def setUp(self, props=None):
        self.pa = edge.get_props("edgeworthbox", props, model_dir="capital")
        (edge.market, edge.cheese_group, edge.wine_group, edge.max_util) = edge.set_up()

    def tearDown(self):
        (edge.market, edge.cheese_group, edge.wine_group, edge.max_util) = (None, None, None, None)

    def test_gen_util_func(self):
        util = edge.gen_util_func(0)
        self.assertEqual(util, edge.DEF_MAX_UTIL)

    def test_trade(self):
        agent1 = edge.create_wagent('Wine holders', 0)
        agent2 = edge.create_cagent('Cheese holders', 0)
        tu.trade(agent1, "wine", edge.DEF_NUM_WINE, agent2, "cheese", edge.DEF_NUM_CHEESE)
        self.assertEqual(agent1["goods"]["wine"]["endow"], 0)
        self.assertEqual(agent2["goods"]["cheese"]["endow"], 0)

    def test_rec_offer(self):
        agent1 = edge.create_wagent('Wine holders', 0)
        agent2 = edge.create_cagent('Cheese holders', 0)
        ans = tu.rec_offer(agent1, "cheese", 1, agent2)
        self.assertEqual(agent1["goods"]["cheese"]["endow"], 1)
        self.assertEqual(agent2["goods"]["wine"]["endow"], 1)

    def test_utility_delta(self):
        agent = edge.create_cagent('Cheese holders', 0)
        test_case = edge.DEF_NUM_CHEESE
        agent["goods"]["cheese"]["endow"] = test_case
        change = tu.utility_delta(agent, "cheese", 1)
        check = (edge.DEF_MAX_UTIL - test_case + edge.DEF_MAX_UTIL - (test_case + 1)) / 2
        self.assertEqual(change, check)

    def test_adj_add_good(self):
        agent = edge.create_cagent('Cheese holders', 0)
        tu.adj_add_good(agent, "cheese", -edge.DEF_NUM_CHEESE)
        self.assertEqual(agent["goods"]["cheese"]["endow"], 0)

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
