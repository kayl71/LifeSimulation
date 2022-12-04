import pygame as pg

import display
import food_manager
import genome_manager
import menus


class Core:

    def __init__(self):
        """
        Конструктор класса Core.
        """
        self.creatures = genome_manager.create_population(6)

        self.creatures[1].color = (255, 255, 0)
        self.creatures[2].color = (0, 0, 255)
        self.creatures[3].color = (0, 255, 255)
        self.creatures[4].color = (255, 0, 255)
        self.creatures[5].color = (0, 0 , 0)

        self.food = food_manager.FoodManager(1000)
        self.alive = True   # Существует ли программа
        self.running = False    # Идёт ли симуляция
        self.existing = False   # Существует ли симуляция
        pg.init()
        self.screen_width = 700
        self.screen_height = 700
        self.area_width = 2000
        self.area_height = 2000
        self.camera = display.Camera(self.screen_width//2, self.screen_height//2)
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        self.fullscreen_menu = menus.FullScreenMenu(self.screen, self.screen_width, self.screen_height, self.existing)

    def run(self):
        menu = self.fullscreen_menu.initialize()
        time_now = pg.time.get_ticks()
        time_last_update = time_now
        time_last_fixed_update = time_now
        FUPS = 4  # Fixed Update Per Second
        UPS = 60  # Update Per Second

        while self.alive and self.fullscreen_menu.alive:
            time_now = pg.time.get_ticks()
            self.handle_events(pg.event.get(), menu)

            if self.running and time_now - time_last_fixed_update > 1000 / FUPS:
                time_last_fixed_update = time_now

            if self.fullscreen_menu.running and time_now - time_last_update > 1000 / UPS:
                self.update((time_now - time_last_update) / 1000)
                self.render()
                self.camera.move(self.screen_width, self.screen_height, self.area_width, self.area_height)
                self.food.update(time_now)
                time_last_update = time_now

        pg.quit()

    def handle_events(self, events, menu):
        for event in events:
            if not self.fullscreen_menu.running:
                menu.react(event)
            if event.type == pg.QUIT:
                self.alive = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.camera.scale_plus()
                elif event.button == 5:
                    self.camera.scale_minus(self.screen_width, self.screen_height, self.area_width, self.area_height)


    def fixed_update(self):
        pass

    def render(self):
        """
        Отрисовка всех объектов на экран
        """
        display.render(self.screen, self.creatures, self.food, self.camera, self.screen_width, self.screen_height)

    def update(self, delta_time):
        """
        Обновляет состояние всех животных на экране
        :param delta_time: отрезок времени, отвечающий за частоту обновления
        """
        for creature in self.creatures:
            if creature.is_dead():
                self.creatures.remove(creature)
            else:
                creature.update(delta_time, self.food)
                if creature.is_reproducing():
                    self.creatures.append(creature.get_child())


    def begin(self):
        self.existing = True

    def end(self):
        self.existing = False

    def start(self):
        self.running = True

    def stop(self):
        self.running = False


if __name__ == "__main__":
    core = Core()
    core.run()
