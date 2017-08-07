# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 20:23:01 2014

@author: Brandon
This implements Paul Krugman's babysitting co-op model.
"""

# import logging
import indra.entity as ent
import indra.env as env
import indra.display_methods as disp
import random

''' These are our possible goals'''
UNKNOWN = 'unknown'
BABYSIT = 'babysit'
GO_OUT = 'go out'

ENV_NM = "Krugman Babysitting Co-op"


class CoopAgent(ent.Agent):
    """
    An agent that chooses to babysit or go out based on coupon holdings
    """
    def __init__(self, name, coupons, min_holdings):
        super().__init__(name, UNKNOWN)
        self.coupons = coupons
        self.min_holdings = min_holdings
        self.sitting = False

    def act(self):
        self.sitting = False
        if self.coupons < self.min_holdings:
            self.goal = BABYSIT
        elif self.coupons > self.min_holdings:
            if random.random() > .5:
                self.goal = GO_OUT
            else:
                self.goal = BABYSIT

    def pay(self, sitter):
        self.coupons -= 1
        sitter.coupons += 1


class CoopEnv(env.Environment):
    """
    An environment the co-op agents use to survey and interact
    """

    def __init__(self, model_nm=ENV_NM, props=None):
        super().__init__("Co-op Environment",
                         model_nm=model_nm, postact=True,
                         props=props)
        self.rd_exchanges = 0

    def postact_loop(self):
        """
        If an agent wants to go out, it hopes to 
        find a babysitter, and pay them
        """
        exchange = 0
        for agent in reversed(self.agents):
            if agent.goal == GO_OUT:
                sitter = self.assign_sitter()
                if sitter is None:
                    pass
                else:
                    agent.pay(sitter)
                    exchange += 1
            else:
                pass
            self.rd_exchanges = exchange
        print('\nCoupon exchanges in round ' + str(self.period)
              + ': ' + str(self.rd_exchanges) + '\n')

    def assign_sitter(self):
        """
        Surveys the environment for available and willing babysitters
        """
        for agent in reversed(self.agents):
            if agent.goal == BABYSIT:
                if agent.sitting is False:
                    agent.sitting = True
                    return agent
                else:
                    pass
            else:
                pass

    def census(self, disp=True):
        """
        Take a census of our pops.
        """
        self.change_pop_data('CoopAgent', self.rd_exchanges)
        for var in self.varieties_iter():
            pop = self.get_pop_data(var)
            self.append_pop_hist(var, pop)
        self.change_pop_data('CoopAgent', -self.rd_exchanges)

    def view_pop(self):
        """
        Draws a line graph of coupon exchanges
        """
        if self.period < 4:
            print("Too little data to display")
            return

        (period, data) = self.line_data()
        self.line_graph = disp.LineGraph("History of Coupon Exchanges",
                                         data, period)
