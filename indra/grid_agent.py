"""
grid_agent.py
Overrides pos for SpatialAgent.
Maybe other things for grid as well.
"""

# import logging
import indra.spatial_agent as sa

X = 0
Y = 1

class GridView():
    """
    Defines a subsection of the entire grid env.
    """

    class CellIter:
        """
        Iterate through the view's cells.
        """
        def __init__(self, view):
            self.view = view
            self.x = view.x1
            self.y = view.y1

        def __iter__(self):
            return self

        def __next__(self):
            while self.y < self.view.y2:
                while self.x < self.view.x2:
                    ret = self.view.grid[self.y][self.x]
                    self.x += 1
                    return ret
                self.x = self.view.x1
                self.y += 1

            raise StopIteration()

    def __init__(self, grid, x1, y1, x2, y2):
        """
        see if view is in grid
        adjust x, y to fit if not
        """
        if x1 < 0:
            x1 = 0
        if y1 < 0:
            y1 = 0
        if x2 > grid.width:
            x2 = grid.width
        if y2 > grid.height:
            y2 = grid.height
        self.grid = grid
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def __iter__(self):
        """
        Iterate through the cells in this view.
        """
        return GridView.CellIter(self)

    def out_of_bounds(self, x, y):
        """
        Returns False if x, y in view, else True.
        """
        return out_of_bounds(x, y, self.x1, self.y1, self.x2, self.y2)

    def filter_view(self, lam):
        """
        Returns a view filtered with lambda functionlam.
        """
        return list(filter(lam, iter(self)))

    def get_empties(self):
        """
        Return all of the unoccupied cells in this view.
        """
        return self.filter_view(lambda x: x.is_empty())

    def get_neighbors(self):
        """
        Return all of the occupied cells in this view.
        """
        return self.filter_view(lambda x: not x.is_empty())
    
    def to_json(self):
        safe_fields = {}
        safe_fields["x1"] = self.x1
        safe_fields["x2"] = self.x2
        safe_fields["y1"] = self.y1
        safe_fields["y2"] = self.y2
        return safe_fields

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
        if self.__cell:
            return self.__cell.coords
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
        safe_fields = super().to_json()
        safe_fields["cell"] = self.__cell.to_json()
        #safe_fields["neighborhood"] = None#self.neighborhood #Try if we can to_json lists
        safe_fields["hood_size"] = self.hood_size
        safe_fields["my_view"] = self.my_view.to_json() if self.my_view else None
        
        return safe_fields
    
    def from_json_preadd(self, json_input):
        super().from_json_preadd(json_input)
        
        self.hood_size = json_input["hood_size"]
    
    def from_json_postadd(self, json_input):
        super().from_json_postadd(json_input)
        
        if json_input["my_view"]:
            self.my_view = GridView(self.env, json_input["my_view"]["x1"], 
                                     json_input["my_view"]["y1"], 
                                     json_input["my_view"]["x2"], 
                                     json_input["my_view"]["y2"])