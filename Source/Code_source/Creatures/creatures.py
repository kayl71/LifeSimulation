import math

from Source.Code_source.Managers import genome_manager


class Creature:
    IS_AGING = False

    def __init__(self, size, speed, color, x=0, y=0, is_baby=False, energy=200, direction=0,
                 alive=True, reproducing=False, time_alive=0, max_time_alive=30,
                 time_to_grow_up=3, energy_for_reproducing=500):
        """
        Конструктор класса 'Creature'.

        :param size: размер животного (радиус круга или сторона прямоугольника).
        :param speed: скорость перемещения животного по зоне действий.
        :param color: цвет животного.
        :param x: горизонтальная координата животного.
        :param y: вертикальная координата животного.
        :param is_baby: является ли ребенком.
        :param energy: запас энергии животного. Если равен нулю, то животное умирает.
        :param direction: направление движения животного.
        :param alive: живо ли животное.
        :param reproducing: размножается ли животное.
        :param time_alive: время жизни животного.
        :param max_time_alive: максимально возможное время жизни животного.
        :param time_to_grow_up: время, в течение которого новое животное не двигается.
        :param energy_for_reproducing: энергия, необходимая для размножения.
        """

        self.alive = alive
        self.is_baby = is_baby
        self.reproducing = reproducing
        self.time_alive = time_alive
        self.energy = energy
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.color = color
        self.direction = direction
        self.energy_loss = genome_manager.get_energy_loss(self.size, self.speed)
        self.max_time_alive = max_time_alive
        self.time_to_grow_up = time_to_grow_up
        self.energy_for_reproducing = energy_for_reproducing

    def update(self, dt, food):
        """
        Обновляет состояние животного.
        :param dt: отрезок времени, задающий частоту обновления состояния.
        :param food: еда, которую животное может поглотить.
        """

        self.time_alive += dt
        if self.is_baby:
            self.is_baby = self.time_alive < self.time_to_grow_up
            return
        if self.IS_AGING and self.time_alive > self.max_time_alive:
            self.alive = False

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
            if self.energy > self.energy_for_reproducing:
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
        self.energy /= 3
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
            self.rotate(k * 10 * self.speed * dt)


class Hunter(Creature):
    def hunter_update(self, dt, near_prey=None):
        """
        Обновляет состояние животного.
        :param dt: отрезок времени, задающий частоту обновления состояния.
        :param near_prey: ближайшая жертва
        """

        self.time_alive += dt
        if self.is_baby:
            self.is_baby = self.time_alive < self.time_to_grow_up
            return
        if self.IS_AGING and self.time_alive > self.max_time_alive:
            self.alive = False

        self.x += self.speed * math.cos(math.radians(self.direction)) * dt
        self.y += self.speed * math.sin(math.radians(self.direction)) * dt
        self.energy -= dt * self.energy_loss
        if self.energy <= 0:
            self.alive = False
            return

        if near_prey is None or near_prey.size > self.size:
            return
        point = [near_prey.x, near_prey.y]

        if (point[0] - self.x) ** 2 + (point[1] - self.y) ** 2 <= (self.size + near_prey.size) ** 2:
            self.energy = min(self.energy+near_prey.energy, 600)
            near_prey.alive = False
            if self.energy > self.energy_for_reproducing:
                self.reproducing = True
        else:
            self.move_to(point[0], point[1], dt)
        self.energy -= self.energy_loss * dt


class Prey(Creature):
    def prey_update(self, dt, food):
        """
        Обновляет состояние животного.
        :param dt: отрезок времени, задающий частоту обновления состояния.
        :param food: еда, которую животное может поглотить.
        """

        self.time_alive += dt
        if self.is_baby:
            self.is_baby = self.time_alive < self.time_to_grow_up
            return
        if self.IS_AGING and self.time_alive > self.max_time_alive:
            self.alive = False

        self.x += self.speed * math.cos(math.radians(self.direction)) * dt
        self.y += self.speed * math.sin(math.radians(self.direction)) * dt
        self.energy -= dt * self.energy_loss
        if self.energy <= 0:
            self.alive = False
            return

        point = food.get_near_food((self.x, self.y))
        if point is None:
            return

        if (point[0] - self.x) ** 2 + (point[1] - self.y) ** 2 <= (self.size + food.food_size) ** 2:
            food.eat(point)
            self.energy += 20
            if self.energy > self.energy_for_reproducing:
                self.reproducing = True
        else:
            self.move_to(point[0], point[1], dt)
        self.energy -= self.energy_loss * dt


if __name__ == "__main__":
    print("This module is not for direct call!")
