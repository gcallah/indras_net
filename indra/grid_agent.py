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

    def __init__(self, name, goal, max_move=1, max_detect=1, cell=None):
        super().__init__(name, goal, max_move=max_move,
                         max_detect=max_detect)
        self.__cell = cell
        self.neighborhood = None
        self.hood_size = max_detect
        self.my_view = None

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

    def _neighbor_filter(self, moore=True, view=None, filt_func=None):
        """
        This filter can be overridden in class's that need a different one
        by passing in a different filter function.
        """
        if filt_func is None:
            def filt_func(n): return n is not self
        return filter(filt_func,
                      self.env.neighbor_iter(self.pos[X], self.pos[Y],
                                             moore=moore,
                                             view=view))

    def act(self):
        """
        Here we set up the usual pattern of action for a grid agent.
        """
        env_vars = self.survey_env()
        eval_vars = self.eval_env(env_vars)
        if eval_vars:
            self.respond_to_cond(eval_vars)

    def survey_env(self):
        """
        Have a look around, by default in a square view.
        """
        self.my_view = self.get_square_view(self.hood_size)
        return (self.my_view)

    def eval_env(self, env_vars):
        """
        Return True if we need to do something.
        """
        return env_vars is not None

    def respond_to_cond(self, eval_vars=None):
        """
        Default is to jump to empty cell.
        """
        self.move_to_empty(grid_view=self.my_view)

    def get_square_view(self, distance):
        return self.env.get_square_view(self.pos, distance)

    def neighbor_iter(self, moore=True, save_hood=False, view=None,
                      filt_func=None, sq_v=1):
        """
        Iterate over our neighbors.
        In some models, the neighbors don't move:
            then we can save the neighborhood and a lot of overhead!
        """
        if view is None:
            view = self.my_view
        if view is None:
            # our default view is a square reaching 1 cell out from self
            # in every direction
            view = self.get_square_view(sq_v)

        if not save_hood:
            return self._neighbor_filter(moore, view=view, filt_func=filt_func)
        else:
            if not self.neighborhood:
                self.neighborhood = list(self._neighbor_filter(
                                         moore, view=view,
                                         filt_func=filt_func))
            return iter(self.neighborhood)

    def move_to_empty(self, grid_view=None):
        self.env.move_to_empty(self, grid_view=grid_view)

    def debug_info(self):
        """
        Relevant debugging info.
        """
        s = (super().debug_info() + "\nLocation x: "
             + str(self.pos[X]) + ", y: " + str(self.pos[X])
             + "\nHood size: " + str(self.hood_size))
        return s

    def to_json(self):
        """
        We're going to make a dictionary of the 'safe' parts of the object to
        output to a json file. (We can't output the env, for instance, since
        IT contains a reference to each agent!)
        """
        safe_fields = super().to_json()
        safe_fields["pos"] = self.pos
        return safe_fields
