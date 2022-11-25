import pygame as pg
import Creature

# Рендер в классах
def render(screen, creature):
    if type(creature) == Creature.Hunter:
        pg.draw.rect(screen, creature.color, [creature])
    elif type(creature) == Creature.Prey:
        pg.draw.circle(screen)
    else: # ещё что то
        pg.draw.circle(screen)

