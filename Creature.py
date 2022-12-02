import math

import GenomeManager


class Creature:

    def __init__(self, size, speed, color, x = 0, y = 0):
        self.alive = True
        self.energy = 10
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.color = color
        self.direction = 0

        self.energy_loss = GenomeManager.GetEnergyLoss(self.size, self.speed)
        #self.hunger = hunger
        #self.thurst = thurst
        #self.sleep = sleep

    def update(self, dt):
        self.x += self.speed*math.cos(math.radians(self.direction)) * dt
        self.y += self.speed*math.sin(math.radians(self.direction)) * dt
        self.energy -= dt * self.energy_loss
        if self.energy <= 0:
            self.alive = False

    def is_dead(self):
        return not self.alive

    def eat(self, energy):
        self.energy += energy

class Hunter(Creature):
    pass


class Prey(Creature):
    pass
