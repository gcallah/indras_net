"""
auditorium_model.py
Modeling Schelling's auditorium puzzle.
"""
import indra.grid_agent as ga
import indra.grid_env as ge


class AuditoriumAgent(ga.GridAgent):
    """
    Agents that seat themselves in an auditorium.
    """
    def __init__(self, name, goal="Get a seat"):
        super().__init__(name, goal=goal)
        self.seated = False

    def act(self):
        """
        Find a seat.
        Once seated, these agents just stay put!
        """
        if not self.seated:
            self.env.move_to_empty(self)
            self.seated = True

    def is_row_half_empty(self, row):
        num_empties = len(row.get_empties())
        num_neighbors = len(row.get_neighbors())
        return num_empties > num_neighbors


class RearAgent(AuditoriumAgent):
    """
    Agents that want to sit at the back.
    They also want their row less than half full.
    """

    def act(self):
        """
        Find a seat in the furthest row back < 1/2 full.
        Once seated, these agents just stay put!
        """
        if not self.seated:
            for row in self.env.row_iter():
                if self.is_row_half_empty(row):
                    self.env.position_item(self, grid_view=row)
                    self.seated = True
                    break


class NotInFrontAgent(AuditoriumAgent):
    """
    These agents don't want to be the very first person in front.
    They start out in the middle, and fill from there.
    """
    def act(self):
        if not self.seated:
            start = self.env.get_mdl_row()
            for row in self.env.row_iter(start_row=start, direction=-1):
                if self.is_row_half_empty(row):
                    self.env.position_item(self, grid_view=row)
                    self.seated = True
                    break


class Auditorium(ge.GridEnv):
    """
    The auditorium where agents will seat themselves.
    """

    class RowIter:
        """
        Iterate through auditorium's rows.
        Returns a GridView of just that row.
        """
        def __init__(self, aud, start_row=0, direction=1):
            self.auditorium = aud
            self.row = start_row
            self.dir = direction

        def __iter__(self):
            return self

        def __next__(self):
            if self.row < self.auditorium.height:
                ret = self.auditorium.get_row_view(self.row)
                self.row += self.dir
                return ret
            else:
                raise StopIteration()

    def __init__(self, name, height=36, width=40, torus=False,
                 model_nm="Auditorium", num_agents=800, props=None):
        super().__init__(name, width, height, torus=torus,
                         model_nm=model_nm, props=props)
        self.total_agents = num_agents
        self.curr_agents = 0

    def step(self):
        """
        Add an agent each turn.
        """
        super().step()
        if self.curr_agents < self.total_agents:
            self.add_agent(NotInFrontAgent("NotInFront agent %i"
                                           % self.curr_agents),
                           position=False)
            self.curr_agents += 1

    def row_iter(self, start_row=0, direction=1):
        return Auditorium.RowIter(self, start_row, direction)

    def get_mdl_row(self):
        return self.height // 2
