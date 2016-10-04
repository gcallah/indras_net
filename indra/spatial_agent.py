"""
Filename: spatial_agent.py
Author: Gene Callahan
"""

from collections import deque
# import logging
import indra.entity as ent

MAX_EXCLUDE = 10


class SpatialAgent(ent.Agent):
    """
    This class is the parent of all entities that are
    located in space (and might or might not move in it)
    """

    def __init__(self, name, goal, max_move=0, max_detect=1):
        super().__init__(name, goal)
        self.max_move = max_move
        self.max_detect = max_detect
        self.__pos = None
        self.exclude = deque(maxlen=MAX_EXCLUDE)

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, pos):
        self.__pos = pos
