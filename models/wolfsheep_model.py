"""
wolfsheep_model.py
Wolves and sheep roaming a meadow, with wolves eating sheep
that get near them.
"""
import indra.grid_env as ge
import indra.grid_agent as ga


class Creature(ga.GridAgent):
    """
    A creature: moves around randomly.
    Reproduction to be added.
    """
    def __init__(self, name, goal, repro_age, life_force):
        super().__init__(name, goal)
        self.age = 0
        self.alive = True
        self.repro_age = repro_age
        self.life_force = life_force
        self.init_life_force = life_force

    def died(self):
        if self.alive:
            self.alive = False
            self.env.died(self)

    def act(self):
        self.age += 1
        self.life_force -= 1
        if self.life_force <= 0:
            self.died()
        if self.age % self.repro_age == 0:
            self.reproduce()

    def preact(self):
        self.env.move_to_empty(self)

    def reproduce(self):
        if self.alive:
            creature = self.__class__(self.name + "x", self.goal,
                                      self.repro_age, self.init_life_force)
            self.env.add_agent(creature)


class Wolf(Creature):
    """
    A wolf: moves around randomly and eats any sheep
    nearby.
    """
    def __init__(self, name, goal, repro_age, life_force):
        super().__init__(name, goal, repro_age, life_force)

    def act(self):
        super().act()
        if self.alive:

            def my_filter(n): return isinstance(n, Sheep)

            for sheep in self.neighbor_iter(filt_func=my_filter):
                if sheep.alive:
                    self.eat(sheep)
                    break  # don't be greedy! eat one sheep per turn!

    def eat(self, sheep):
        self.life_force += sheep.life_force
        sheep.died()


class Sheep(Creature):
    """
    A sheep: moves around randomly and sometimes gets eaten.
    """
    def __init__(self, name, goal, repro_age, life_force):
        super().__init__(name, goal, repro_age, life_force)


class Meadow(ge.GridEnv):
    """
    A meadow in which wolf eat sheep.
    """

    def died(self, prey):
        self.remove_agent(prey)
