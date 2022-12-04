import math

import genome_manager


class Creature:

    def __init__(self, size, speed, color, x=0, y=0, is_baby=False, energy=100, direction=0):
        """
        Конструктор класса 'Creature'.

        :param size: размер животного (радиус круга или сторона прямоугольника).
        :param speed: скорость перемещения животного по зоне действий.
        :param color: цвет животного.
        :param x: горизонтальная координата животного.
        :param y: вертикальная координата животного.
        :param direction: направление движения животного.
        :param is_baby: является ли ребенком
        :param energy: запас энергии животного. Если равен нулю, то животное умирает.
        """
        self.alive = True
        self.is_baby = is_baby
        self.reproducing = False
        self.time_alive = 0
        self.energy = energy
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.color = color
        self.direction = direction
        self.energy_loss = genome_manager.get_energy_loss(self.size, self.speed)

    def update(self, dt, food):
        """
        Обновляет состояние животного.

        :param dt: отрезок времени, задающий частоту обновления состояния.
        :param food: еда, которую животное может поглотить.
        """
        self.time_alive += dt
        if self.is_baby:
            self.is_baby = self.time_alive < 1
            return

        self.x += self.speed * math.cos(math.radians(self.direction)) * dt
        self.y += self.speed * math.sin(math.radians(self.direction)) * dt
        self.energy -= dt * self.energy_loss
        if self.energy <= 0:
            self.alive = False
        point = food.get_near_food((self.x, self.y))
        if point is None:
            return
        if (point[0] - self.x) ** 2 + (point[1] - self.y) ** 2 <= (self.size + food.food_size) ** 2:
            food.eat(point)
            self.energy += 20
            if self.energy > 200:
                self.reproducing = True
        else:
            self.move_to(point[0], point[1], dt)
        self.energy -= self.energy_loss * dt

        if self.energy <= 0:    # Если энергия - 0, то животное умирает
            self.alive = 0

    def is_dead(self):
        """
        Проверяет, умерло ли животное.

        :return: отрицание к параметру 'alive'.
        """
        return not self.alive

    def is_reproducing(self):
        """
        Проверяет, размножается ли животное.

        :return: параметр 'reproducing'.
        """
        return self.reproducing

    def get_child(self):
        """
        Отвечает за рождение потомка животного.

        :return: потомок животного.
        """
        child = genome_manager.get_child(self)
        self.energy /= 2
        self.reproducing = False
        return child

    def rotate(self, angle):
        """
        Отвечает за изменение направления движения животного.

        :param angle: угол, на который изменится направление движения.
        """
        self.direction += angle

    def move_to(self, x, y, dt):
        """
        Отвечает за передвижение к точке.

        :param x: координата x точки.
        :param y: координата y точки.
        :param dt: отрезок времени, задающий частоту обновления состояния.
        """
        X, Y = self.x - x, self.y - y
        k = 1
        if Y > 0:
            k = -1
        angle = (180 - math.degrees(math.acos(X / math.sqrt(X * X + Y * Y))) * k) % 360
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
