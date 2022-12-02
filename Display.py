import pygame as pg
import Creature


def render(screen, creatures, food, camera, width, height):
    """
    Отрисовывает объекты на экране в соответствии с положением и масштабом камеры.

    :param screen: экран, на котором происходит отрисовка.
    :param creatures: животные для отрисовки.
    :param food: еда для отрисовки.
    :param camera: камера.
    :param width: ширина экрана.
    :param height: высота экрана.
    """

    screen.fill((0, 0, 0))
    pg.draw.rect(screen, (255, 0, 0), [(-990 - camera.x) * camera.scale + width / 2,
                                       (-990 - camera.y) * camera.scale + height / 2,
                                       1980 * camera.scale + 1,  # Прямоугольник добавлен для проверки кода,
                                       1980 * camera.scale + 1])  # удалить его в финальной версии

    # Отрисовка еды
    for coord_food in food.food:
        pg.draw.circle(screen, (0, 255, 0),
                       [(coord_food[0] - camera.x) * camera.scale + width / 2,
                        (coord_food[1] - camera.y) * camera.scale + height / 2],
                       (food.food_size * camera.scale) + 1)

    # Отрисовка животных
    for creature in creatures:
        # Отрисовка хищника
        if type(creature) == Creature.Hunter:
            pg.draw.rect(screen, creature.color,
                         [(creature.x - camera.x) * camera.scale + width / 2,
                          (creature.y - camera.y) * camera.scale + height / 2,
                          creature.size * camera.scale + 1,
                          creature.size * camera.scale + 1])
        # Отрисовка жертвы
        elif type(creature) == Creature.Prey:
            pg.draw.circle(screen, creature.color,
                           [(creature.x - camera.x) * camera.scale + width / 2,
                            (creature.y - camera.y) * camera.scale + height / 2],
                           (creature.size * camera.scale) + 1)
        # Отрисовка другого животного
        else:
            pg.draw.circle(screen, creature.color,
                           [(creature.x - camera.x) * camera.scale + width / 2,
                            (creature.y - camera.y) * camera.scale + height / 2],
                           (creature.size * camera.scale) + 1)

    pg.display.update()


