import pygame as pg


class Creature:

    def __init__(self, koef_take_sun, koef_take_meat, koef_take_plant, size, x, y, speed, color):
        self.koefTakeSun = koef_take_sun
        self.koefTakeMeat = koef_take_meat
        self.koefTakePlant = koef_take_plant
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.color = color

    def update(self):
        pass


class Hunter(Creature):
    def render(self, screen):
        pg.draw.rect(screen, self.color, [self.x, self.y, self.size, self.size])


class Prey(Creature):
    def render(self, screen):
        pg.draw.circle(screen, self.color, [self.x, self.y], self.size)
