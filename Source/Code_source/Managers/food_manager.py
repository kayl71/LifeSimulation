import math
import random


class AreaParameters:
    AREA_SIZE = 0


class Cell:
    def __init__(self):
        """
        Конструктор класса Cell.
        """

        self.POS = -AreaParameters.AREA_SIZE / 2
        self.SIZE = AreaParameters.AREA_SIZE
        self.DEPTH_MAX = 30
        self.MAP = []
        for i in range(self.DEPTH_MAX):
            self.MAP.append([])
            for j in range(self.DEPTH_MAX):
                self.MAP[i].append([])
        self.SIZE /= self.DEPTH_MAX

    def add(self, x, y, obj=None):
        """

        :param x:
        :param y:
        :param obj:

        :return:
        """

        xi = self.__get_x_index(x)
        yi = self.__get_y_index(y)
        if all([xi >= 0, xi < len(self.MAP[0]), yi >= 0, yi < len(self.MAP)]):
            self.MAP[yi][xi].append([x, y, obj])

    def search(self, x, y, without_it=False):
        """

        :param x:
        :param y:
        :param without_it:

        :return:
        """
        xi = self.__get_x_index(x)
        yi = self.__get_y_index(y)
        min_p, min_v = None, 99999999
        for X in range(xi - 1, xi + 2):
            if X < 0 or X >= self.DEPTH_MAX:
                continue
            for Y in range(yi - 1, yi + 2):
                if Y < 0 or Y >= self.DEPTH_MAX:
                    continue
                info = self.__search(x, y, X, Y, without_it)
                if info[1] < min_v:
                    min_v = info[1]
                    min_p = info[0]
        if min_p is None:
            return None
        return min_p

    def __get_x_index(self, x):
        """

        :param x:

        :return:
        """
        return math.ceil((x - self.POS) / self.SIZE) - 1

    def __get_y_index(self, y):
        """

        :param y:

        :return:
        """
        return math.ceil((y - self.POS) / self.SIZE) - 1

    def __search(self, x, y, xi, yi, without_it=False):
        """

        :param x:
        :param y:
        :param xi:
        :param yi:
        :param without_it:

        :return:
        """

        min_v, min_p = 9999999, None
        for point in self.MAP[yi][xi]:
            if without_it and x == point[0] and y == point[1]:
                continue
            p = (point[0] - x) ** 2 + (point[1] - y) ** 2
            if min_v > p:
                min_v = p
                min_p = point
        return [min_p, min_v]

    def get(self):
        """

        :return:
        """
        list_get = []
        for i in range(self.DEPTH_MAX):
            for j in range(self.DEPTH_MAX):
                list_get += self.MAP[i][j]
        return list_get

    def remove(self, x, y, obj=None):
        """

        :param x:
        :param y:
        :param obj:

        :return:
        """
        xi = self.__get_x_index(x)
        yi = self.__get_y_index(y)
        self.MAP[yi][xi].remove([x, y, obj])


class FoodManager:

    def __init__(self, max_food=1000, count_food_per_sec=1, count_food_start=20):
        """
        Конструктор класса 'FoodManager'.
        """

        self.food = Cell()
        self.len_food = 0

        self.max_count_food = max_food
        if count_food_per_sec == 0:
            self.time_add = 10 ** 9
        else:
            self.time_add = 1000 / count_food_per_sec
        self.food_size = 5

        self.last_time_food_add = -self.time_add * count_food_start
        self.update(self.time_add * count_food_start, 0)

    def add_food(self):
        """
        Добавляет еду в случайную точку зоны действий.
        """
        self.food.add(random.randint(-AreaParameters.AREA_SIZE // 2,
                                     AreaParameters.AREA_SIZE // 2),
                      random.randint(-AreaParameters.AREA_SIZE // 2,
                                     AreaParameters.AREA_SIZE // 2))
        self.len_food += 1

    def update(self, time_now, last_time):
        """
        Добавляет новую еду, если прошло достаточно времени с последнего добавления.

        :param time_now: текущее время.
        :param last_time: время последнего добавления.
        """

        count_food_add = int((time_now - last_time) // self.time_add)
        for i in range(min(count_food_add, self.max_count_food - self.len_food)):
            self.add_food()
        self.last_time_food_add = time_now

    def get_near_food(self, point):
        """
        Возвращает ближайшую еду к животному.
        :param point: координаты животного.

        :return: ближайшая еда.
        """
        return self.food.search(point[0], point[1])

    def eat(self, point):
        """
        Удаляет еду, поглощённую животным из списка.

        :param point: еда.
        """
        self.len_food -= 1
        self.food.remove(point[0], point[1])

    def get_food(self):
        """
        Возвращает список еды.

        :return: список еды.
        """
        return self.food.get()

    def start(self, time_now):
        """

        :param time_now:
        """
        self.last_time_food_add = time_now


if __name__ == "__main__":
    print("This module is not for direct call!")
