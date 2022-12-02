import pygame as pg
import Creature

# Рендер в классах
def render(screen, creatures):
    screen.fill((0,0,0))
    for creature in creatures:
        if type(creature) == Creature.Hunter:
            pg.draw.rect(screen, creature.color, [creature.x, creature.y, creature.size, creature.size])
        elif type(creature) == Creature.Prey:
            pg.draw.circle(screen, creature.color, [creature.x, creature.y], creature.size)
        else:
            pg.draw.circle(screen, creature.color, [creature.x, creature.y], creature.size)
        pg.display.update()

