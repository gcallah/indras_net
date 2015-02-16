"""
Filename: predator_prey.py
Author: Gene Callahan
"""

import math
import random
import logging
import pprint
import spatial_agent as sa
import spatial_env


EAT = "eat"
AVOID = "avoid"
REPRODUCE = "reproduce"

pp = pprint.PrettyPrinter(indent=4)


class Creature(sa.SpatialAgent):

    """ This class is the parent of all things that:
        1) eat; 2) age; and 3) reproduce """

    def __init__(self, name, life_force, repro_age,
                 decay_rate, max_move=0.0, max_detect=10.0,
                 goal=EAT, rand_age=False):

        super().__init__(name, goal, max_move, max_detect)

        self.life_force = random.uniform(life_force * .8,
                                         life_force * 1.2)
        self.orig_force = self.life_force
        self.decay_rate = decay_rate
        self.repro_age = repro_age
        self.env = None

        if not rand_age:
            self.age = 0
        else:
            self.age = random.uniform(0, self.repro_age)


    def __str__(self):
        return(self.name)


    def is_alive(self):
        """
        Boolean: is this critter alive or not?
        """
        return self.life_force > 0


    def act(self):
        """
        Reproduce if it is time!
        """
        self.age += 1.0
        if (int(math.floor(self.age)) % self.repro_age) < 1:
            offspring = self.reproduce()
            assert self.env != None
            if offspring != None:
                d, _i = math.modf(self.age)
                offspring.age += d
                self.env.add_agent(offspring)
        self.life_force -= self.decay_rate


    def reproduce(self):
        """
        The default reproduce does nothing.
        """
        return None


    def eat(self, prey):
        """
        Eat another critter and gain its life force.
        """
        self.life_force += prey.life_force
        prey.be_eaten()
        logging.info(self.name + " has eaten " + prey.name)


    def be_eaten(self):
        """
        Be eaten; life force goes to 0.
        """
        self.life_force = 0


class Grass(Creature):
    """
    This class defines grass, a type of herb
    and a likely prey creature
    """

    MAX_GRASS = 200


    def __init__(self, name, life_force, repro_age, decay_rate,
                 max_move=0.0, max_detect=0.0, goal=REPRODUCE,
                 rand_age=False):

        super().__init__(name, life_force, repro_age, decay_rate,
                         max_move=max_move, max_detect=max_detect,
                         goal=goal, rand_age=rand_age)


    def reproduce(self):
        """
        Make new grass.
        """
        my_pop = self.env.get_my_pop(self)
        if my_pop < self.MAX_GRASS:
            return Grass("herb" + str(my_pop), self.orig_force,
                         self.repro_age, self.decay_rate)
        else: return None


class MobileCreature(Creature, sa.MobileAgent):
    """
    This class is the parent of all creatures
    that can move around.
    """

    def __init__(self, name, life_force, repro_age, 
                 decay_rate, max_move=0.0, max_detect=10.0,
                 max_eat=2.0, goal=EAT, rand_age=False):

        super().__init__(name, life_force, repro_age, 
                         decay_rate, max_move, max_detect,
                         goal=goal, rand_age=rand_age)

        self.max_eat = max_eat
        self.wandering = True


    def in_gobble_range(self):
        """
        Are we close enough to eat the thing we are
        focused on?
        """
        return self.in_range(self.focus, self.max_eat)


class Predator(MobileCreature):
    """
    The ancestor of all creatures that eat other mobile
    creatures.
    """

    def detect_behavior(self):
        """
        On detecting prey, predators pursue it.
        """
        self.pursue_prey()


    def pursue_prey(self):
        """
        Chase down the prey we have spotted.
        """
        prey = self.focus
        logging.info(self.name + " is pursuing " + prey.name)
        if prey.is_alive():
            new_pos = self.pos
            vector = prey.pos - self.pos
            dist = abs(vector)
            if dist < self.max_move:
                new_pos = prey.pos
            else:
                new_pos += (vector / dist) * self.max_move

            self.pos = new_pos
            if self.in_gobble_range():
                self.eat(prey)
                self.wandering = True
                self.focus = None


