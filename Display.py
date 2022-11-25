import pygame as pg
import Creature


def render(screen, creatures, camera, width, height):
    screen.fill((0, 0, 0))
    for creature in creatures:
        if type(creature) == Creature.Hunter:
            pg.draw.rect(screen, creature.color,
                         [(creature.x - camera.x) * camera.scale + width/2,
                          (creature.y - camera.y) * camera.scale + height/2,
                          creature.size * camera.scale + 1,
                          creature.size * camera.scale + 1])
        elif type(creature) == Creature.Prey:
            pg.draw.circle(screen, creature.color,
                           [(creature.x - camera.x) * camera.scale + width/2,
                            (creature.y - camera.y) * camera.scale + height/2],
                           (creature.size * camera.scale) + 1)
        else:  # ещё что то
            pass
        pg.display.update()


class Camera:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.scale = 1

    def move(self):
        kpressed = pg.key.get_pressed()
        if kpressed[pg.K_UP]:
            self.y -= 10/self.scale
        elif kpressed[pg.K_DOWN]:
            self.y += 10/self.scale

        if kpressed[pg.K_LEFT]:
            self.x -= 10/self.scale
        elif kpressed[pg.K_RIGHT]:
            self.x += 10/self.scale

    def scale_plus(self):
        self.scale = self.scale*1.3

    def scale_minus(self):
        self.scale = self.scale/1.3
