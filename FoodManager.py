import random
from sortedcontainers import SortedList


class FoodManager:

    def __init__(self):
        """
        Конструктор класса 'FoodManager'
        """

        self.food = SortedList()  # Список еды
        self.last_time_food_add = 0  # Время последней добавки еды
        self.time_add = 0.1  # Интервал добавок еды
        self.food_size = 5  # Размер еды

    def add_food(self):
        """
        Добавляет еду в случайную точку зоны действий
        """
        self.food.add((random.randint(-1000, 1000), random.randint(-1000, 1000)))

    def update(self, time_now):
        """
        Добавляет новую еду, если прошло достаточно времени с последнего добавления

        :param time_now: текущее время
        """

        if time_now > self.last_time_food_add + self.time_add:
            self.add_food()
            self.last_time_food_add = time_now

    def get_near_food(self, point):
        # Не оптимально, доделать!!!
        if len(self.food) == 0:
            return None
        min_r2, min_point = 99999999, 0
        for food in self.food:
            r2 = (point[0] - food[0]) ** 2 + (point[1] - food[1]) ** 2
            if min_r2 > r2:
                min_r2 = r2
                min_point = food
        return min_point

    def eat(self, point):
        """
        Удаляет еду, поглощённую животным из списка

        :param point: еда
        """
        self.food.remove(point)

    def get_food(self):
        """
        Возвращает список еды

        :return: список еды
        """
        return self.food
