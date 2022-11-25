import pygame as pg
import Creature

# Рендер в классах
def render(screen, creatures):
    for creature in creatures:
        if type(creature) == Creature.Hunter:
            pg.draw.rect(screen, creature.color, [creature.x, creature.y, creature.size, creature.size])
        elif type(creature) == Creature.Prey:
            pg.draw.circle(screen, creature.color, [creature.x, creature.y], creature.size)
        else: # ещё что то
            pass
        pg.display.update()

