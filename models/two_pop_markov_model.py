"""
You can clone this file and its companion two_pop_m_run.py
to easily get started on a new two pop markov model.
It also is a handy tool to have around for testing
new features added to the base system.
"""
import indra.two_pop_markov as itpm


class TestFollower(itpm.Follower):
    """
    An agent that prints its neighbors in preact
    and also jumps to an empty cell: defaut behavior
    from our ancestor.
    """

    def preact(self):
        (x, y) = self.pos
        print("With " + self.name
              + " we are looking around "
              + " x = " + str(x)
              + " y = " + str(y))
        print(self.name + " has neighbors: ")
        for neighbor in self.neighbor_iter():
            (x1, y1) = neighbor.pos
            print("    %i, %i" % (x1, y1))

    def postact(self):
        print("Agent %s postacting" % (self.name))
        super().postact()
        print("He is in state %s." % (self.state))


class TestLeader(itpm.Leader):
    """
    An agent that prints its neighbors in preact
    and also jumps to an empty cell: defaut behavior
    from our ancestor.
    """

    def preact(self):
        (x, y) = self.pos
        print("With " + self.name
              + " we are looking around "
              + " x = " + str(x)
              + " y = " + str(y))
        print(self.name + " has neighbors: ")
        for neighbor in self.neighbor_iter():
            (x1, y1) = neighbor.pos
            print("    %i, %i" % (x1, y1))

    def postact(self):
        print("Agent %s postacting" % (self.name))
        super().postact()
        print("He is in state %s." % (self.state))
