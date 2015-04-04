"""
Filename: plane_agent.py
Author: Gene Callahan
"""

from collections import deque
# import logging
import indra.spatial_agent as sa

MAX_EXCLUDE = 10


class PlaneAgent(sa.SpatialAgent):
    """
    This class is the parent of all entities that are
    located in space (and might or might not move in it)
    """

    def __init__(self, name, goal, max_move=0.0, max_detect=0.0):
        super().__init__(name, goal)
        self.max_move = max_move
        self.max_detect = max_detect
        self.pos = None
        self.focus = None
        self.wandering = False
        self.exclude = deque(maxlen=MAX_EXCLUDE)

    def in_detect_range(self, prehended):
        """
        Can we see the prehended with our limited view?
        """
        return self.in_range(prehended, self.max_detect)

    def in_range(self, prey, dist):
        """
        Is one agent in range of another in some sense?
        """
        if prey is None:
            return False

        if abs(self.pos - prey.pos) < dist:
            return True
        else:
            return False

    def detect_behavior(self):
        """
        What to do on detecting a prehension.
        """
        pass

    def get_pos(self):
        return (self.pos.real, self.pos.imag)


class MobileAgent(PlaneAgent):
    """
    Agents that can move in the env
    """
    def __init__(self, name, goal, max_move=20.0, max_detect=20.0):
        super().__init__(name, goal,
                         max_move=max_move,
                         max_detect=max_detect)
        self.wandering = True
