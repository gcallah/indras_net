"""
Filename: plane_agent.py
Author: Gene Callahan
"""

# import logging
import indra.spatial_agent as sa
import indra.plane_env as pe

MAX_EXCLUDE = 10


class PlaneAgent(sa.SpatialAgent):
    """
    This class is the parent of all entities that are
    located on a plane env.
    """

    def __init__(self, name, goal, max_move=0.0, max_detect=0.0):
        super().__init__(name, goal, max_move, max_detect)

    @property
    def pos(self):
        return (self.__pos.real, self.__pos.imag)

    @pos.setter
    def pos(self, pos):
        self.__pos = pos

    def in_range(self, prey, dist):
        """
        Is one agent in range of another in some sense?
        """
        if prey is None:
            return False
        my_pos = pe.pos_to_complex(self.pos)
        prey_pos = pe.pos_to_complex(prey.pos)
        if abs(my_pos - prey_pos) < dist:
            return True
        else:
            return False

    def detect_behavior(self):
        """
        What to do on detecting a prehension.
        """
        pass
