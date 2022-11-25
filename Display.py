import pygame as pg
import Creature


# Рендер в классах
def render(screen, creatures, camera):
    screen.fill((0, 0, 0))
    for creature in creatures:
        if type(creature) == Creature.Hunter:
            pg.draw.rect(screen, creature.color, [creature.x-camera.x, creature.y-camera.y,
                                                  creature.size, creature.size])
        elif type(creature) == Creature.Prey:
            pg.draw.circle(screen, creature.color, [creature.x-camera.x, creature.y-camera.y], creature.size)
        else:  # ещё что то
            pass
        pg.display.update()


class Camera:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        kpressed = pg.key.get_pressed()
        if kpressed[pg.K_UP]:
            self.y -= 3
        elif kpressed[pg.K_DOWN]:
            self.y += 3

        if kpressed[pg.K_LEFT]:
            self.x -= 3
        elif kpressed[pg.K_RIGHT]:
            self.x += 3

