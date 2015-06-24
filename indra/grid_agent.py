"""
grid_agent.py
Overrides pos for SpatialAgent.
Maybe other things for grid as well.
"""

# import logging
import indra.spatial_agent as sa

X = 0
Y = 1


class GridAgent(sa.SpatialAgent):
    """
    This class is the parent of all entities that are
    located in a grid space (and might or might not move in it)
    """

    def __init__(self, name, goal, max_move=0.0, max_detect=0.0, cell=None):
        super().__init__(name, goal, max_move=max_move,
                         max_detect=max_detect)
        self.__cell = cell
        self.neighborhood = None

    @property
    def cell(self):
        return self.__cell

    @cell.setter
    def cell(self, cell):
        """
        Sets where we are on grid.
        """
        self.__cell = cell

    @property
    def pos(self):
        if self.cell:
            return self.cell.coords
        else:
            return None

    def _neighbor_filter(self, distance=1, moore=True, view=None):
        return filter(lambda x: x is not self,
                      self.env.neighbor_iter(self.pos[X], self.pos[Y],
                                             distance=distance,
                                             moore=moore,
                                             view=view))

    def get_square_view(self, distance):
        return self.env.get_square_view(self.pos, distance)

    def neighbor_iter(self, distance=1, moore=True, save_hood=False,
                      view=None):
        """
        Iterate over our neighbors.
        In some models, the neighbors don't move:
            then we can save the neighborhood and a lot of overhead!
        """
        if not save_hood:
            return self._neighbor_filter(distance, moore, view=view)
        else:
            if not self.neighborhood:
                self.neighborhood = list(self._neighbor_filter(
                                         distance, moore, view=view))
            return iter(self.neighborhood)

    def to_json(self):
        """
        We're going to make a dictionary of the 'safe' parts of the object to
        output to a json file. (We can't output the env, for instance, since
        IT contains a reference to each agent!)
        """
        safe_fields = super().to_json()
        safe_fields["pos"] = self.pos
        return safe_fields


class SocialAgent(GridAgent):
    """
    A grid agent concerned with its neighbors.
    """

    def __init__(self, name, goal, max_move=0.0, max_detect=0.0, cell=None):
        super().__init__(self, name, goal, max_move=max_move,
                         max_detect=max_detect, cell=cell)
        self.my_view = None
