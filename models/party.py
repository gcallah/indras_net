import indra.display_methods as disp
import indra.markov as markov
import indra.markov_agent as ma
import indra.markov_env as menv

from random import randint, choice

GROUP_SITES = []
BORING_GROUPS = 0

class Person(ma.MarkovAgent):

    def __init__(self, id):
        self.id = id
        self.happy = True
        self.group_site_index = randint(range(len(GROUP_SITES)))
        self.my_group_site = GROUP_SITES[self.group_site_index]
        self.sex = choice(['M', 'F']) # become a man or a woman
        GROUP_SITES[self.group_site_index] += [self]

    def updateHappiness(self, tolerance):
        same = 0
        for p in self.my_group_site:
            if p.sex == self.sex:
                same += 1

        total = len(self.my_group_site)

        opposite = total - same

        return (opposite / total) <= (tolerance / 100)

    def leave(self):
        if ~self.happy:
            #randomly face right or left
            for i in range(len(self.my_group_site)):
                currPerson = self.my_group_site[i]
                if currPerson.id == self.id:
                    index = i

            temp = self.my_group_site[-1]
            self.my_group_site[index] = temp
            self.my_group_site[:len(self.my_group_site) - 1]
            GROUP_SITES[self.group_site_index] = self.my_group_site

    def findNewGroup(self):
        for i in range(len(GROUP_SITES)):
            if i != self.group_site_index:
                if len(GROUP_SITES[i]) != 0:
                    self.group_site_index = i
                    self.my_group_site = GROUP_SITES[self.group_site_index]
                    GROUP_SITES[self.group_site_index] += [self]
                    return



class Party(menv.MarkovEnv):

    def start(self):
        pass


