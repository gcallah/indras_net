"""
edgebox_model.py
An Edgeworth Box model where two agents trade goods.
"""
import logging
import spatial_agent

TRADE = "trade"

WINE = "wine"
CHEESE = "cheese"

GAIN = 1
LOSE = -1

Accept = True
Refuse = False


def util_func(qty):
    return 10 - .5 * qty


class EdgeboxAgent(spatial_agent.SpatialAgent):
    """
    Agents who attempt to trade goods to achieve greater utility
    """

    def __init__(self, name, goal=TRADE):
        super().__init__(name, goal, max_detect=1000.0)
        self.goods = {}
        self.utils = 0


    def act(self):
        potential_traders = self.survey_env(TRADE)        
        for t in potential_traders:
            logging.info("Potential trader for " 
                    + self.name 
                    + " (who has " + " ".join(self.list_goods())
                    + " and utils of " + str(self.utils)
                    + "): " + t.name)
            for g in self.goods:
                if self.goods[g]["endow"] > 0:
                    print(self.name + " is offering " + g + " to " + t.name)
                    t.rec_offer(g, 1, self)


    def endow(self, good, endow):
        if good not in self.goods:
            self.__add_good(good)
        self.goods[good]["endow"] = endow
        for i in range(1, endow):
            self.utils += self.goods[good]["util_func"](i)


# for the moment all offers are of 1 unit!
    def rec_offer(self, offer_good, amt, counterparty):
        util_gain = self.__marginal_util(offer_good, amt, GAIN)
        print(self.name
                + " is looking at a util gain of "
                + str(util_gain)
                + " for good "
                + offer_good)
        for g in self.goods:
            if (g != offer_good) and (self.goods[g]["endow"] > 0):
                util_loss = self.__marginal_util(g, 1, LOSE)
                print(self.name
                     + " is looking at a util loss of "
                     + str(util_loss)
                     + " for good "
                     + g)
                if (util_gain + util_loss) > 0:
                    if(counterparty.rec_reply(
                                offer_good, amt, g, 1, self)):
                        self.trade()

    def trade(self):
        print("Going to trade!")


    def rec_reply(self, my_good, my_amt, his_good, his_amt, counterparty):
        util_gain = self.__marginal_util(his_good, his_amt, 1)
        util_loss = self.__marginal_util(my_good, my_amt, -1)
        return util_gain > util_loss


    def list_goods(self):
        goods_list = []
        for g in self.goods:
            goods_list.append(g)
        return goods_list


    def __marginal_util(self, good, amt, gain_or_lose):
        g = self.goods[good]
        if gain_or_lose == GAIN:
            return g["util_func"](g["endow"] + 1)
        else:
            return -(g["util_func"](g["endow"]))


    def __add_good(self, good):
        self.goods[good] = {"endow": 0, "util_func": util_func}


class EdgeboxEnv(spatial_agent.SpatialEnvironment):
    """
    Contains goods and agents who exchange them.
    """

    def __init__(self, length, height, model_nm=None):
        super().__init__("An Edgeworth Box", length, height, model_nm=model_nm)
        self.do_census = False


    def step(self, delay=0):
        super().step(delay=delay)

