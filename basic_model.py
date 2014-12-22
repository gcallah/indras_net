import entity

class BasicAgent(entity.Agent):

    def act(self):
        print("Agent " + self.name + " trying to achieve " + self.goal)

