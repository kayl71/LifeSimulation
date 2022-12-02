import random


class FoodManager:

    def __init__(self):
        self.food = []
        self.last_time_food_add = 0
        self.time_add = 0.1
        self.food_size = 5

    def add_food(self):
        self.food.append([random.randint(-1000, 1000), random.randint(-1000, 1000)])

    def update(self, time_now):
        if time_now > self.last_time_food_add + self.time_add:
            self.add_food()
            self.last_time_food_add = time_now


    def get_food(self):
        return self.food