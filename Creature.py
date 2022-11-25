import math


class Creature:

    def __init__(self, koef_take_sun, koef_take_meat, koef_take_plant, size, x, y,
                 speed, color, direction, hunger, thurst, sleep):
        self.koef_take_sun = koef_take_sun
        self.koef_take_meat = koef_take_meat
        self.koef_take_plant = koef_take_plant
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.color = color
        self.direction = direction
        self.hunger = hunger
        self.thurst = thurst
        self.sleep = sleep

    def update(self, dt):
        self.x += self.speed * math.cos(math.radians(self.direction)) * dt
        self.y += self.speed * math.sin(math.radians(self.direction)) * dt
        self.hunger += 1
        self.thurst += 1
        self.sleep += 1


class Hunter(Creature):
    pass


class Prey(Creature):
    pass
