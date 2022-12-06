import math
import random
from sortedcontainers import SortedList

class Cell:

    POS = -1000
    SIZE = 2048
    DEPTH_MAX = 30
    MAP = []

    def __init__(self):
        self.m = []
        for i in range(self.DEPTH_MAX):
            self.m.append([])
            for j in range(self.DEPTH_MAX):
                self.m[i].append([])
        self.SIZE /= self.DEPTH_MAX

    def add(self, x, y):
        xi = self.__get_x_index(x)
        yi = self.__get_y_index(y)
        self.m[yi][xi].append([x, y])

    def search(self, x, y):
        xi = self.__get_x_index(x)
        yi = self.__get_y_index(y)
        min_p, min_v = None, 99999999
        for X in range(xi-1, xi+2):
            if X < 0 or X >= self.DEPTH_MAX:
                continue
            for Y in range(yi-1, yi+2):
                if Y < 0 or Y >= self.DEPTH_MAX:
                    continue
                info = self.__search(x, y, X, Y)
                if info[1] < min_v:
                    min_v = info[1]
                    min_p = info[0]
        if min_p is None:
            return None
        return min_p

    def __get_x_index(self, x):
        return math.ceil((x-self.POS)/self.SIZE) - 1
    def __get_y_index(self, y):
        return math.ceil((y-self.POS)/self.SIZE) - 1

    def __search(self, x, y, xi, yi):
        min_v, min_p = 9999999, None
        for point in self.m[yi][xi]:
            P = (point[0] - x)**2 + (point[1] - y)**2
            if min_v > P:
                min_v = P
                min_p = point
        return [min_p, min_v]

    def get(self):
        list_get = []
        for i in range(self.DEPTH_MAX):
            for j in range(self.DEPTH_MAX):
                list_get += self.m[i][j]
        return list_get

    def remove(self, x, y):
        xi = self.__get_x_index(x)
        yi = self.__get_y_index(y)
        self.m[yi][xi].remove([x, y])



class FoodManager:

    def __init__(self, max_food=1000, count_food_start=None):
        """
        Конструктор класса 'FoodManager'
        """
        self.food = Cell()
        self.len_food = 0

        self.max_count_food = max_food
        self.time_add = 10
        self.food_size = 5
        if count_food_start is None:
            count_food_start = max_food//2

        self.last_time_food_add = -self.time_add * count_food_start
        self.update(self.time_add * count_food_start)

    def add_food(self):
        """
        Добавляет еду в случайную точку зоны действий
        """
        self.food.add(random.randint(-1000, 1000), random.randint(-1000, 1000))
        self.len_food += 1

    def update(self, time_now):
        """
        Добавляет новую еду, если прошло достаточно времени с последнего добавления
        :param time_now: текущее время
        """

        count_food_add = int((time_now - self.last_time_food_add)//self.time_add)
        for i in range(min(count_food_add, self.max_count_food - self.len_food)):
            self.add_food()
        self.last_time_food_add += count_food_add * self.time_add

    def get_near_food(self, point):
        """
        Возвращает ближайшую еду к животному
        :param point: координаты животного
        :return: ближайшая еда
        """
        return self.food.search(point[0], point[1])

    def eat(self, point):
        """
        Удаляет еду, поглощённую животным из списка
        :param point: еда
        """
        self.len_food -= 1
        self.food.remove(point[0], point[1])

    def get_food(self):
        """
        Возвращает список еды
        :return: список еды
        """
        return self.food.get()

    def start(self, time_now):
        self.last_time_food_add = time_now