class MobilePrey(MobileCreature):
    """
    Prey that moves around.
    """

    def __init__(self, name, life_force, repro_age, 
                 decay_rate, max_move=0.0, max_detect=10.0,
                 max_eat=2.0, goal=AVOID, rand_age=False):

        super().__init__(name, life_force, repro_age, 
                         decay_rate, max_move, max_detect,
                         goal=goal, rand_age=rand_age)


    def detect_behavior(self):
        self.avoid_predator()


    def avoid_predator(self):
        """
        The default avoid_predator does nothing.
        We may want to do something here later.
        """
        pass



class Fox(Predator):
    """
    This class defines foxes, a type of predator.
    """

    def __init__(self, name, life_force, repro_age, decay_rate,
                 max_move=10.0, max_detect=10.0, goal=EAT, rand_age=False):

        super().__init__(name, life_force, repro_age, decay_rate,
                         max_move, max_detect, goal=goal,
                         rand_age=rand_age)


    def reproduce(self):
        """
        Make a new fox
        """
        return Fox("brer" + self.env.new_name_suffix(self),
                   self.orig_force, self.repro_age,
                   self.decay_rate, self.max_move,
                   self.max_detect)


class Mouse(MobilePrey):
    """
    This class defines mice, a type of herbivore
    and a likely prey creature
    """

    AVG_MOUSE_FORCE = 10.0


    def __init__(self, name, life_force, repro_age, decay_rate,
                 max_move, max_detect=10.0, goal=EAT, rand_age=False):

        super().__init__(name, life_force, repro_age, decay_rate,
                         max_move, max_detect, goal=goal,
                         rand_age=rand_age)


    def reproduce(self):
        """
        Make a new mouse; life force reverts towards mean.
        """
        force = (self.orig_force + self.AVG_MOUSE_FORCE) / 2.0
        return Mouse("mickey" + self.env.new_name_suffix(self),
                     force, self.repro_age, self.decay_rate,
                     self.max_move)


class Rabbit(Predator):

    """
    This class defines rabbits, a type of herbivore
    and a likely prey creature.
    """

    AVG_RABBIT_FORCE = 20.0


    def __init__(self, name, life_force, repro_age, decay_rate,
                 max_move, max_detect=10.0, goal=EAT,
                 rand_age=False):

        super().__init__(name, life_force, repro_age, decay_rate,
                         max_move, max_detect, goal=goal,
                         rand_age=rand_age)


    def reproduce(self):
        """
        Make a new rabbit; life force reverts towards mean.
        """
        force = (self.orig_force + self.AVG_RABBIT_FORCE) / 2.0
        return Rabbit("bunny" + self.env.new_name_suffix(self),
                      force, self.repro_age,
                      self.decay_rate, self.max_move)


class PredPreyEnv(spatial_env.SpatialEnv):

    """ This class creates an environment for predators
        to chase and eat prey """

    repop = True


    def __init__(self, name, length, height, preact=True,
                 postact=True, model_nm="predprey_model"):
        super().__init__(name, length, height, preact,
                         postact, model_nm=model_nm)
        self.agents.set_num_zombies(self.props.get("num_zombies", 0))


    def run(self):
        """
        Create zombies, then call our super's run.
        """
        self.agents.create_zombies()
        super().run()


    def keep_running(self):
        """
        Run as long as there are agents left.
        """
        return len(self.agents) > 0


    def postact_loop(self):
        """
        After acting, we cull dead creatures.
        Since we will be culling let's walk list in reverse.
        """
        for creature in reversed(self.agents):
            if not creature.is_alive():
                self.cull(creature)


    def cull(self, creature):
        """
        Eliminate creatures who have died.
        """
        self.agents.remove(creature)


    def new_name_suffix(self, creature):
        """
        Generate unique names for new critters.
        """
        pop = self.get_my_pop(creature)
        return "." + str(self.period) + "." + str(pop)


