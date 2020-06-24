"""
This is the test suite for edgeworthbox.py.
"""

from unittest import TestCase, main, skip

import capital.edgeworthbox as edge
from capital.trade_utils import AMT_AVAIL, seek_a_trade
from capital.trade_utils import gen_util_func, trade, DEF_MAX_UTIL
from capital.trade_utils import rec_offer, utility_delta, adj_add_good


class EdgeworthboxTestCase(TestCase):
    def setUp(self, props=None):
        self.pa = edge.init_props("edgeworthbox", props, model_dir="capital")
        (edge.cheese_group, edge.wine_group, edge.max_util) = edge.set_up()

    def tearDown(self):
        (edge.cheese_group, edge.wine_group, edge.max_util) = (None, None, None)

    def test_trade(self):
        agent1 = edge.create_wagent('Wine holders', 0)
        agent2 = edge.create_cagent('Cheese holders', 0)
        trade(agent1, "wine", edge.DEF_NUM_WINE,
              agent2, "cheese", edge.DEF_NUM_CHEESE)
        self.assertEqual(agent1["goods"]["wine"][AMT_AVAIL], 0)
        self.assertEqual(agent2["goods"]["cheese"][AMT_AVAIL], 0)

    def test_rec_offer(self):
        agent1 = edge.create_wagent('Wine holders', 0)
        agent2 = edge.create_cagent('Cheese holders', 0)
        ans = rec_offer(agent1, "cheese", 1, agent2)
        self.assertEqual(agent1["goods"]["cheese"][AMT_AVAIL], 1)
        self.assertEqual(agent2["goods"]["wine"][AMT_AVAIL], 1)

    def test_utility_delta(self):
        agent = edge.create_cagent('Cheese holders', 0)
        agent["goods"]["cheese"][AMT_AVAIL] = edge.DEF_NUM_CHEESE
        delta = utility_delta(agent, "cheese", 1)
        self.assertGreaterEqual(delta, 0.0)
        self.assertLessEqual(delta, DEF_MAX_UTIL)

    def test_adj_add_good(self):
        agent = edge.create_cagent('Cheese holders', 0)
        adj_add_good(agent, "cheese", -edge.DEF_NUM_CHEESE)
        self.assertEqual(agent["goods"]["cheese"][AMT_AVAIL], 0)

    def test_create_wagent(self):
        agent = edge.create_cagent('Wine holders', 0)
        name = agent.name
        camt = agent["goods"]["cheese"][AMT_AVAIL]
        wamt = agent["goods"]["wine"][AMT_AVAIL]
        self.assertEqual(name, "Wine holders0")
        self.assertEqual(camt, edge.DEF_NUM_CHEESE)
        self.assertEqual(wamt, 0)

    def test_create_cagent(self):
        agent = edge.create_cagent('Cheese holders',0)
        name = agent.name
        camt = agent["goods"]["cheese"][AMT_AVAIL]
        wamt = agent["goods"]["wine"][AMT_AVAIL]
        self.assertEqual(name, "Cheese holders0")
        self.assertEqual(camt, edge.DEF_NUM_CHEESE)
        self.assertEqual(wamt, 0)

    if __name__ == '__main__':
        main()
