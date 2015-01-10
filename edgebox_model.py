"""
edgebox_model.py
An Edgeworth Box model where two agents trade goods.
"""
import logging
import entity
import spatial_agent

TRADE = "trade"

WINE = "wine"
CHEESE = "cheese"

GAIN = 1
LOSE = -1

GLOBAL_KNOWLEDGE = 1000.0

Accept = True
Reject = False


def util_func(qty):
    """
    A default util func: we can pass in others
    """
    return 10 - .5 * qty


class EdgeboxAgent(spatial_agent.SpatialAgent):
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


    def endow(self, good, endow, util_func=None):
        if good not in self.goods:
            self.__add_good(good)

        g = self.goods[good]
        g["endow"] = endow
        if util_func is not None:
            g["util_func"] = util_func
        for i in range(1, endow):
            self.utils += g["util_func"](i)

        self.pretrade_utils = self.utils


# for the moment all offers are of 1 unit!
    def rec_offer(self, offer_good, amt, counterparty):
        """
        Agent has received an offer of a good,
        and loops over her goods to 
        see if there is a profitable trade.
        If 'yes,' make a counter-offer.
        """

        util_gain = self.__marginal_util(offer_good, amt, GAIN)
        logging.debug(self.name
                + " is looking at a util gain of "
                + str(util_gain)
                + " for good "
                + offer_good)
        for g in self.goods:
            if (g != offer_good) and (self.goods[g]["endow"] > 0):
                util_loss = self.__marginal_util(g, 1, LOSE)
                logging.debug(self.name
                     + " is looking at a util loss of "
                     + str(util_loss)
                     + " for good "
                     + g)
                if (util_gain + util_loss) > 0:
                    if(counterparty.rec_reply(
                            offer_good, amt, g, 1, self) is Accept):
                        self.trade(g, counterparty, offer_good)
                        return Accept
        return Reject


    def rec_reply(self, my_good, my_amt,
                his_good, his_amt, counterparty):
        """
        This is a response to a trade offer this agent has initiated
        """

        util_gain = self.__marginal_util(his_good, his_amt, 1)
        util_loss = self.__marginal_util(my_good, my_amt, -1)
        return (util_gain + util_loss) > 0


    def list_goods(self):
        goods_descr = ""
        for g in self.goods:
            goods_descr = (goods_descr + g + ": " 
                            + str(self.goods[g]["endow"]) + ", ")
        return goods_descr.strip()


    def trade(self, my_good, counterparty, his_good):
        """
        We actual swap goods, and record the trade in the environment
        """

        logging.info(self.name + " going to trade " + my_good 
                    + " for " + his_good
                    + " with " + counterparty.name)
        self.__gain_lose_good(my_good, LOSE)
        self.__gain_lose_good(his_good, GAIN)
        counterparty.__gain_lose_good(his_good, LOSE)
        counterparty.__gain_lose_good(my_good, GAIN)

        self.env.record_trade(1)


    def util_gain(self):
        return self.utils - self.pretrade_utils


    def __gain_lose_good(self, good, gain_or_lose):
        self.utils += self.__marginal_util(good, 1, gain_or_lose)
        self.goods[good]["endow"] += gain_or_lose


    def __marginal_util(self, good, amt, gain_or_lose):
        g = self.goods[good]
        if gain_or_lose == GAIN:
# we are calling a function stored in a dictionary here:
            return g["util_func"](g["endow"] + 1)
        else:
            return -(g["util_func"](g["endow"]))


    def __add_good(self, good):
        self.goods[good] = {"endow": 0, "util_func": util_func}


class EdgeboxEnv(spatial_agent.SpatialEnvironment):
    """
    Contains goods and agents who exchange them.
    """

    def __init__(self, name, length, height, model_nm=None):
        super().__init__(name, length, height, model_nm=model_nm)
        self.do_census = False
        self.trades_this_turn = 0


    def step(self, delay=0):
        super().step(delay=delay)
        self.user.tell("Trades this period: " + str(self.trades_this_turn))
        for a in self.agents:
            print(a.name + " has gained " + str(a.util_gain())
                    + " utils and now has: " + a.list_goods())

# any return other than "None" from the step function 
# breaks the interactive loop
        if self.trades_this_turn <= 0:
            return("We've reached equilibrium.")

        self.trades_this_turn = 0

    
    def record_trade(self, amt):
        self.trades_this_turn += amt


