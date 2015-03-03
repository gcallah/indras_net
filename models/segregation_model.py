# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 21:40:05 2015

@author: Brandon
"""

''' Segregation Model '''

import indra.spatial_agent as sa


class SegregationAgent(sa.SpatialAgent):
    """
    An agent that prints its neighbors when asked to act
    """

    def act(self):
        # print(ge.pos_msg(self))
        x = self.pos[0]
        y = self.pos[1]
        print("With agent " + self.name
              + " we are looking around "
              + " x = " + str(x)
              + " y = " + str(y))
        naybs = self.env.get_neighbors(x, y, True)
        if len(naybs) == 0:
            print(self.name + " has no neighbors.")
        else:
            print(self.name + " has neighbors: ")
            for nayb in naybs:
                print("    " + nayb.name)
