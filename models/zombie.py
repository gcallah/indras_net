import indra.grid_agent as ga
import logging

class TestGridAgent(ga.GridAgent):
    """
    An agent that prints its neighbors in preact
    and also jumps to an empty cell: defaut behavior
    from our ancestor.
    """

    def preact(self):
        (x, y) = self.pos
        logging.info("With " + self.name + " we are looking around " + " x = " + str(x) + " y = " + str(y))
        logging.info(self.name + " has neighbors: ")
        for neighbor in self.neighbor_iter():
            (x1, y1) = neighbor.pos
            logging.info("    %i, %i" % (x1, y1))

    def postact(self):
        logging.info("Agent %s postacting" % (self.name))
