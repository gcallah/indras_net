"""
This is the test suite for trade.py.
"""

from unittest import TestCase, main

import capital.trade as td


class tradeTestCase(TestCase):
    def setUp(self, props=None):
        # self.pa = td.get_props("trade", props, model_dir="capital")
        # (td.trader_group, td.max_utility) = td.set_up()
        pass

    def tearDown(self):
        # (td.trader_group, td.max_utility) = (None, None)
        pass

    def test_random_generate_resources(self):
        pass

    def test_create_trader(self):
        pass
        # waiting for random generate resources being done
        # agent = td.create_trader('trader', 0)
        # name = agent.name
        # pamt = agent["goods"]["penguin"]["endow"]
        # camt = agent["goods"]["cat"]["endow"]
        # bamt = agent["goods"]["bear"]["endow"]
        # famt = agent["goods"]["pet food"]["endow"]
        # self.assertEqual(name, "trader0")

    if __name__ == '__main__':
        main()