class Camera:
    def __init__(self, x, y, scale=1):
        """
        Конструктор класса 'Камера'.

        :param x: горизонтальная координата камеры.
        :param y: вертикальная координата камеры.
        :param scale: масштаб камеры.
        """

        self.x = x
        self.y = y
        self.scale = scale

    def move(self, screen_width, screen_height, area_width, area_height):
        """
        Передвигает камеру по зоне действий.

        :param screen_width: ширина экрана.
        :param screen_height: высота экрана.
        :param area_width: ширина зоны действий.
        :param area_height: высота зоны действий.
        """

        kpressed = pg.key.get_pressed()

        # Движение вверх-вниз
        if not ((kpressed[pg.K_UP] or kpressed[pg.K_w]) and (kpressed[pg.K_DOWN] or kpressed[pg.K_s])):

            if kpressed[pg.K_UP] or kpressed[pg.K_w]:

                # Проверяем, что на следующем шаге не выйдем за пределы зоны действий
                if self.y - (screen_height / self.scale) / 2 >= -area_height / 2 + 10 / self.scale:
                    self.y -= 10 / self.scale   # Делим на масштаб, чтобы при меньшем масштабе камера двигалась быстрее
                else:
                    self.y = (screen_height / self.scale) / 2 - area_height / 2

            elif kpressed[pg.K_DOWN] or kpressed[pg.K_s]:

                if self.y + (screen_height / self.scale) / 2 <= area_height / 2 - 10 / self.scale:
                    self.y += 10 / self.scale
                else:
                    self.y = area_height / 2 - (screen_height / self.scale) / 2

        # Движение вправо-влево
        if not ((kpressed[pg.K_LEFT] or kpressed[pg.K_a]) and (kpressed[pg.K_RIGHT] or kpressed[pg.K_d])):

            if kpressed[pg.K_LEFT] or kpressed[pg.K_a]:

                if self.x - (screen_width / self.scale) / 2 >= -area_width / 2 + 10 / self.scale:
                    self.x -= 10 / self.scale
                else:
                    self.x = (screen_width / self.scale) / 2 - area_width / 2

            elif kpressed[pg.K_RIGHT] or kpressed[pg.K_d]:

                if self.x + (screen_height / self.scale) / 2 <= area_width / 2 - 10 / self.scale:
                    self.x += 10 / self.scale
                else:
                    self.x = area_width / 2 - (screen_height / self.scale) / 2

    # Приближение камеры
    def scale_plus(self):
        """
        Увеличивает масштаб изображения.
        """
        self.scale = self.scale * 1.3   # 1.3 - 'магическое' число, если есть смысл, можно параметризовать

    # Отдаление камеры
    def scale_minus(self, screen_width, screen_height, area_width, area_height):
        """
        Уменьшает масштаб изображения, учитывая положение камеры.

        :param screen_width: ширина экрана.
        :param screen_height: высота экрана.
        :param area_width: ширина зоны действий.
        :param area_height: высота зоны действий.
        """

        # Если можно свободно отдаляться без выхода из зоны действий
        if all([((self.x - screen_width / 2 / (self.scale / 1.3)) >= -area_width / 2),
                ((self.x + screen_width / 2 / (self.scale / 1.3)) <= area_width / 2),
                ((self.y - screen_height / 2 / (self.scale / 1.3)) >= -area_height / 2),
                ((self.y + screen_height / 2 / (self.scale / 1.3)) <= area_width / 2)]):

            self.scale = self.scale / 1.3

        else:
            # Если при очередном отдалении есть риск выйти за пределы зоны действий,
            # но камера не находится около её границы
            if all([((self.x - screen_width / 2 / self.scale) != -area_width / 2),
                    ((self.x + screen_width / 2 / self.scale) != area_width / 2),
                    ((self.y - screen_height / 2 / self.scale) != -area_height / 2),
                    ((self.y + screen_height / 2 / self.scale) != area_width / 2)]):

                self.scale = max(screen_width / (2 * self.x + area_width), screen_width / (area_width - 2 * self.x),
                                 screen_height / (2 * self.y + area_height), screen_height / (area_height - 2 * self.y))
            else:
                old_scale = self.scale

                # Если камера около левой стенки
                if (self.x - screen_width / 2 / old_scale) == -area_width / 2:
                    self.scale = max(old_scale / 1.3, screen_width / area_width,
                                     screen_height / (2 * (self.y + area_height / 2)) * (self.y <= 0) *
                                     ((self.y - screen_height / 2 / old_scale) != -area_height / 2),
                                     screen_height / (2 * (area_height / 2 - self.y)) * (self.y >= 0) *
                                     ((self.y + screen_height / 2 / old_scale) != area_height / 2))

                    self.x = (screen_width / self.scale - area_width) / 2

                # Если камера около правой стенки
                if (self.x + screen_width / 2 / old_scale) == area_width / 2:
                    self.scale = max(old_scale / 1.3, screen_width / area_width,
                                     screen_height / (2 * (self.y + area_height / 2)) * (self.y <= 0) *
                                     ((self.y - screen_height / 2 / old_scale) != -area_height / 2),
                                     screen_height / (2 * (area_height / 2 - self.y)) * (self.y >= 0) *
                                     ((self.y + screen_height / 2 / old_scale) != area_height / 2))

                    self.x = (area_width - screen_width / self.scale) / 2

                # Если камера около верхней стенки
                if (self.y - screen_height / 2 / old_scale) == -area_height / 2:
                    self.scale = max((old_scale / 1.3), (screen_height / area_height),
                                     (screen_width / (2 * (self.x + area_width / 2)) * (self.x <= 0) *
                                     ((self.x - screen_width / 2 / old_scale) != -area_width / 2)),
                                     (screen_width / (2 * (area_width / 2 - self.x)) * (self.x >= 0) *
                                     ((self.x + screen_width / 2 / old_scale) != area_width / 2)))

                    self.y = (screen_height / self.scale - area_height) / 2

                # Если камера около нижней стенки
                if (self.y + screen_height / 2 / old_scale) == area_height / 2:
                    self.scale = max((old_scale / 1.3), (screen_height / area_height),
                                     (screen_width / (2 * (self.x + area_width / 2)) * (self.x <= 0) *
                                     ((self.x - screen_width / 2 / old_scale) != -area_width / 2)),
                                     (screen_width / (2 * (area_width / 2 - self.x)) * (self.x >= 0) *
                                     ((self.x + screen_width / 2 / old_scale) != area_width / 2)))

                    self.y = (area_height - screen_height / self.scale) / 2
