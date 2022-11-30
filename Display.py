import pygame as pg
import Creature


def render(screen, creatures, camera, width, height):
    screen.fill((0, 0, 0))
    pg.draw.rect(screen, (255, 0, 0), [(-990 - camera.x) * camera.scale + width / 2,
                                       (-990 - camera.y) * camera.scale + height / 2,
                                       1980 * camera.scale + 1,    # Прямоугольник добавлен для проверки кода,
                                       1980 * camera.scale + 1])    # удалить его в финальной версии
    for creature in creatures:
        if type(creature) == Creature.Hunter:
            pg.draw.rect(screen, creature.color,
                         [(creature.x - camera.x) * camera.scale + width / 2,
                          (creature.y - camera.y) * camera.scale + height / 2,
                          creature.size * camera.scale + 1,
                          creature.size * camera.scale + 1])
        elif type(creature) == Creature.Prey:
            pg.draw.circle(screen, creature.color,
                           [(creature.x - camera.x) * camera.scale + width / 2,
                            (creature.y - camera.y) * camera.scale + height / 2],
                           (creature.size * camera.scale) + 1)
        else:  # ещё что то
            pass
        pg.display.update()


class Camera:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.scale = 1

    def move(self, screen_width, screen_height, area_width, area_height):
        kpressed = pg.key.get_pressed()
        if kpressed[pg.K_UP]:
            if self.y - (screen_height / self.scale) / 2 >= -area_height / 2 + 10 / self.scale:
                self.y -= 10 / self.scale
            else:
                self.y = (screen_height / self.scale) / 2 - area_height / 2
        elif kpressed[pg.K_DOWN]:
            if self.y + (screen_height / self.scale) / 2 <= area_height / 2 - 10 / self.scale:
                self.y += 10 / self.scale
            else:
                self.y = area_height / 2 - (screen_height / self.scale) / 2

        if kpressed[pg.K_LEFT]:
            if self.x - (screen_width / self.scale) / 2 >= -area_width / 2 + 10 / self.scale:
                self.x -= 10 / self.scale
            else:
                self.x = (screen_width / self.scale) / 2 - area_width / 2
        elif kpressed[pg.K_RIGHT]:
            if self.x + (screen_height / self.scale) / 2 <= area_width / 2 - 10 / self.scale:
                self.x += 10 / self.scale
            else:
                self.x = area_width / 2 - (screen_height / self.scale) / 2

    def scale_plus(self):
        self.scale = self.scale * 1.3

    def scale_minus(self, screen_width, screen_height, area_width, area_height):
        if all([((self.x - screen_width / 2 / (self.scale / 1.3)) >= -area_width / 2),
                ((self.x + screen_width / 2 / (self.scale / 1.3)) <= area_width / 2),
                ((self.y - screen_height / 2 / (self.scale / 1.3)) >= -area_height / 2),
                ((self.y + screen_height / 2 / (self.scale / 1.3)) <= area_width / 2)]):
            self.scale = self.scale / 1.3
        else:
            self.scale = max(screen_width / (2 * self.x + area_width), screen_width / (area_width - 2 * self.x),
                             screen_height / (2 * self.y + area_height), screen_height / (area_height - 2 * self.y))
