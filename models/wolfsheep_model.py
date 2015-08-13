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
    Eventually, this should be a descendant of StanceAgent.
    """
    def __init__(self, name, goal, repro_age, life_force, max_detect=1):
        super().__init__(name, goal, max_detect=max_detect)
        self.age = 0
        self.alive = True
        self.other = None
        self.repro_age = repro_age
        self.life_force = life_force
        self.init_life_force = life_force

    def died(self):
        if self.alive:
            self.alive = False
            self.env.died(self)

    def survey_env(self):
        if self.alive:
            super().survey_env()

            def my_filter(n): return isinstance(n, self.other)

            for other in self.neighbor_iter(filt_func=my_filter):
                print("Detected %s" % (other.name))
                return (other)
        return None

    def postact(self):
        self.age += 1
        self.life_force -= 1
        if self.life_force <= 0:
            self.died()
        elif self.age % self.repro_age == 0:
            self.reproduce()

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
        self.other = Sheep

    def preact(self):
        """
        Wolves always move, seeking prey.
        """
        self.env.move_to_empty(self, grid_view=self.my_view)

    def respond_to_cond(self, env_vars=None):
        """
        We found a nearby sheep: eat it!
        """
        if env_vars is not None:
            sheep = (env_vars)
            if sheep.alive:
                self.eat(sheep)

    def eat(self, sheep):
        self.life_force += sheep.life_force
        sheep.died()
        print("%s eating a sheep!" % (self.name))


class Sheep(Creature):
    """
    A sheep: moves when wolf is nearby and sometimes gets eaten.
    """
    def __init__(self, name, goal, repro_age, life_force, max_detect=3):
        super().__init__(name, goal, repro_age, life_force,
                         max_detect=max_detect)
        self.other = Wolf


class Meadow(ge.GridEnv):
    """
    A meadow in which wolf eat sheep.
    """

    def died(self, prey):
        self.remove_agent(prey)
