"""
edgebox_model.py
An Edgeworth Box model where two agents trade goods.
"""
import logging
import indra.spatial_agent as sa
import indra.spatial_env as se

TRADE = "trade"

WINE = "wine"
CHEESE = "cheese"

GLOBAL_KNOWLEDGE = 1000.0

Accept = True
Reject = False


def gen_util_func(qty):
    """
    A default util func: we can pass in others
    """
    return 10 - .5 * qty


class EdgeboxAgent(sa.SpatialAgent):
    """
    Agents who attempt to trade goods to achieve greater utility.
    We are descending this from SpatialAgent, because later on we want
    traders who can detect local prices but may not
    know about distant ones
    """

    def __init__(self, name, goal=TRADE, max_detect=GLOBAL_KNOWLEDGE):
        super().__init__(name, goal, max_detect=max_detect)
        self.goods = {}
        self.utils = 0
        self.pretrade_utils = 0

    def act(self):
        """
        Act is called in an interactive loop by code
        in the base framework
        """

        potential_traders = self.survey_env(TRADE)
        for t in potential_traders:
            for g in self.goods:
                amt = 1
                while self.goods[g]["endow"] >= amt:
                    logging.debug(self.name + " is offering "
                                  + g + " to " + t.name)
                    if t.rec_offer(g, amt, self):
                        break
                    amt += 1

    def endow(self, good, new_endow, util_func=None):
        """
        Endow an agent with some amount of some good.
        """
        if good not in self.goods:
            self.__add_good(good)

        g = self.goods[good]
        if util_func is not None:
            g["util_func"] = util_func

        self.utils += self.__marginal_util(good, new_endow)

        self.pretrade_utils = self.utils
        g["endow"] += new_endow

    def incr_util(self, good, incr):
        """
        Increase the utility we receive from a good by incr.
        """
        self.goods[good]["incr"] += incr

    def rec_offer(self, his_good, his_amt, counterparty):
        """
        Agent has received an offer of a good,
        and loops over her goods to
        see if there is a profitable trade.
        If 'yes,' make a counter-offer.
        """

        my_amt = 1
        util_gain = self.__marginal_util(his_good, his_amt)
        logging.info(self.name
                     + " is looking at a util gain of "
                     + str(util_gain)
                     + " for good "
                     + his_good)
        for my_good in self.goods:
            if((my_good != his_good)
               and (self.goods[my_good]["endow"] > 0)):
                util_loss = self.__marginal_util(my_good, -my_amt)
                logging.info(self.name
                             + " is looking at a util loss of "
                             + str(util_loss)
                             + " for good "
                             + my_good)
                if util_gain > util_loss:
                    if(counterparty.rec_reply(his_good,
                                              his_amt,
                                              my_good,
                                              my_amt)
                       is Accept):
                        self.trade(my_good, my_amt,
                                   counterparty, his_good, his_amt)
                        return Accept
        return Reject

    def rec_reply(self, my_good, my_amt, his_good, his_amt):
        """
        This is a response to a trade offer this agent has initiated
        """

        util_gain = self.__marginal_util(his_good, his_amt)
        util_loss = self.__marginal_util(my_good, -my_amt)
        return util_gain > util_loss

    def list_goods(self):
        """
        List the goods an agent possesses.
        """
        goods_descr = ""
        for g in self.goods:
            goods_descr = (goods_descr + g + ": "
                           + str(self.goods[g]["endow"]) + ", ")
        return goods_descr.strip()

    def trade(self, my_good, my_amt, counterparty, his_good, his_amt):
        """
        We actual swap goods, and record the trade in the environment
        """
        logging.info(self.name + " is going to trade "
                     + str(my_amt) + " units of " + my_good
                     + " for " + str(his_amt)
                     + " units of " + his_good
                     + " with " + counterparty.name)
        self.__adj_good_amt(my_good, -my_amt)
        self.__adj_good_amt(his_good, his_amt)
        counterparty.__adj_good_amt(his_good, -his_amt)
        counterparty.__adj_good_amt(my_good, my_amt)

        self.env.record_trade(self, counterparty)

    def util_gain(self):
        """
        Calculate our utility gain.
        """
        return self.utils - self.pretrade_utils

    def __adj_good_amt(self, good, amt):
        """
        We are about to add or give up a good.
        Record the change in possessions and utility.
        """
        self.utils += self.__marginal_util(good, amt)
        self.goods[good]["endow"] += amt

    def __marginal_util(self, good, amt):
        """
        What is the marginal utility gained or lost
        from our current trade?
        """
        g = self.goods[good]
        return (g["util_func"](g["endow"])
                - g["util_func"](g["endow"] + amt))

    def __add_good(self, good):
        """
        Add a new good this agent 'knows' about
        and has a utility function for.
        """
        self.goods[good] = {"endow": 0,
                            "util_func": gen_util_func,
                            "incr": 0.0}


class EdgeboxEnv(se.SpatialEnv):
    """
    Contains goods and agents who exchange them.
    """

    def __init__(self, name, length, height, model_nm=None,
                 preact=False):
        super().__init__(name, length, height, model_nm=model_nm,
                         preact=preact)
        self.do_census = False
        self.trades_this_prd = 0

    def step(self):
        """
        Step through one period of trading.
        """
        self.trades_this_prd = 0
        super().step()
        self.user.tell("Trades this period: "
                       + str(self.trades_this_prd))
        self.step_report()

    def step_report(self):
        """
        What we report to the user after stepping.
        """
        if self.trades_this_prd <= 0:
            self.user.tell("We've reached equilibrium.")
        else:
            for a in self.agents:
                self.user.tell(a.name + " has gained "
                               + str(a.util_gain())
                               + " utils and now has: "
                               + a.list_goods())

    def record_trade(self, a1, a2):
        """
        Record the fact a trade has occured.
        """
        self.trades_this_prd += 1
        self.join_agents(a1, a2)
