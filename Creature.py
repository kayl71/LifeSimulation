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

    def update(self, dt):
        self.x += self.speed*math.cos(math.radians(self.direction)) * dt
        self.y += self.speed*math.sin(math.radians(self.direction)) * dt
        self.energy -= dt * self.energy_loss
        if self.energy <= 0:
            self.alive = False
        self.move_to(200, 200, dt)

    def is_dead(self):
        return not self.alive

    def rotate(self, angle):
        self.direction += angle

    def eat(self, energy):
        self.energy += energy

    def move_to(self, x, y, dt):
        X, Y = self.x - x, self.y - y
        k = 1
        if Y > 0:
            k = -1
        angle = (180 - math.degrees(math.acos(X / math.sqrt(X*X + Y * Y))) * k ) % 360
        self.direction%= 360
        k = 1
        if angle - self.direction < 0:
            k = -1
        if not math.fabs(self.direction - angle) < 1:
            self.rotate(k * 3 * self.speed * dt)


class Hunter(Creature):
    pass


class Prey(Creature):
    pass
