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
    def __init__(self, name, goal, tolerance):
        super().__init__(name, goal)
        self.tolerance = tolerance
      
        
    def act(self):
        like_me = 0
        total_neighbors = 0
        (x, y) = self.env.get_pos_components(self)
        for neighbor in self.env.neighbor_iter(x, y):
            total_neighbors += 1
            if self.get_type() == neighbor.get_type():
                like_me += 1
        if like_me / total_neighbors < self.tolerance:        
            self.env.move_to_empty(self)
            print(self.name + ' has moved')
           
           
        
class BlueAgent(SegregationAgent):

    pass       

class RedAgent(SegregationAgent):
    
    pass

class GreenAgent(SegregationAgent):
    
    pass