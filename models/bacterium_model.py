import indra.grid_agent as ga

X = 0
Y = 1

class Bacterium(ga.GridAgent):
    """
    An agent that randomly jumps to an empty cell every turn. does not yet seek
    the foodsource
    """

    def act(self):
        (x, y) = self.get_pos()
        print("My name is " + self.name + " and I am a " + self.ntype +".")
        print("My position is" + " x = " + str(x)+ "," + " y = " + str(y))
        #print(self.name + " has neighbors: ")
        for neighbor in self.env.neighbor_iter(x, y):
            """(x1, y1) = neighbor.get_pos()
            print("    %i, %i" % (x1, y1))"""

    def postact(self):
        self.env.move_to_empty(self)        

class FoodSource(ga.GridAgent):
    """
    An agent that checks its neighbors every turn. If one of those neighbors is
    a Bacterium, it will run away to a random location
    """

    def act(self):
        (x, y) = self.get_pos() #x and y
        print("I am a " + self.ntype)
        print("My position is x = " + str(x)+ ", y = " + str(y))
        for neighbor in self.env.neighbor_iter(x, y):
            if neighbor.ntype == "Bacterium":
                print("Enemy near! Run away!")
                self.env.move_to_empty(self)
                (x, y) = self.get_pos()
                print("My new position is x = " + str(x) + ", y = " + str(y))
            else:
                print("nothing here")
                
"""
    def postact(self):
        self.env.move_to_empty(self)
"""        