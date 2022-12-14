import pygame as pg


def render(screen, all_creatures, food, camera, screen_width, screen_height, area_width, area_height):
    """
    Отрисовывает объекты на экране в соответствии с положением и масштабом камеры.

    :param screen: экран, на котором происходит отрисовка.
    :param all_creatures: животные для отрисовки.
    :param food: еда для отрисовки.
    :param camera: камера.
    :param screen_width: ширина экрана.
    :param screen_height: высота экрана.
    :param area_width: ширина зоны действий.
    :param area_height: высота зоны действий.
    """

    screen.fill((0, 0, 0))
    pg.draw.rect(screen, (255, 0, 0), [((-area_width/2+10) - camera.x) * camera.scale + screen_width / 2,
                                       ((-area_height/2+10) - camera.y) * camera.scale + screen_height / 2,
                                       (area_width-20) * camera.scale + 1,
                                       (area_height-20) * camera.scale + 1])
    # Отрисовка еды
    for coord_food in food.food.get():
        pg.draw.circle(screen, (0, 255, 0),
                       [(coord_food[0] - camera.x) * camera.scale + screen_width / 2,
                        (coord_food[1] - camera.y) * camera.scale + screen_height / 2],
                       (food.food_size * camera.scale) + 1)

    # Отрисовка животных
    for cur_creature in all_creatures:
        pg.draw.circle(screen, cur_creature.color,
                       [(cur_creature.x - camera.x) * camera.scale + screen_width / 2,
                        (cur_creature.y - camera.y) * camera.scale + screen_height / 2],
                       (cur_creature.size * camera.scale) + 1)

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

                if self.x + (screen_width / self.scale) / 2 <= area_width / 2 - 10 / self.scale:
                    self.x += 10 / self.scale
                else:
                    self.x = area_width / 2 - (screen_width / self.scale) / 2

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

        scale_candidate = self.scale / 1.3

        # Если можно свободно отдаляться без выхода из зоны действий
        if all([((self.x - screen_width / 2 / scale_candidate) >= -area_width / 2),
                ((self.x + screen_width / 2 / scale_candidate) <= area_width / 2),
                ((self.y - screen_height / 2 / scale_candidate) >= -area_height / 2),
                ((self.y + screen_height / 2 / scale_candidate) <= area_width / 2)]):

            self.scale = scale_candidate

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
                old_x = self.x
                old_y = self.y

                # Если камера около левой или правой стенки
                if any([(old_x - screen_width / 2 / old_scale) == -area_width / 2,
                        (old_x + screen_width / 2 / old_scale) == area_width / 2]):
                    scale_candidate = max(old_scale / 1.3, screen_width / area_width,
                                          screen_height / (2 * (old_y + area_height / 2)) * (old_y <= 0) *
                                          ((old_y - screen_height / 2 / old_scale) != -area_height / 2),
                                          screen_height / (2 * (area_height / 2 - old_y)) * (old_y >= 0) *
                                          ((old_y + screen_height / 2 / old_scale) != area_height / 2))

                # Если камера около верхней или нижней стенки
                if any([(old_y - screen_height / 2 / old_scale) == -area_height / 2,
                        (old_y + screen_height / 2 / old_scale) == area_height / 2]):
                    scale_candidate = max((old_scale / 1.3), (screen_height / area_height),
                                          (screen_width / (2 * (old_x + area_width / 2)) * (old_x <= 0) *
                                          ((old_x - screen_width / 2 / old_scale) != -area_width / 2)),
                                          (screen_width / (2 * (area_width / 2 - old_x)) * (old_x >= 0) *
                                          ((old_x + screen_width / 2 / old_scale) != area_width / 2)),
                                          scale_candidate)
                self.scale = scale_candidate

                # Перемещение камеры от стенки
                if (self.x - screen_width / 2 / old_scale) == -area_width / 2:
                    self.x = (screen_width / self.scale - area_width) / 2

                elif (old_x + screen_width / 2 / old_scale) == area_width / 2:
                    self.x = (area_width - screen_width / self.scale) / 2

                if (self.y - screen_height / 2 / old_scale) == -area_height / 2:
                    self.y = (screen_height / self.scale - area_height) / 2

                elif (old_y + screen_height / 2 / old_scale) == area_height / 2:
                    self.y = (area_height - screen_height / self.scale) / 2
