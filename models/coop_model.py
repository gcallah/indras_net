# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 20:23:01 2014

@author: Brandon
"""

import logging
import indra.entity as ent
import indra.env as env
import indra.display_methods as dsp

''' These are our possible goals'''
UNKNOWN = 'unknown'
BABYSIT = 'babysit'
GO_OUT = 'go out'

ENV_NM = "Krugman Babysitting Co-op"


class CoopAgent(ent.Agent):

    def __init__(self, name, coupons):
        super().__init__(name, UNKNOWN)
        self.coupons = coupons
        self.sitting = False

    def act(self):

        self.sitting = False
        if self.coupons < 5.5:
            self.goal = BABYSIT
        else:
            self.goal = GO_OUT
        print(self.name + ' acting with coupons = '
              + str(self.coupons) + ' , goal = ' + self.goal)

    def pay(self, sitter):
        self.coupons -= 1
        sitter.coupons += 1
        # print('exchange has occured')


class CoopEnv(env.Environment):

    def __init__(self, model_nm=None):
        super().__init__("Co-op Environment",
                         model_nm=model_nm, preact=True)
        self.exchange_hist = []
        self.rd_exchanges = 0

    def preact_loop(self):
        exchange = 0
        for agent in reversed(self.agents):
            if agent.goal == GO_OUT:
                sitter = self.assignSitter()
                agent.pay(sitter)
                exchange += 1
            else:
                continue
            self.rd_exchanges = exchange
        self.exchange_hist.append(self.rd_exchanges)
        print('Coupon exchanges this round: ' + str(self.rd_exchanges))

    def assignSitter(self):
        for agent in reversed(self.agents):
            if agent.goal == BABYSIT:
                if agent.sitting is False:
                    agent.sitting = True
                    print(agent.name + ' is now sitting')
                    return agent
                else:
                    # print(agent.name + ' already sitting')
                    pass
            else:
                pass

    def display(self):
        if self.period < 4:
            print("Too little data to display")
            return

        dsp.display_line_graph('History of Coupon Exchanges ',
                               {"exchange history": self.exchange_hist},
                               self.period)
