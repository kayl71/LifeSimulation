import random
from sortedcontainers import SortedList

class Square:
    HEIGHT = 2048
    WIDTH = 2048

    def __init__(self, depth, height=HEIGHT, width=WIDTH, x=0, y=0):
        self.depth = depth
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        if depth > 0:
            self.m = [
                Square(depth - 1, height // 2, width // 2, x, y),
                Square(depth - 1, height // 2, width // 2, x + width // 2, y),
                Square(depth - 1, height // 2, width // 2, x, y + height // 2),
                Square(depth - 1, height // 2, width // 2, x + width // 2, y + height // 2)
            ]
        else:
            self.m = []

    def __search(self, x: int, y: int, link = None):
        if self.depth == 0:
            if len(self.m) == 0:
                return None
            mp = None
            mv = 9999999
            for p in self.m:
                v = (x - p[0]) ** 2 + (y - p[1]) ** 2
                if mv > v:
                    mv = v
                    mp = p
            if mp is None:
                return None
            return (mp, mv, self)

        pos = self.__get_pos(x, y)
        X = self.m[pos].__search(x, y, link)
        if not X is None:
            return X

        point, value = (0, 0), 9999999
        for i in range(len(self.m)):
            if pos == i:
                continue
            pv = self.m[i].__search(x, y)
            if pv is None or value < pv[1]:
                continue
            point = pv[0]
            value = pv[1]
            link = pv[2]
        if value == 9999999:
            return None
        return (point, value, link)

    def __get_pos(self, x: int, y: int):
        pos = 0
        if self.x is None or self.width is None or x is None:
            print(self.x, self.width, x)
        if self.x + self.width//2 < x:
            pos += 1
        if self.y + self.height//2 < y:
            pos += 2
        return pos

    def add(self, x: int, y: int):
        if self.depth == 0:
            self.m.append((x, y))
            return

        pos = self.__get_pos(x, y)
        self.m[pos].add(x, y)

    def get(self):
        if self.depth == 0:
            return self.m

        lists = []
        for square in self.m:
            lists += square.get()
        return lists

    def search(self, x, y):
        info = self.__search(x, y)
        if info is None:
            return None
        return (info[0][0], info[0][1])
    def remove(self, x, y):
        info = self.__search(x, y)
        info[2].m.remove((x, y))


class FoodManager:

    def __init__(self, max_food=1000, count_food_start=None):
        """
        Конструктор класса 'FoodManager'
        """
        self.food = Square(8, x = -1024, y = -1024)
        self.len_food = 0

        self.max_count_food = max_food
        self.time_add = 2
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
