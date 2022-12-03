import random
from sortedcontainers import SortedList
class FoodManager:

    def __init__(self):
        self.food = SortedList()

        self.last_time_food_add = 0
        self.max_count_food =5000
        self.time_add = 5
        self.food_size = 5

    def add_food(self):
        self.food.add((random.randint(-1000, 1000), random.randint(-1000, 1000)))

    def update(self, time_now):
        if len(self.food) > self.max_count_food:
            return

        count_food_add = int((time_now - self.last_time_food_add)//self.time_add)
        for i in range(min(count_food_add, self.max_count_food - len(self.food))):
            self.add_food()
        self.last_time_food_add += count_food_add * self.time_add

    def get_near_food(self, point):
        # Не оптимально, доделать!!!
        if len(self.food) == 0:
            return None
        min_R2, min_point = 99999999, 0
        for food in self.food:
            R2 = (point[0] - food[0])**2 + (point[1] - food[1])**2
            if min_R2 > R2:
                min_R2 = R2
                min_point = food
        return min_point



    def eat(self, point):
        self.food.remove(point)

    def get_food(self):
        return self.food