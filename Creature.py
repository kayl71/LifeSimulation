import math

import GenomeManager


class Creature:

    def __init__(self, size, speed, color, x=0, y=0, energy=100, direction=0):
        """
        Конструктор класса 'Creature'.

        :param size: размер животного (радиус круга или сторона прямоугольника).
        :param speed: скорость перемещения животного по зоне действий.
        :param color: цвет животного.
        :param x: горизонтальная координата животного.
        :param y: вертикальная координата животного.
        :param energy: запас энергии животного. Если равен нулю, то животное умирает.
        :param direction: направление движения животного.
        """

        self.alive = True
        self.energy = energy
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.color = color
        self.direction = direction

        # Потеря энергии в зависимости от размера и скорости
        self.energy_loss = GenomeManager.get_energy_loss(self.size, self.speed)

    def update(self, dt, food):
        """
        Обновляет состояние животного.

        :param dt: отрезок времени, задающий частоту обновления состояния.
        :param food: еда, которую животное может поглотить.
        """

        self.x += self.speed * math.cos(math.radians(self.direction)) * dt
        self.y += self.speed * math.sin(math.radians(self.direction)) * dt
        self.energy -= dt * self.energy_loss

        if self.energy <= 0:    # Если энергия - 0, то животное умирает
            self.alive = False

        point = food.get_near_food((self.x, self.y))

        if point:
            if (point[0] - self.x) ** 2 + (point[1] - self.y) ** 2 <= (self.size + food.food_size) ** 2:
                food.eat(point)
                self.energy += 20
            else:
                self.move_to(point[0], point[1], dt)

            self.energy -= self.energy_loss * dt

            if self.energy <= 0:
                self.alive = 0

    def is_dead(self):
        """
        Проверяет, умерло ли животное.

        :return: отрицание к параметру 'alive'.
        """
        return not self.alive

    def rotate(self, angle):
        """
        Отвечает за изменение направления движения животного.

        :param angle: угол, на который изменится направление движения.
        """
        self.direction += angle

    def move_to(self, x, y, dt):
        """
        ???

        :param x: ?
        :param y: ?
        :param dt: ?

        :return: ?
        """

        x1, y1 = self.x - x, self.y - y
        k = 1
        if y1 > 0:
            k = -1
        angle = (180 - math.degrees(math.acos(x1 / math.sqrt(x1**2 + y1**2))) * k) % 360
        self.direction %= 360
        k = 1
        if angle - self.direction < 0:
            k = -1
        if not math.fabs(self.direction - angle) < 1:
            self.rotate(k * 5 * self.speed * dt)


class Hunter(Creature):
    pass


class Prey(Creature):
    pass
