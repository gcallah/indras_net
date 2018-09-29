import indra.grid_agent as ga
import logging
import random as r

class TestGridAgent(ga.GridAgent):
    """
    An agent that prints its neighbors in preact
    and also jumps to an empty cell: defaut behavior
    from our ancestor.
    """

    def randomPermutation(n): #gets a random permutation of g=grid locations
        def swap(i,j):
            return (j,i)
        g = []
        for i in range(1,n+1):
            g.append(i)
        for i in range(0,r.randint(10,20)):
            x,y = (r.randint(0,n-1),r.randint(0,n-1))
            (g[x],g[y])  =  swap(g[x],g[y])
        return g  
               
    
    def preact(self):
        (x, y) = self.pos
        logging.info("With " + self.name + " we are looking around " + " x = " + str(x) + " y = " + str(y))
        logging.info(self.name + " has neighbors: ")
        for neighbor in self.neighbor_iter():
            (x1, y1) = neighbor.pos
            logging.info("    %i, %i" % (x1, y1))

    def postact(self):
        logging.info("Agent %s postacting" % (self.name))

